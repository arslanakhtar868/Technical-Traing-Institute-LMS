from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import hashlib

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Firebase Configuration - Load from JSON file (Download from Firebase Console)
cred = credentials.Certificate(r"C:\Users\SADEED\PycharmProjects\PythonProject\training-institute-firebase.json")  # Place your Firebase private key JSON here
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://training-institute-90eb3-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
})


@app.route("/")
def home():
    return render_template("index_page.html")


# Route to render the signup page
@app.route('/signup')
def signup_page():
    return render_template("signup.html")

# Route to handle form submission
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        name = data.get("name")
        course = data.get("course")
        address = data.get("address")
        password = data.get("password")

        if not name or not course or not address or not password:
            return jsonify({"status": "error", "message": "All fields are required!"}), 400

        # Encrypt password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save data to Firebase Realtime Database
        user_ref = db.reference('users').push()
        user_ref.set({
            "name": name,
            "course": course,
            "address": address,
            "password": hashed_password  # Store encrypted password
        })

        return jsonify({"status": "success", "message": "Signup successful!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
