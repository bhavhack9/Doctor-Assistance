# import csv
#
# # Function to read the CSV file and build a dictionary mapping symptoms to diseases
# def build_symptom_disease_mapping(csv_file):
#     symptom_disease_mapping = {}
#     with open(csv_file, newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row if it exists
#         for row in reader:
#             symptoms = [symptom.strip() for symptom in row[0].split(",") if symptom.strip()]
#             disease = row[1].strip()
#             if disease not in symptom_disease_mapping:
#                 symptom_disease_mapping[disease] = set(symptoms)
#             else:
#                 symptom_disease_mapping[disease].update(symptoms)
#     return symptom_disease_mapping
#
# # Function to predict diseases based on user-input symptoms
# def predict_diseases(symptom_disease_mapping, user_symptoms):
#     predicted_diseases = {}
#
#     for disease, symptoms in symptom_disease_mapping.items():
#         if user_symptoms.issubset(symptoms):
#             predicted_diseases[disease] = symptoms
#
#     return predicted_diseases
#
# # Function to calculate common symptoms from a list of diseases
# def calculate_common_symptoms(symptom_disease_mapping, diseases, provided_symptoms):
#     common_symptoms = set.intersection(
#         *[symptom_disease_mapping[disease] for disease in diseases]
#     )
#     common_symptoms -= provided_symptoms  # Exclude the already provided symptoms
#     return common_symptoms
#
# # Main function
# def predict(symptoms):
#     csv_file = "dataset.csv"  # Path to your CSV file
#     symptom_disease_mapping = build_symptom_disease_mapping(csv_file)
#
#     initial_symptoms_input = symptoms
#     provided_symptoms = set(symptom.strip() for symptom in initial_symptoms_input.split(',') if symptom.strip())
#     predicted_diseases = predict_diseases(symptom_disease_mapping, provided_symptoms)
#
#     final_results = []
#
#     if predicted_diseases:
#         print("Predicted diseases and their symptoms:")
#         for disease, symptoms in predicted_diseases.items():
#             result_string = f"{disease}, {', '.join(symptoms)}"
#             final_results.append(result_string)
#         common_symptoms = calculate_common_symptoms(symptom_disease_mapping, list(predicted_diseases.keys()), provided_symptoms)
#     else:
#         print("No diseases found matching the initial symptoms.")
#
#     return final_results


import csv

# Function to read the CSV file and build a dictionary mapping symptoms to diseases
def build_symptom_disease_mapping(csv_file):
    symptom_disease_mapping = {}
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            symptoms = [symptom.strip() for symptom in row[0].split(",") if symptom.strip()]
            disease = row[1].strip()
            if disease not in symptom_disease_mapping:
                symptom_disease_mapping[disease] = set(symptoms)
            else:
                symptom_disease_mapping[disease].update(symptoms)
    return symptom_disease_mapping

# Function to predict diseases based on user-input symptoms
def predict_diseases(symptom_disease_mapping, user_symptoms):
    predicted_diseases = {}

    for disease, symptoms in symptom_disease_mapping.items():
        if user_symptoms.issubset(symptoms):
            predicted_diseases[disease] = symptoms

    return predicted_diseases

# Function to calculate common symptoms from a list of diseases
def calculate_common_symptoms(symptom_disease_mapping, diseases, provided_symptoms):
    common_symptoms = set.intersection(
        *[symptom_disease_mapping[disease] for disease in diseases]
    )
    common_symptoms -= provided_symptoms  # Exclude the already provided symptoms
    return common_symptoms

# Main function
def predict(symptoms):
    csv_file = "dataset.csv"  # Path to your CSV file
    symptom_disease_mapping = build_symptom_disease_mapping(csv_file)

    initial_symptoms_input = symptoms
    provided_symptoms = set(symptom.strip() for symptom in initial_symptoms_input.split(',') if symptom.strip())
    predicted_diseases = predict_diseases(symptom_disease_mapping, provided_symptoms)

    unique_symptoms = set()

    if predicted_diseases:
        for disease, symptoms in predicted_diseases.items():
            unique_symptoms.update(symptoms)
        common_symptoms = calculate_common_symptoms(symptom_disease_mapping, list(predicted_diseases.keys()), provided_symptoms)
        unique_symptoms.update(common_symptoms)
    else:
        print("No diseases found matching the initial symptoms.")

    unique_symptoms -= provided_symptoms  # Remove already provided symptoms
    return list(unique_symptoms)

