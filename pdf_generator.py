import pdfkit
from io import BytesIO

# Function to generate a PDF from a detailed patient report
def generate_patient_pdf(report_string, path_to_wkhtmltopdf):
    # Generate HTML content for the PDF with detailed and organized formatting
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
            }}
            h1 {{
                color: #333;
                text-align: center;
                font-size: 24px;
            }}
            .section {{
                margin-top: 20px;
                padding: 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .section h2 {{
                color: #555;
                font-size: 20px;
                margin-bottom: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            table, th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
            }}
            .report-timestamp {{
                text-align: center;
                font-size: 14px;
                margin-top: 20px;
                color: #777;
            }}
            .diagnosis, .recommendations {{
                margin-top: 30px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #eef;
            }}
            .recommendations h3, .diagnosis h3 {{
                color: #555;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-family: 'Courier New', Courier, monospace;
            }}
        </style>
    </head>
    <body>
        <h1>Patient Report: {report_string['patient_id']}</h1>
        
        <div class="section">
            <h2>Patient Details</h2>
            <p><strong>Gender:</strong> {report_string['gender']}</p>
            <p><strong>Age:</strong> {report_string['age']}</p>
            <p><strong>Weight:</strong> {report_string['weight']} kg</p>
            <p><strong>Height:</strong> {report_string['height']} m</p>
            <p><strong>BMI:</strong> {report_string['bmi']}</p>
        </div>

        <div class="section">
            <h2>Vital Signs</h2>
            <table>
                <tr>
                    <th>Heart Rate (bpm)</th>
                    <td>{report_string['vital_signs']['heart_rate']}</td>
                </tr>
                <tr>
                    <th>Respiratory Rate (bpm)</th>
                    <td>{report_string['vital_signs']['respiratory_rate']}</td>
                </tr>
                <tr>
                    <th>Body Temperature (°C)</th>
                    <td>{report_string['vital_signs']['body_temp']}</td>
                </tr>
                <tr>
                    <th>Oxygen Saturation (%)</th>
                    <td>{report_string['vital_signs']['oxygen_saturation']}</td>
                </tr>
                <tr>
                    <th>Systolic BP (mmHg)</th>
                    <td>{report_string['vital_signs']['systolic_bp']}</td>
                </tr>
                <tr>
                    <th>Diastolic BP (mmHg)</th>
                    <td>{report_string['vital_signs']['diastolic_bp']}</td>
                </tr>
                <tr>
                    <th>Pulse Pressure (mmHg)</th>
                    <td>{report_string['vital_signs']['pulse_pressure']}</td>
                </tr>
                <tr>
                    <th>MAP (mmHg)</th>
                    <td>{report_string['vital_signs']['map']}</td>
                </tr>
                <tr>
                    <th>HRV</th>
                    <td>{report_string['vital_signs']['hrv']}</td>
                </tr>
            </table>
        </div>

        <div class="diagnosis">
            <h3>Diagnosis</h3>
            <pre>{report_string['diagnosis']}</pre>
        </div>

        <div class="recommendations">
            <h3>Recommendations</h3>
            <pre>{report_string['recommendations']}</pre>
        </div>

        <div class="report-timestamp">
            <p><strong>Report Generated on:</strong> {report_string['report_timestamp']}</p>
        </div>
    </body>
    </html>
    """

    # Create a pdfkit configuration with the path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    
    # Generate the PDF from the HTML content
    pdf = pdfkit.from_string(html_content, False, configuration=config)

    # Return the generated PDF as a BytesIO object (in-memory PDF)
    return BytesIO(pdf)
