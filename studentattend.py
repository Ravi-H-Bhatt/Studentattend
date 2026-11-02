"""A simple command-line student attendance application."""

import json
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).with_name("attendance_data.json")


def load_data():
	if DATA_FILE.exists():
		try:
			with DATA_FILE.open("r", encoding="utf-8") as file:
				data = json.load(file)
			if isinstance(data, dict):
				return {
					"students": data.get("students", {}),
					"attendance": data.get("attendance", {}),
				}
		except (json.JSONDecodeError, OSError):
			print("Could not read saved data. Starting with an empty list.")
	return {"students": {}, "attendance": {}}


def save_data(data):
	with DATA_FILE.open("w", encoding="utf-8") as file:
		json.dump(data, file, indent=2)


def add_student(data):
	student_id = input("Student ID: ").strip()
	name = input("Student name: ").strip()
	if not student_id or not name:
		print("ID and name are required.")
	elif student_id in data["students"]:
		print("That student ID already exists.")
	else:
		data["students"][student_id] = name
		save_data(data)
		print(f"Added {name}.")


def list_students(data):
	if not data["students"]:
		print("No students have been added.")
		return
	print("\nStudents:")
	for student_id, name in sorted(data["students"].items()):
		print(f"{student_id}: {name}")


def mark_attendance(data):
	if not data["students"]:
		print("Add students before taking attendance.")
		return

	attendance_date = input(f"Date (YYYY-MM-DD, default {date.today()}): ").strip()
	attendance_date = attendance_date or date.today().isoformat()
	try:
		date.fromisoformat(attendance_date)
	except ValueError:
		print("Please enter a valid date in YYYY-MM-DD format.")
		return

	records = data["attendance"].setdefault(attendance_date, {})
	for student_id, name in sorted(data["students"].items()):
		while True:
			status = input(f"{name} ({student_id}) — present? [y/n]: ").strip().lower()
			if status in ("y", "n"):
				records[student_id] = "Present" if status == "y" else "Absent"
				break
			print("Enter y for present or n for absent.")
	save_data(data)
	print(f"Attendance saved for {attendance_date}.")


def view_attendance(data):
	attendance_date = input("Date (YYYY-MM-DD): ").strip()
	records = data["attendance"].get(attendance_date)
	if not records:
		print("No attendance records for that date.")
		return

	print(f"\nAttendance for {attendance_date}:")
	for student_id, name in sorted(data["students"].items()):
		print(f"{name} ({student_id}): {records.get(student_id, 'Not recorded')}")


def main():
	data = load_data()
	actions = {
		"1": ("Add student", add_student),
		"2": ("List students", list_students),
		"3": ("Mark attendance", mark_attendance),
		"4": ("View attendance by date", view_attendance),
	}

	while True:
		print("\nStudent Attendance")
		for key, (label, _) in actions.items():
			print(f"{key}. {label}")
		print("0. Exit")
		choice = input("Choose an option: ").strip()

		if choice == "0":
			print("Goodbye!")
			break
		action = actions.get(choice)
		if action:
			action[1](data)
		else:
			print("Invalid option. Try again.")


if __name__ == "__main__":
	main()
