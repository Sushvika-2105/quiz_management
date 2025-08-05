# quiz_management
A command-line based quiz application developed using **Python** and **MySQL**, designed to facilitate dynamic quiz-taking experiences and efficient user management. The system supports both **admin** and **user** roles with database-driven functionality and real-time score tracking.

---

## 🚀 Features

- **Admin Panel**
  - Add, modify, and delete quiz questions by technology.
  - Secure login with input validation.
  - View registered users and quiz database.

- **User Mode**
  - Register with name and mobile number.
  - Take quizzes based on chosen technology (Python / MySQL).
  - Auto-score calculation and result storage.

- **Database Integration**
  - MySQL-backed accurate data storage.
  - Transaction-safe operations using SQL constraints and commits.
  - Result leaderboard with top performers and timestamps.

---

## 🛠️ Technologies Used

- **Python 3.x**
- **MySQL (via `mysql-connector-python`)**
- Command Line Interface (CLI)
- SQL for relational data modeling

---

## 📂 Project Structure

```plaintext
quizsystem/
├── main.py                  # Core application logic
├── database_schema.sql      # MySQL table definitions
├── README.md                # Project documentation
