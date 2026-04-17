class Student:
    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = marks
        self.total = self.calculate_total()
        self.percentage = self.calculate_percentage()
        self.grade = self.calculate_grade()

    def calculate_total(self):
        return sum(self.marks.values())

    def calculate_percentage(self):
        return self.total / 6

    def calculate_grade(self):
        if self.percentage >= 90:
            return "A"
        elif self.percentage >= 75:
            return "B"
        elif self.percentage >= 50:
            return "C"
        else:
            return "F"

    def to_dict(self):
        return {
            "name": self.name,
            "marks": self.marks,
            "total": self.total,
            "percentage": self.percentage,
            "grade": self.grade
        }