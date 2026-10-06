import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

DEPARTMENTS = [
    "Architectural Assistant-ship",
    "Automobile Engineering",
    "Civil Engineering",
    "Computer Science & Engineering",
    "Electrical Engineering",
    "Electronics & Communication Engineering",
    "Food Processing Technology",
    "Mechanical Engineering",
    "Science & Humanities",
]

PROGRAM_LEVELS = ["Diploma", "B.Tech", "M.Tech"]

STATUSES = ["Prospective Applicant", "Enrolled Student", "Alumnus"]


def generate_student_data(num_students=5):
    students = []
    for _ in range(num_students):
        program_level = random.choice(PROGRAM_LEVELS)
        status = random.choice(STATUSES)

        student = {
            "student_id": fake.uuid4(),
            "name": fake.first_name(),
            "lastname": fake.last_name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "status": status,
            "program_level": program_level,
            "department": random.choice(DEPARTMENTS),
            "year_of_study": (
                None if status == "Prospective Applicant"
                else random.choice(["1st Year", "2nd Year", "3rd Year", "4th Year"])
            ),
            "interests": random.sample(
                [
                    "Placements", "Scholarships", "Hostel/Accommodation",
                    "Admission Process", "Fee Structure", "Research Projects",
                    "Student Clubs", "Sports", "Hackathons", "Internships",
                ],
                k=random.randint(2, 5),
            ),
            "application_or_admission_year": (
                datetime.now() - timedelta(days=random.randint(1, 365 * 4))
            ).strftime("%Y"),
            "advisor_or_hod": fake.name(),
        }

        students.append(student)

    return students
