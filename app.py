from flask import Flask, render_template, request, redirect, session
from service import StudentService
from auth import AuthService
from model import Student

app = Flask(__name__)
app.secret_key = "secret123"

service = StudentService()
auth = AuthService()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        try:
            username = request.form["username"].strip()
            password = request.form["password"].strip()

            if not username or not password:
                raise ValueError("All fields are required")

            auth.users = auth.load_users()   # reload latest data
            user = auth.login(username, password)
            session["user"] = user

            if user["role"] == "user" and user.get("force_change"):
                return redirect("/force_change")

            return redirect("/dashboard")

        except ValueError as e:
            error = str(e)
        except Exception:
            error = "Unexpected error occurred"

    return render_template("login.html", error=error)


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    user = session["user"]

    if user["role"] == "user" and user.get("force_change"):
        return redirect("/force_change")

    return render_template("dashboard.html", user=user)


# ---------------- ADD STUDENT ----------------
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect("/dashboard")

    error = None

    if request.method == "POST":
        try:
            sid = request.form["id"].strip()
            name = request.form["name"].strip()

            if not sid or not name:
                raise ValueError("ID and Name cannot be empty")

            sid = int(sid)

            subjects = ["math", "science", "social", "computer", "english", "language"]
            marks = {}

            for sub in subjects:
                val = request.form[sub].strip()

                if not val:
                    raise ValueError(f"{sub.capitalize()} cannot be empty")

                val = float(val)

                if val < 0 or val > 100:
                    raise ValueError(f"{sub.capitalize()} must be 0–100")

                marks[sub.capitalize()] = val

            student = Student(sid, name, marks)
            service.add_student(student)

            return redirect("/view")

        except ValueError as e:
            error = str(e)
        except Exception:
            error = "Something went wrong"

    return render_template("add_student.html", error=error)


# ---------------- VIEW ----------------
@app.route("/view")
def view_students():
    if "user" not in session:
        return redirect("/")

    if session["user"]["role"] != "admin":
        return redirect("/dashboard")

    students = sorted(service.students.items(), key=lambda x: int(x[0]))
    return render_template("view_students.html", students=students, user=session["user"])


# ---------------- SEARCH ----------------
@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect("/")

    if session["user"]["role"] != "admin":
        return redirect("/dashboard")

    results = []
    error = None

    if request.method == "POST":
        try:
            query = request.form["query"].strip()

            if not query:
                raise ValueError("Search cannot be empty")

            for sid, data in service.students.items():
                if query == sid or query.lower() in data["name"].lower():
                    results.append((sid, data))

        except ValueError as e:
            error = str(e)

    return render_template("search.html", results=results, error=error)


# ---------------- UPDATE ----------------
@app.route("/update/<sid>", methods=["GET", "POST"])
def update_student(sid):
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect("/dashboard")

    data = service.students.get(str(sid))
    error = None

    if request.method == "POST":
        try:
            name = request.form["name"].strip() or data["name"]

            marks = {}
            for sub, old_val in data["marks"].items():
                val = request.form[sub].strip()

                if val == "":
                    marks[sub] = old_val
                else:
                    val = float(val)
                    if val < 0 or val > 100:
                        raise ValueError(f"{sub} must be 0–100")
                    marks[sub] = val

            service.update_student(int(sid), name, marks)
            return redirect("/view")

        except ValueError as e:
            error = str(e)
        except Exception:
            error = "Update failed"

    return render_template("update.html", sid=sid, data=data, error=error)


# ---------------- DELETE ----------------
@app.route("/delete/<sid>")
def delete_student(sid):
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect("/dashboard")

    try:
        service.delete_student(int(sid))
    except Exception:
        pass

    return redirect("/view")


# ---------------- SORT ----------------
@app.route("/sort", methods=["GET", "POST"])
def sort_students():
    if "user" not in session:
        return redirect("/")

    if session["user"]["role"] != "admin":
        return redirect("/dashboard")

    if request.method == "POST":
        criteria = request.form.get("criteria")

        students = list(service.students.items())

        if criteria == "name":
            students.sort(key=lambda x: x[1]["name"].lower())
        elif criteria == "percentage":
            students.sort(key=lambda x: x[1]["percentage"], reverse=True)

        return render_template("view_students.html", students=students, user=session["user"])

    return render_template("sort.html")


# ---------------- REPORT ----------------
@app.route("/report/<sid>")
def report(sid):
    if "user" not in session:
        return redirect("/")

    user = session["user"]

    if user["role"] == "user" and str(user["student_id"]) != sid:
        return redirect("/dashboard")

    data = service.students.get(str(sid))
    if not data:
        return "Student not found", 404

    # 📊 STATS
    avg = data["total"] / len(data["marks"])
    high = max(data["marks"].values())
    low = min(data["marks"].values())

    return render_template(
        "report.html",
        data=data,
        sid=sid,
        avg=avg,
        high=high,
        low=low
    )


# ---------------- CHANGE PASSWORD ----------------
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect("/")

    error = None

    if request.method == "POST":
        try:
            new_pass = request.form["password"].strip()

            if not new_pass:
                raise ValueError("Password cannot be empty")

            auth.change_password(session["user"]["username"], new_pass)
            return redirect("/dashboard")

        except ValueError as e:
            error = str(e)

    return render_template("change_password.html", error=error)


# ---------------- FORCE CHANGE ----------------
@app.route("/force_change", methods=["GET", "POST"])
def force_change():
    if "user" not in session:
        return redirect("/")

    user = session["user"]

    if user["role"] != "user" or not user.get("force_change"):
        return redirect("/dashboard")

    error = None

    if request.method == "POST":
        try:
            new_pass = request.form["password"].strip()

            if not new_pass:
                raise ValueError("Password cannot be empty")

            auth.change_password(user["username"], new_pass)
            user["force_change"] = False
            session["user"] = user

            return redirect("/dashboard")

        except ValueError as e:
            error = str(e)

    return render_template("force_change.html", error=error)

# ---------------- RESET PASSWORD ----------------

@app.route("/reset/<username>")
def reset_password(username):
    if "user" not in session:
        return redirect("/")

    # Only admin allowed
    if session["user"]["role"] != "admin":
        return redirect("/dashboard")

    try:
        auth.reset_password(username)
        return redirect("/view")
    except Exception as e:
        return f"Error: {e}"

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)