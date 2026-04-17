# Student Management System CLI

A command-line interface for managing student records, marks, and grades. Built with Python, this system supports role-based authentication (admin and student) with comprehensive student data management features.

## Features

### Admin Features
- ✅ **Add Student** - Register new students with their marks
- ✅ **View All** - Display all student records in a formatted table
- ✅ **Search** - Find students by ID or name
- ✅ **Student Report** - View detailed report for a specific student
- ✅ **Sort Students** - Sort by name or percentage
- ✅ **Update Student** - Modify student information and marks
- ✅ **Delete Student** - Remove student records
- ✅ **Change Password** - Update admin password

### Student Features
- ✅ **View My Data** - Check personal academic records
- ✅ **My Report** - Get detailed performance report
- ✅ **Change Password** - Update student password

### Subjects Tracked
- Math
- Science
- Social
- Computer
- English
- Language

## Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Steps
1. Clone the repository:
```bash
git clone https://github.com/yourusername/student-management-system-cli.git
cd student-management-system-cli
```

2. Run the application:
```bash
python main.py
```

## Usage

### Initial Login
1. Start the application
2. Enter your Student ID/Username
3. Enter your password
4. On first login, you'll be prompted to change your default password

### Admin Dashboard
After logging in as admin, you can:
- Add new students with marks (0-100 for each subject)
- View all records in a formatted table
- Search by student ID or name
- Generate detailed reports
- Sort students by name or percentage
- Edit student information
- Delete records

### Student Dashboard
After logging in as a student, you can:
- View your academic records
- Check your performance report (total, percentage, grade)
- Change your password

## Grading System

Grades are calculated based on percentage:
- **A** : 90% and above
- **B** : 75% - 89%
- **C** : 50% - 74%
- **F** : Below 50%

## File Structure

```
├── main.py          # Main application entry point
├── auth.py          # Authentication and user management
├── model.py         # Student data model
├── service.py       # Student operations and business logic
├── users.txt        # User credentials (JSON format)
├── data.txt         # Student records (JSON format)
└── README.md        # This file
```

## Data Storage

- **users.txt** - Stores user credentials and roles
- **data.txt** - Stores all student records and their marks

Both files use JSON format for easy readability and modification.

## Security Notes

- Passwords are stored in plain text (not for production use)
- For production, implement proper password hashing (bcrypt, argon2)
- Use environment variables for sensitive data
- Implement database instead of JSON files

## Future Enhancements

- [ ] Database integration (SQL)
- [ ] Password encryption/hashing
- [ ] REST API interface
- [ ] Web UI dashboard
- [ ] Email notifications
- [ ] Backup and restore functionality
- [ ] Advanced analytics and insights
- [ ] Multi-class management

## License

This project is open source and available under the MIT License.

## Author

Created as a Student Management System CLI project.

## Support

For issues, feature requests, or contributions, please create an issue or pull request on GitHub.

---

**Note**: This is a learning project suitable for educational purposes. For production use, implement proper security measures, database integration, and error handling.
