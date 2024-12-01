from datetime import datetime
from groq import Groq
import os

# Set up your Groq API key and client
GROQ_API_KEY = os.environ.get("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")
groq_client = Groq(api_key=GROQ_API_KEY)

def parse_patient_data(data):
    """
    Parse patient data from a dictionary into a human-readable report.

    Parameters
    ----------
    data : dict
        A dictionary containing the patient data.

    Returns
    -------
    dict
        A dictionary containing the parsed patient report.
    """
    patient_id = data.get("Patient ID")
    heart_rate = data.get("Heart Rate")
    respiratory_rate = data.get("Respiratory Rate")
    timestamp = data.get("Timestamp").split(".")[0]
    body_temp = data.get("Body Temperature")
    oxygen_saturation = data.get("Oxygen Saturation")
    systolic_bp = data.get("Systolic Blood Pressure")
    diastolic_bp = data.get("Diastolic Blood Pressure")
    age = data.get("Age")
    gender = data.get("Gender")
    weight = data.get("Weight (kg)")
    height = data.get("Height (m)")
    hrv = data.get("Derived_HRV")
    pulse_pressure = data.get("Derived_Pulse_Pressure")
    bmi = data.get("Derived_BMI")
    map_value = data.get("Derived_MAP")

    # Parse timestamp to readable format
    formatted_timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    # Generate the report in a structured way
    report = {
        "patient_id": patient_id,
        "gender": gender,
        "age": age,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "vital_signs": {
            "heart_rate": heart_rate,
            "respiratory_rate": respiratory_rate,
            "body_temp": body_temp,
            "oxygen_saturation": oxygen_saturation,
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "pulse_pressure": pulse_pressure,
            "map": map_value,
            "hrv": hrv
        },
        "report_timestamp": formatted_timestamp.strftime('%d %b %Y, %I:%M %p')
    }
    return report

def generate_diagnosis(report):
    """
    Generate a diagnosis based on the patient report.

    Parameters
    ----------
    report : dict
        A dictionary containing the patient report.

    Returns
    -------
    str
        The generated diagnosis.
    """
    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role": "user",
            "content": f"""Vous êtes un assistant médical expert. Sur la base des données fournies sur le patient, analysez les informations et fournissez un diagnostic préliminaire ou identifiez d'éventuelles préoccupations. Prenez en compte les éléments suivants :\n\n{report}\n\nSoyez concis mais précis. S'il n'y a pas suffisamment d'informations pour établir un diagnostic concluant, suggérez des tests ou des données supplémentaires qui permettraient de clarifier l'état du patient. Ne faites aucune supposition sur la santé du patient.\n\nVotre réponse doit être formatée comme suit :\n\nDiagnostic : <diagnostic>\nTests ou Données Supplémentaires Requises : <tests ou données>\n\nRéponse :"""
        }],
        temperature=0.1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    diagnosis = ""
    for chunk in completion:
        diagnosis += chunk.choices[0].delta.content or ""

    return diagnosis

def generate_recommendations(report, diagnosis):
    """
    Generate recommendations based on patient report and diagnosis.

    Parameters
    ----------
    report : dict
        The patient report.
    diagnosis : str
        The diagnosis of the patient.

    Returns
    -------
    str
        The recommendations for the patient, formatted as a string.
    """
    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role": "user",
            "content": f"""Vous êtes un assistant médical expert en soins aux patients. Ci-dessous se trouvent un rapport de patient, un diagnostic et un contexte médical pertinent. Sur la base de ces informations, fournissez des recommandations claires et actionnables, telles que des traitements ou des ajustements de style de vie.\n\nRapport du Patient :\n{report}\n\nDiagnostic :\n{diagnosis}\n\nSortie :\nRecommandations : Fournissez des étapes détaillées à suivre, incluant des traitements, des changements de mode de vie ou des tests, adaptés à l'état du patient et au contexte fourni.\n\nVotre réponse doit être formatée comme suit, n'ajoute rien d'autre que les recommandations :\n\nRecommandations court terme : <recommandations court terme>\nRecommandations moyen terme : <recommandations moyen terme>\nRecommandations long terme : <recommandations long terme>\n\nRéponse :"""
        }],
        temperature=0.1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    recommendations = ""
    for chunk in completion:
        recommendations += chunk.choices[0].delta.content or ""

    return recommendations

def generate_full_report(data):
    """
    Generate a comprehensive patient report including diagnosis and recommendations.

    Parameters
    ----------
    data : dict
        A dictionary containing patient vital signs and other relevant data.

    Returns
    -------
    str
        A formatted string containing the patient report, diagnosis, and recommendations.
    """
    report = parse_patient_data(data)
    diagnosis = generate_diagnosis(report)
    recommendations = generate_recommendations(report, diagnosis)

    full_report = f"{report}\n\n{diagnosis}\n\n{recommendations}"
    return full_report
