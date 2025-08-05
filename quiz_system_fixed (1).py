
import mysql.connector
from datetime import datetime
import getpass

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="prasanthi@27",
    database="quizsystem"
)
cursor = conn.cursor()

def admin_login():
    username = input("Enter Admin Username: ")
    password = getpass.getpass("Enter Admin Password: ")
    cursor.execute("SELECT * FROM Admin WHERE username=%s AND password=%s", (username, password))
    return cursor.fetchone()

def add_question():
    while True:
        tech = input("Enter Technology (Python/MySQL): ").strip()
        if tech in ["Python", "MySQL"]:
            break
        else:
            print("Invalid technology. Please enter only 'Python' or 'MySQL'. Try again.")
    question = input("Enter Question: ")
    a = input("Option A: ")
    b = input("Option B: ")
    c = input("Option C: ")
    d = input("Option D: ")
    while True:
        correct = input("Correct Option (A/B/C/D): ").strip().upper()
        if correct in ["A", "B", "C", "D"]:
            break
        else:
            print("Invalid option. Choose A, B, C, or D.")

    cursor.execute("""
        INSERT INTO Questions (technology, question_text, option_a, option_b, option_c, option_d, correct_option)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (tech, question, a, b, c, d, correct))
    conn.commit()

def modify_question():
    while True:
        try:
            qid = int(input("Enter Question ID to Modify: "))
            cursor.execute("SELECT * FROM Questions WHERE question_id=%s", (qid,))
            question = cursor.fetchone()
            if question:
                break
            print("No question found with that ID. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric Question ID.")

    old_a, old_b, old_c, old_d, old_correct = question[3], question[4], question[5], question[6], question[7]

    def get_option(label, current):
        text = input(f"Option {label} [{current}]: ").strip()
        return text if text else current

    new_a = get_option("A", old_a)
    new_b = get_option("B", old_b)
    new_c = get_option("C", old_c)
    new_d = get_option("D", old_d)

    options = {"A": new_a, "B": new_b, "C": new_c, "D": new_d}
    if len(set(options.values())) < 4:
        print("Error: Options must be distinct. Aborting update.")
        return

    while True:
        new_correct = input(f"Correct Option (A/B/C/D) [{old_correct}]: ").strip().upper()
        if not new_correct:
            new_correct = old_correct
        if new_correct in options:
            break
        print("Invalid choice. Must be A, B, C, or D.")

    try:
        sql = """
            UPDATE Questions
            SET option_a=%s, option_b=%s, option_c=%s, option_d=%s, correct_option=%s
            WHERE question_id=%s
        """
        cursor.execute(sql, (new_a, new_b, new_c, new_d, new_correct, qid))
        conn.commit()
        print("Options and correct answer updated successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Failed to update: {e}")

def delete_question():
    while True:
        try:
            qid = int(input("Enter Question ID to Delete: "))
            cursor.execute("SELECT * FROM Questions WHERE question_id=%s", (qid,))
            question = cursor.fetchone()

            if question:
                cursor.execute("DELETE FROM Questions WHERE question_id=%s", (qid,))
                conn.commit()
                print("Question deleted successfully.")
                break  
            else:
                print("ID is not available. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric ID.")

def view_questions():
    cursor.execute("SELECT * FROM Questions")
    for row in cursor.fetchall():
        print(row)

def view_users():
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    
    if not users:
        print("\nNo users right now.")
    else:
        print(f"\n{'User ID':<10}{'Username':<20}{'Mobile Number':<15}", end="")
        col_count = len(users[0])
        if col_count > 3:
            print(f"{'Email':<30}", end="")
        if col_count > 4:
            print(f"{'Registered On':<20}", end="")
        print()  
        print("-" * 95)
        for row in users:
            print(f"{row[0]:<10}{row[1]:<20}{row[2]:<15}", end="")
            if col_count > 3:
                print(f"{row[3]:<30}", end="")
            if col_count > 4:
                print(f"{str(row[4]):<20}", end="")
            print()

def user_login():
    while True:
        name = input("Enter Your Name (alphabets only): ").strip()
        if name.isalpha():
            break
        else:
            print("Invalid name. Please enter alphabets only, no numbers or special characters.")

    while True:
        mobile = input("Enter Mobile Number (10 digits): ")
        if mobile.isdigit() and len(mobile) == 10:
            break
        else:
            print("Invalid mobile number. Please enter exactly 10 digits.")

    cursor.execute("INSERT INTO Users (username, mobile_number) VALUES (%s, %s)", (name, mobile))
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    return cursor.fetchone()[0]

def take_quiz(user_id):
    while True:
        tech = input("Select Technology (Python/MySQL): ").strip().capitalize()
        if tech not in ["Python", "Mysql"]:
            print("Invalid technology. Please enter 'Python' or 'MySQL'.")
            continue

        cursor.execute("SELECT * FROM Questions WHERE technology=%s", (tech,))
        questions = cursor.fetchall()

        if not questions:
            print(f"No questions found for {tech}. Please choose a different technology.")
        else:
            break  

    score = 0
    total = len(questions)

    for q in questions:
        print(f"\n{q[0]}. {q[2]}")
        print(f"A. {q[3]}\nB. {q[4]}\nC. {q[5]}\nD. {q[6]}")
        
        while True:
            answer = input("Your Answer (A/B/C/D): ").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                break
            else:
                print("Invalid input. Please enter only A, B, C, or D.")
        
        if answer == q[7].strip().upper():
            score += 1

    cursor.execute(
        "INSERT INTO Results (user_id, technology, score) VALUES (%s, %s, %s)",
        (user_id, tech, score)
    )
    conn.commit()
    
    print(f"\nQuiz Completed! You scored {score} out of {total}.")

def view_top_scores():
    cursor.execute("""
        SELECT u.username, u.mobile_number, q.technology, q.score, q.quiz_time
        FROM Results q
        JOIN Users u ON q.user_id = u.user_id
        ORDER BY q.score DESC, q.quiz_time ASC
        LIMIT 3
    """)
    
    results = cursor.fetchall()

    if not results:
        print("\nNo quiz results found.")
        return

    print("\nTop 3 Scores:")
    print(f"{'Username':<20}{'Mobile':<15}{'Technology':<15}{'Score':<10}{'Quiz Time':<20}")

    for row in results:
        username, mobile, tech, score, time = row
        print(f"{username:<20}{mobile:<15}{tech:<15}{score:<10}{str(time):<20}")

def main():
    while True:
        print("\n1. Admin Login\n2. User Login\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            if admin_login():
                while True:
                    print("\n1. Add Q\n2. Modify Q\n3. Delete Q\n4. View Q\n5. View Users\n6. Logout")
                    a_choice = input("Admin Option: ")
                    if a_choice == "1": add_question()
                    elif a_choice == "2": modify_question()
                    elif a_choice == "3": delete_question()
                    elif a_choice == "4": view_questions()
                    elif a_choice == "5": view_users()
                    elif a_choice == "6": break
            else:
                print("Invalid Admin Credentials.")
        elif choice == "2":
            user_id = user_login()
            take_quiz(user_id)
            view_top_scores()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
