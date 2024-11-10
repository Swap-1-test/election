from flask import Flask, render_template, Response
import psycopg2
import csv
import io

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
        
        # Organize results by position
        results_dict = {}
        for position, candidate, votes in results:
            if position not in results_dict:
                results_dict[position] = []
            results_dict[position].append((candidate, votes))
        
        return render_template('result.html', results=results_dict)
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/details')
def details():
    try:
        db_cursor.execute("ROLLBACK")  # Clears any failed transaction
        db_cursor.execute("SELECT DISTINCT full_name, prn FROM votes WHERE full_name IS NOT NULL AND prn IS NOT NULL")
        voters = db_cursor.fetchall()
        return render_template('details.html', voters=voters)
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/download_results')
def download_results():
    try:
        db_cursor.execute("SELECT position, candidate, COUNT(*) FROM votes GROUP BY position, candidate")
        results = db_cursor.fetchall()
        
        # Create CSV file in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Position', 'Candidate', 'Votes'])  # header row
        for row in results:
            writer.writerow(row)
        
        output.seek(0)
        return Response(output.getvalue(),
                        mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=vote_counts.csv"})
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/download_voters')
def download_voters():
    try:
        db_cursor.execute("SELECT DISTINCT full_name, prn FROM votes WHERE full_name IS NOT NULL AND prn IS NOT NULL")
        voters = db_cursor.fetchall()
        
        # Create CSV file in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Full Name', 'PRN'])  # header row
        for voter in voters:
            writer.writerow(voter)
        
        output.seek(0)
        return Response(output.getvalue(),
                        mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=voter_details.csv"})
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
