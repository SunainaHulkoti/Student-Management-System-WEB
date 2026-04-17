from service import StudentService
from model import Student
from auth import AuthService

def input_marks():
    subjects = ["Math", "Science", "Social", "Computer", "English", "Language"]
    marks = {}

    for sub in subjects:
        try:
            m = float(input(f"Enter marks for {sub}: "))
            if m < 0 or m > 100:
                raise ValueError("Marks must be between 0 and 100")
            marks[sub] = m
        except ValueError as e:
            print("Invalid input:", e)
            return None

    return marks


def login_system():
    auth = AuthService()

    while True:
        print("\n===== LOGIN SYSTEM =====")
        print("1. Login")
        print("2. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                username = input("Enter Student ID / Username: ").strip()
                password = input("Password: ").strip()

                user = auth.login(username, password)

                if user.get("force_change"):
                    while True:
                        new_pass = input("Enter new password: ").strip()
                        try:
                            auth.change_password(username, new_pass)
                            print("Please login again.")
                            break
                        except ValueError as e:
                            print("Error:", e)
                    continue

                return user

            elif choice == "2":
                return None

        except ValueError as e:
            print("Error:", e)


def student_menu(user):
    service = StudentService()
    auth = AuthService()

    role = user["role"]
    username = user["username"]
    student_id = user.get("student_id")

    print(f"\nWelcome {user.get('name', username)}")

    while True:
        print("\n===== MENU =====")

        if role == "admin":
            print("1. Add Student")
            print("2. View All")
            print("3. Search Student")
            print("4. Student Report")
            print("5. Sort Students")
            print("6. Update Student")
            print("7. Delete Student")
            print("8. Change Password")
            print("9. Logout")
        else:
            print("1. View My Data")
            print("2. My Report")
            print("3. Change Password")
            print("4. Logout")

        choice = input("Enter choice: ").strip()

        try:
            if role == "admin":

                if choice == "1":
                    sid = int(input("Enter ID: "))
                    name = input("Enter Name: ").strip()

                    marks = input_marks()
                    if marks is None:
                        continue

                    student = Student(sid, name, marks)
                    service.add_student(student)

                elif choice == "2":
                    service.view_students()

                elif choice == "3":
                    query = input("Enter ID or Name: ").strip()
                    service.search_student(query)

                elif choice == "4":
                    sid = int(input("Enter ID: "))
                    service.student_report(sid)
                
                elif choice == "5":
                    print("\nSort By:")
                    print("1. Name")
                    print("2. Percentage")

                    opt = input("Enter choice: ").strip()

                    if opt == "1":
                        service.sort_students("name")
                    elif opt == "2":
                        service.sort_students("percentage")
                    else:
                        print("Invalid choice")

                elif choice == "6":
                    sid = int(input("Enter ID: "))

                    if str(sid) not in service.students:
                        print("Record Not Found")
                        continue

                    old = service.students[str(sid)]

                    name = input(f"New name ({old['name']}) [Enter to skip]: ").strip()
                    if not name:
                        name = old["name"]

                    marks = {}
                    for sub, val in old["marks"].items():
                        m = input(f"{sub} ({val}) [Enter to skip]: ")
                        if m == "":
                            marks[sub] = val
                        else:
                            m = float(m)
                            if m < 0 or m > 100:
                                raise ValueError("Marks must be 0–100")
                            marks[sub] = m

                    service.update_student(sid, name, marks)

                elif choice == "7":
                    sid = int(input("Enter ID: "))
                    service.delete_student(sid)

                elif choice == "8":
                    new_pass = input("New password: ")
                    auth.change_password(username, new_pass)

                elif choice == "9":
                    break

            else:
                if choice == "1":
                    service.search_student(student_id)

                elif choice == "2":
                    service.student_report(student_id)

                elif choice == "3":
                    new_pass = input("New password: ")
                    auth.change_password(username, new_pass)

                elif choice == "4":
                    break

        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected Error:", e)


def main():
    while True:
        user = login_system()

        if user:
            student_menu(user)
        else:
            print("Exiting...")
            break


if __name__ == "__main__":
    main()