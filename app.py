# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Updated symptom-condition mapping
# conditions = {
#     "Flu": ["fever", "cough", "body ache", "fatigue", "headache", "chills", "sore throat", "congestion"],
#     "Covid-19": ["fever", "cough", "fatigue", "shortness of breath", "loss of taste", "loss of smell", "body ache", "sore throat", "headache"],
#     "Viral Infection": ["fatigue", "fever", "headache", "body ache", "cough", "sore throat", "chills", "runny nose"],
#     "Allergy": ["sneezing", "runny nose", "itchy eyes", "skin rash", "cough", "congestion", "wheezing"],
#     "Stomach Bug": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever", "fatigue"],
#     "Migraine": ["headache", "nausea", "sensitivity to light", "sensitivity to sound", "fatigue", "vision changes"],
#     "Sinus Infection": ["headache", "facial pain", "congestion", "runny nose", "sore throat", "fatigue"],
#     "Common Cold": ["sneezing", "runny nose", "cough", "sore throat", "mild fever", "fatigue"],
#     "Bronchitis": ["cough", "chest discomfort", "fatigue", "shortness of breath", "fever", "sore throat"],
#     "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "body ache"]
# }

# # Sample precautions and medicines
# precautions = {
#     "Flu": ["Rest well", "Drink fluids", "Take fever medication"],
#     "Covid-19": ["Isolate yourself", "Monitor oxygen levels", "Drink warm fluids"],
#     "Viral Infection": ["Stay hydrated", "Take pain relievers", "Get enough rest"],
#     "Allergy": ["Avoid allergens", "Take antihistamines", "Use a nasal spray"],
#     "Stomach Bug": ["Drink electrolytes", "Eat bland foods", "Avoid dairy"],
#     "Migraine": ["Rest in a dark room", "Take pain relievers", "Avoid triggers"],
#     "Sinus Infection": ["Use steam inhalation", "Drink warm fluids", "Take decongestants"],
#     "Common Cold": ["Drink warm tea", "Use a humidifier", "Get plenty of rest"],
#     "Bronchitis": ["Use a humidifier", "Drink warm liquids", "Avoid smoking"],
#     "Pneumonia": ["Seek medical attention", "Take antibiotics (if bacterial)", "Get plenty of rest"]
# }

# medicines = {
#     "Flu": ["Paracetamol", "Ibuprofen"],
#     "Covid-19": ["Paracetamol", "Cough syrup"],
#     "Viral Infection": ["Acetaminophen", "Ibuprofen"],
#     "Allergy": ["Antihistamines", "Nasal spray"],
#     "Stomach Bug": ["ORS solution", "Loperamide"],
#     "Migraine": ["Pain relievers", "Anti-nausea medication"],
#     "Sinus Infection": ["Decongestants", "Nasal steroids"],
#     "Common Cold": ["Cough syrup", "Vitamin C"],
#     "Bronchitis": ["Cough suppressants", "Bronchodilators"],
#     "Pneumonia": ["Antibiotics (if bacterial)", "Cough medicine"]
# }

# @app.route("/")
# def home():
#     return render_template("index.html", symptoms=sorted(set(sum(conditions.values(), []))))  # Unique symptom list

# @app.route("/diagnose", methods=["POST"])
# def diagnose():
#     selected_symptoms = request.form.getlist("symptoms-selector")
#     if not selected_symptoms:
#         return render_template("result.html", diagnosis="No symptoms selected. Please try again.", precautions=[], medicines=[])

#     # Match conditions based on symptoms
#     condition_scores = {condition: sum(symptom in selected_symptoms for symptom in symptoms) for condition, symptoms in conditions.items()}
    
#     # Filter conditions with at least 1 matching symptom
#     possible_conditions = [cond for cond, score in condition_scores.items() if score > 0]
#     possible_conditions.sort(key=lambda x: condition_scores[x], reverse=True)  # Sort by highest matches

#     if not possible_conditions:
#         diagnosis = "No exact match found. Consider consulting a doctor."
#     else:
#         diagnosis = f"Possible conditions: {', '.join(possible_conditions)}"

#     # Get associated precautions and medicines for suggested conditions
#     suggested_precautions = {condition: precautions.get(condition, []) for condition in possible_conditions}
#     suggested_medicines = {condition: medicines.get(condition, []) for condition in possible_conditions}

