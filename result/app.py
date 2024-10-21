from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Database connection setup
conn = psycopg2.connect("dbname='voting_db' user='user' host='db' password='password'")
db_cursor = conn.cursor()

@app.route('/')
def result():
    try:
        db_cursor.execute("ROLLBACK")  # Clears any failed transaction
        db_cursor.execute("SELECT position, candidate, COUNT(*) FROM votes GROUP BY position, candidate")
        results = db_cursor.fetchall()
        return render_template('result.html', results=results)
    except Exception as e:
        return f"Error: {e}", 500

# Route to display details of students who voted
@app.route('/details')
def details():
    try:
        db_cursor.execute("ROLLBACK")  # Clears any failed transaction
        db_cursor.execute("SELECT DISTINCT full_name, prn FROM votes WHERE full_name IS NOT NULL AND prn IS NOT NULL")
        voters = db_cursor.fetchall()
        return render_template('details.html', voters=voters)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
