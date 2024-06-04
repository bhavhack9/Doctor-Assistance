import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def remove_disease_name(symptoms, disease):
    """Remove the disease name from the symptoms string."""
    return ','.join(symptoms.split(',', 1)[1:]).strip()

def load_and_clean_data(file_path):
    """Load data from a CSV file and clean the symptoms column."""
    df = pd.read_csv(file_path)
    df['Symptoms'] = df.apply(lambda row: remove_disease_name(row['Symptoms'], row['Disease']), axis=1)
    return df

def train_model(df):
    """Train a Multinomial Naive Bayes model on the dataset."""
    symptoms = df['Symptoms']
    diseases = df['Disease']
    symptoms_train, symptoms_test, diseases_train, diseases_test = train_test_split(symptoms, diseases, test_size=0.2, random_state=42)

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(symptoms_train)
    X_test = vectorizer.transform(symptoms_test)

    model = MultinomialNB()
    model.fit(X_train, diseases_train)

    return model, vectorizer

def predict_disease(model, vectorizer, user_input):
    """Predict the disease based on user input symptoms."""
    user_input_vectorized = vectorizer.transform([user_input])
    proba = model.predict_proba(user_input_vectorized)[0]
    most_probable_disease = model.classes_[proba.argmax()]
    probability_percentage = proba[proba.argmax()] * 100

    return most_probable_disease, probability_percentage

def predict(symptoms):
    # Load and clean data
    df = load_and_clean_data('dataset.csv')

    # Train the model
    model, vectorizer = train_model(df)

    # Get user input and predict disease
    user_input = symptoms
    predicted_disease, probability_percentage = predict_disease(model, vectorizer, user_input)

    # print("Predicted disease:", predicted_disease)
    # print("Probability for the predicted disease: {:.2f}%".format(probability_percentage))
    return predicted_disease,probability_percentage
