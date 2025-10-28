import 
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Agify and Genderize API URLs
AGIFY_API_URL = "https://api.agify.io"
GENDERIZE_API_URL = "https://api.genderize.io"

@app.route('/')
def home():
    return render_template('index.html')  # Render the front-end template

@app.route('/predict', methods=['POST'])
def predict():
    name = request.form.get('name')  # Get the name from the form input

    if not name:
        return render_template('index.html', error="Name is required!")  # Show an error if no name is entered

    # Fetch predicted age from Agify API
    agify_response = requests.get(AGIFY_API_URL, params={"name": name})
    if agify_response.status_code != 200:
        return jsonify({"error": "Failed to fetch age prediction"}), 500

    agify_data = agify_response.json()
    predicted_age = agify_data.get("age", "N/A")

    # Fetch predicted gender from Genderize API
    genderize_response = requests.get(GENDERIZE_API_URL, params={"name": name})
    if genderize_response.status_code != 200:
        return jsonify({"error": "Failed to fetch gender prediction"}), 500

    genderize_data = genderize_response.json()
    predicted_gender = genderize_data.get("gender", "N/A")

    # Render the result on the same page
    return render_template('index.html', name=name, predicted_age=predicted_age, predicted_gender=predicted_gender)

if __name__ == '__main__':
    app.run(debug=True)
