from flask import Blueprint, jsonify, request, send_file
import pandas as pd
from datetime import datetime
from io import BytesIO
from pdf_generator import generate_patient_pdf  # Import the PDF generation function
from report_generator import generate_full_report  # Import the report generation function

# Initialize the blueprint
api_bp = Blueprint('api', __name__)

# Read the CSV file and ensure 'Patient ID' is treated as a string
patient_data = pd.read_csv("human_vital_signs_dataset_2024.csv")
patient_data['Patient ID'] = patient_data['Patient ID'].astype(str)

# Number of patients per page
PATIENTS_PER_PAGE = 20

# API Route to fetch list of patients
@api_bp.route('/patients', methods=['GET'])
def get_patients():
    # Pagination
    page = int(request.args.get('page', 1))
    start = (page - 1) * PATIENTS_PER_PAGE
    end = start + PATIENTS_PER_PAGE
    patients_page = patient_data.iloc[start:end]
    
    # Generate list of patient IDs to return
    patients = patients_page['Patient ID'].tolist()

    return jsonify({
        "patients": patients,
        "page": page,
        "total_pages": (len(patient_data) + PATIENTS_PER_PAGE - 1) // PATIENTS_PER_PAGE
    })

# API Route to generate full report for a specific patient
@api_bp.route('/patient_report/<int:patient_id>', methods=['GET'])
def patient_report(patient_id):
    # Check if the patient exists
    patient_data_filtered = patient_data[patient_data['Patient ID'] == str(patient_id)]
    if patient_data_filtered.empty:
        return jsonify({"error": f"Patient with ID {patient_id} not found."}), 404

    # Get the first matching patient (since we expect unique Patient IDs)
    patient = patient_data_filtered.iloc[0]
    
    # Call the report generator to generate the full report
    full_report = generate_full_report(patient)
    
    # Return the full report as JSON
    return jsonify({"report": full_report})

# API Route to generate PDF for a specific patient
@api_bp.route('/generate_pdf/<patient_id>', methods=['GET'])
def generate_pdf(patient_id):
    # Ensure the patient_id is treated as a string for consistent comparison
    patient_id = str(patient_id)

    if patient_id not in patient_data['Patient ID'].values:
        return jsonify({"error": f"Patient with ID {patient_id} not found."}), 404

    # Find the patient data based on the selected Patient ID
    patient = patient_data[patient_data['Patient ID'] == patient_id].iloc[0]
    
    # Generate the full report as a string
    full_report = generate_full_report(patient)

    # Parse the full report string to separate out patient details, diagnosis, and recommendations
    report_data = {
        'patient_id': patient['Patient ID'],
        'gender': patient['Gender'],
        'age': patient['Age'],
        'weight': patient['Weight (kg)'],
        'height': patient['Height (m)'],
        'bmi': patient['Derived_BMI'],
        'vital_signs': {
            'heart_rate': patient['Heart Rate'],
            'respiratory_rate': patient['Respiratory Rate'],
            'body_temp': patient['Body Temperature'],
            'oxygen_saturation': patient['Oxygen Saturation'],
            'systolic_bp': patient['Systolic Blood Pressure'],
            'diastolic_bp': patient['Diastolic Blood Pressure'],
            'pulse_pressure': patient['Derived_Pulse_Pressure'],
            'map': patient['Derived_MAP'],
            'hrv': patient['Derived_HRV'],
        },
        'diagnosis': full_report.split("\n\n")[1],  # Assuming diagnosis is the second part of the report
        'recommendations': full_report.split("\n\n")[2],  # Assuming recommendations are the third part
        'report_timestamp': datetime.now().strftime('%d %b %Y, %I:%M %p')
    }

    # Path to wkhtmltopdf executable (adjust this path if necessary)
    path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    
    # Call the generate_patient_pdf function from pdf_generator.py
    pdf = generate_patient_pdf(report_data, path_to_wkhtmltopdf)
    
    # Send the PDF as a downloadable file
    return send_file(pdf, download_name=f"patient_{patient_id}_report.pdf", as_attachment=True)
