from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests  # Use requests to make API calls
import traceback

app = Flask(__name__, static_folder='assets', static_url_path='/assets')

# Register the API blueprint
from api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    try:
        page = int(request.args.get('page', 1))
        
        # Make a request to the API to fetch patient data
        response = requests.get(f'http://localhost:5000/api/patients?page={page}')
        
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            patients = data.get('patients', [])
            total_pages = data.get('total_pages', 0)
        else:
            # Handle error if API request fails
            patients = []
            total_pages = 0
        
        # Pass the data to the template
        return render_template(
            'index.html',
            show_patient_list=True,
            patients=patients,
            page=page,
            total_pages=total_pages
        )
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return "An error occurred", 500

@app.route('/patient/<int:patient_id>')
def patient_report(patient_id):
    try:
        # Fetch the patient report by calling the API endpoint
        response = requests.get(f'http://localhost:5000/api/patient_report/{patient_id}')
        
        if response.status_code == 200:
            # Parse the full report string returned by the API
            full_report = response.json().get('report', '')
            report_sections = full_report.split("\n\n")

            if len(report_sections) < 3:
                error = "Report is incomplete. Please check the data."
                return render_template('index.html', error=error)

            # Extract report, diagnosis, and recommendations
            report_data = eval(report_sections[0])  # Convert string to dictionary
            diagnosis = report_sections[1]
            recommendations = report_sections[2]

            # Pass parsed data to the template
            return render_template(
                'index.html',
                report_string=report_data,
                diagnosis=diagnosis,
                recommendations=recommendations,
                patient_id=patient_id
            )
        else:
            error = response.json().get('error', 'Unknown error occurred')
            return render_template('index.html', error=error)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return "An error occurred", 500

@app.route('/generate_pdf/<int:patient_id>')
def generate_pdf(patient_id):
    # Redirect to the API endpoint for PDF generation
    return redirect(f'/api/generate_pdf/{patient_id}')

if __name__ == '__main__':
    app.run(debug=True)
