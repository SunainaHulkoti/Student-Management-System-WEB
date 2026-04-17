import json
from model import Student
from auth import AuthService

class StudentService:
    def __init__(self, filename="data.txt"):
        self.filename = filename
        self.students = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except:
            return {}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.students, file, indent=4)

    def add_student(self, student):
        if str(student.student_id) in self.students:
            raise ValueError("Duplicate ID not allowed")

        self.students[str(student.student_id)] = student.to_dict()
        self.save_data()

        # AUTO CREATE USER
        from auth import AuthService
        auth = AuthService()
        auth.create_user_for_student(student.student_id, student.name)

        print("Record Added Successfully")

    def view_students(self):
        if not self.students:
            print("No Records Found")
            return

        print("\n" + "="*80)
        print(f"{'ID':<5} {'Name':<15} {'Total':<10} {'%':<8} {'Grade':<6}")
        print("="*80)

        # SORT BY ID (numerically)
        sorted_data = sorted(self.students.items(), key=lambda x: int(x[0]))

        for sid, data in sorted_data:
            print(f"{sid:<5} {data['name']:<15} {data['total']:<10} {data['percentage']:<8.2f} {data['grade']:<6}")

        print("="*80)
    
    def sort_students(self, sort_by):
        if not self.students:
            print("No Records Found")
            return

        data_list = list(self.students.items())

        if sort_by == "name":
            data_list.sort(key=lambda x: x[1]["name"].lower())

        elif sort_by == "percentage":
            data_list.sort(key=lambda x: x[1]["percentage"], reverse=True)

        else:
            print("Invalid sorting option")
            return

        print("\n" + "="*80)
        print(f"{'ID':<5} {'Name':<15} {'Total':<10} {'%':<8} {'Grade':<6}")
        print("="*80)

        for sid, data in data_list:
            print(f"{sid:<5} {data['name']:<15} {data['total']:<10} {data['percentage']:<8.2f} {data['grade']:<6}")

        print("="*80)

    def search_student(self, query):
        found = False

        print("\n" + "="*60)
        print(f"{'ID':<5} {'Name':<15} {'Total':<10} {'%':<8} {'Grade':<6}")
        print("="*60)

        for sid, data in self.students.items():
            if str(query) == sid or str(query).lower() in data["name"].lower():
                print(f"{sid:<5} {data['name']:<15} {data['total']:<10} {data['percentage']:<8.2f} {data['grade']:<6}")
                found = True

        if not found:
            print("No matching record found")

        print("="*60)

    def update_student(self, student_id, name, marks):
        if str(student_id) not in self.students:
            raise ValueError("Record Not Found")

        updated = Student(student_id, name, marks)
        self.students[str(student_id)] = updated.to_dict()
        self.save_data()
        print("Record Updated Successfully")

    def delete_student(self, student_id):
        if str(student_id) not in self.students:
            raise ValueError("Record Not Found")

        del self.students[str(student_id)]
        self.save_data()

    # DELETE USER
        auth = AuthService()
        auth.delete_user(student_id)

        print("Record Deleted Successfully")

    def student_report(self, student_id):
        if str(student_id) not in self.students:
            print("Record Not Found")
            return

        data = self.students[str(student_id)]

        print("\n" + "="*50)
        print(f"STUDENT REPORT - {data['name']}")
        print("="*50)

        print(f"{'Subject':<20} {'Marks':<10}")
        print("-"*50)

        for subject, marks in data["marks"].items():
            print(f"{subject:<20} {marks:<10}")

        print("-"*50)
        print(f"{'Total':<20} {data['total']}/600")
        print(f"{'Percentage':<20} {data['percentage']:.2f}%")
        print(f"{'Grade':<20} {data['grade']}")
        print("="*50)