#     return render_template("result.html", diagnosis=diagnosis, precautions=suggested_precautions, medicines=suggested_medicines)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load trained model and vectorizer
with open("model/symptom_checker.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("model/vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Expanded disease data with symptoms, precautions, and medicines
disease_data = {
    "Flu": {
        "Symptoms": ["fever", "cough", "body ache", "fatigue", "headache", "chills", "sore throat", "congestion"],
        "Precautions": "Rest well, drink fluids, take fever medication",
        "Medicine": "Paracetamol, Ibuprofen"
    },
    "Covid-19": {
        "Symptoms": ["fever", "cough", "fatigue", "shortness of breath", "loss of taste", "loss of smell", "body ache", "sore throat", "headache"],
        "Precautions": "Isolate yourself, monitor oxygen levels, drink warm fluids",
        "Medicine": "Paracetamol, Cough syrup"
    },
    "Viral Infection": {
        "Symptoms": ["fatigue", "fever", "headache", "body ache", "cough", "sore throat", "chills", "runny nose"],
        "Precautions": "Stay hydrated, take pain relievers, get enough rest",
        "Medicine": "Acetaminophen, Ibuprofen"
    },
    "Allergy": {
        "Symptoms": ["sneezing", "runny nose", "itchy eyes", "skin rash", "cough", "congestion", "wheezing"],
        "Precautions": "Avoid allergens, take antihistamines, use a nasal spray",
        "Medicine": "Antihistamines, Nasal spray"
    },
    "Stomach Bug": {
        "Symptoms": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever", "fatigue"],
        "Precautions": "Drink electrolytes, eat bland foods, avoid dairy",
        "Medicine": "ORS solution, Loperamide"
    },
    "Migraine": {
        "Symptoms": ["headache", "nausea", "sensitivity to light", "sensitivity to sound", "fatigue", "vision changes"],
        "Precautions": "Rest in a dark room, take pain relievers, avoid triggers",
        "Medicine": "Pain relievers, Anti-nausea medication"
    },
    "Sinus Infection": {
        "Symptoms": ["headache", "facial pain", "congestion", "runny nose", "sore throat", "fatigue"],
        "Precautions": "Use steam inhalation, drink warm fluids, take decongestants",
        "Medicine": "Decongestants, Nasal steroids"
    },
    "Common Cold": {
        "Symptoms": ["sneezing", "runny nose", "cough", "sore throat", "mild fever", "fatigue"],
        "Precautions": "Drink warm tea, use a humidifier, get plenty of rest",
        "Medicine": "Cough syrup, Vitamin C"
    },
    "Bronchitis": {
        "Symptoms": ["cough", "chest discomfort", "fatigue", "shortness of breath", "fever", "sore throat"],
        "Precautions": "Use a humidifier, drink warm liquids, avoid smoking",
        "Medicine": "Cough suppressants, Bronchodilators"
    },
    "Pneumonia": {
        "Symptoms": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "body ache"],
        "Precautions": "Seek medical attention, take antibiotics (if bacterial), get plenty of rest",
        "Medicine": "Antibiotics, Cough medicine"
    }
}

@app.route("/")
def index():
    symptoms_list = sorted(set(symptom for disease in disease_data.values() for symptom in disease["Symptoms"]))
    return render_template("index.html", symptoms=symptoms_list)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    symptoms_input = request.form.get("symptoms-selector", "").strip().split(",")

    # If no symptoms are selected, return an error message
    if not symptoms_input or symptoms_input == [""]:
        return render_template(
            "result.html", 
            disease="⚠️ No symptoms selected", 
            precautions="Please select symptoms to get a diagnosis.", 
            medicine="Consult a doctor for further guidance."
        )

    # Convert input into vectorized form
    symptoms_vector = vectorizer.transform([" ".join(symptoms_input)])

    # Predict diseases (Multiple possible diseases)
    predicted_diseases = model.predict(symptoms_vector)

    # Store matching diseases, precautions, and medicines
    matched_diseases = []
    precautions_list = []
    medicine_list = []

    for disease in predicted_diseases:
        if disease in disease_data:
            matched_diseases.append(disease)
            precautions_list.append(disease_data[disease]["Precautions"])
            medicine_list.append(disease_data[disease]["Medicine"])

    # If no known disease matches, return a message
    if not matched_diseases:
        return render_template(
            "result.html", 
            disease="⚠️ No matching disease found", 
            precautions="Your symptoms do not match a specific disease in our database. Please consult a doctor.",
            medicine="N/A"
        )

    return render_template(
        "result.html",
        disease=", ".join(matched_diseases),
        precautions=" | ".join(precautions_list),
        medicine=" | ".join(medicine_list)
    )

if __name__ == "__main__":
    app.run(debug=True)
