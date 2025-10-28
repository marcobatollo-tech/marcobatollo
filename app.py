from flask import Flask, jsonify, request

app = Flask(__name__)

# Empty data store for students
students_data = {}

@app.route('/')
def home():
    return "🎓 Welcome to the Student Schedule Management System API!"

# -------------------------------------------------
# 1️⃣ STUDENT MANAGEMENT ROUTES
# -------------------------------------------------

# Get all students
@app.route('/students', methods=['GET'])
def get_all_students():
    if not students_data:
        return jsonify({"message": "No students found"}), 200
    return jsonify(list(students_data.values())), 200

# Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    required_fields = ["name", "grade", "section"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    name_key = data["name"].lower()

    if name_key in students_data:
        return jsonify({"error": "Student already exists"}), 400

    students_data[name_key] = {
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"],
        "schedule": []
    }

    return jsonify({"message": "Student added successfully"}), 201

# Get a specific student's data
@app.route('/student/<student_name>', methods=['GET'])
def get_student(student_name):
    student = students_data.get(student_name.lower())
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200

# Delete a student entirely
@app.route('/student/<student_name>', methods=['DELETE'])
def delete_student(student_name):
    student_name = student_name.lower()
    if student_name not in students_data:
        return jsonify({"error": "Student not found"}), 404
    del students_data[student_name]
    return jsonify({"message": "Student deleted successfully"}), 200

# -------------------------------------------------
# 2️⃣ SCHEDULE MANAGEMENT ROUTES
# -------------------------------------------------

# Get a student's schedule
@app.route('/student/<student_name>/schedule', methods=['GET'])
def get_schedule(student_name):
    student = students_data.get(student_name.lower())
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student["schedule"]), 200

# Add a schedule entry for a student
@app.route('/student/<student_name>/schedule', methods=['POST'])
def add_schedule(student_name):
    student = students_data.get(student_name.lower())
    if not student:
        return jsonify({"error": "Student not found"}), 404

    new_schedule = request.get_json()
    required_fields = ["day", "subject", "time"]

    if not all(field in new_schedule for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    student["schedule"].append(new_schedule)
    return jsonify({"message": "Schedule added successfully"}), 201

# Update a schedule entry
@app.route('/student/<student_name>/schedule', methods=['PUT'])
def update_schedule(student_name):
    student = students_data.get(student_name.lower())
    if not student:
        return jsonify({"error": "Student not found"}), 404

    updated_schedule = request.get_json()
    required_fields = ["day", "subject", "time"]
    if not all(field in updated_schedule for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    for item in student["schedule"]:
        if item["day"] == updated_schedule["day"] and item["subject"] == updated_schedule["subject"]:
            item["time"] = updated_schedule["time"]
            return jsonify({"message": "Schedule updated successfully"}), 200

    return jsonify({"error": "Schedule entry not found"}), 404

# Delete a schedule entry
@app.route('/student/<student_name>/schedule', methods=['DELETE'])
def delete_schedule(student_name):
    student = students_data.get(student_name.lower())
    if not student:
        return jsonify({"error": "Student not found"}), 404

    schedule_to_delete = request.get_json()
    if not schedule_to_delete or "day" not in schedule_to_delete or "subject" not in schedule_to_delete:
        return jsonify({"error": "Missing 'day' or 'subject'"}), 400

    for idx, item in enumerate(student["schedule"]):
        if item["day"] == schedule_to_delete["day"] and item["subject"] == schedule_to_delete["subject"]:
            student["schedule"].pop(idx)
            return jsonify({"message": "Schedule deleted successfully"}), 200

    return jsonify({"error": "Schedule entry not found"}), 404


# -------------------------------------------------
# Run the Flask app
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
