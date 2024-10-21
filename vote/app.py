from flask import Flask, render_template, request, redirect, session, flash
import psycopg2
import redis
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Connect to PostgreSQL
db_conn = psycopg2.connect(os.environ['DATABASE_URL'])
db_cursor = db_conn.cursor()

# Connect to Redis
redis_conn = redis.StrictRedis.from_url(os.environ['REDIS_URL'])

# Candidates for the election
candidates = {
    'president': ['Candidate A1', 'Candidate A2'],
    'vice_president': ['Candidate B1', 'Candidate B2'],
    'secretary': ['Candidate C1', 'Candidate C2'],
    'treasurer': ['Candidate D1', 'Candidate D2']
}
# Function to create the votes table if it doesn't exist
def create_votes_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        position VARCHAR(50),
        candidate VARCHAR(100),
        full_name VARCHAR(100),
        prn VARCHAR(50)
    );
    '''
    db_cursor.execute(create_table_query)
    db_conn.commit()

# Call the function to create the table when the app starts
create_votes_table()



# Authentication page route
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        full_name = request.form['full_name']
        prn = request.form['prn']

        # Store the voter's full name and PRN in the session
        session['full_name'] = full_name
        session['prn'] = prn

        # Redirect to the voting page
        return redirect('/')

    return render_template('auth.html')

# Voting page route
@app.route('/', methods=['GET', 'POST'])
def vote():
    if 'full_name' not in session or 'prn' not in session:
        # If the user hasn't authenticated, redirect to the authentication page
        return redirect('/auth')

    if request.method == 'POST':
        prn = session['prn']
        
        # Check if the user has already voted by querying PostgreSQL
        db_cursor.execute("SELECT COUNT(*) FROM votes WHERE prn = %s", (prn,))
        vote_count = db_cursor.fetchone()[0]

        if vote_count > 0:
            flash('You have already voted!', 'error')
            return redirect('/thankyou')

        # Collect votes for each position
        votes_inserted = 0  # Count the number of successful votes inserted
        for position in candidates.keys():
            candidate = request.form.get(position)  # Get the selected candidate for each position
            if candidate:  # Check if a candidate was selected
                # Insert vote into PostgreSQL along with voter's name and PRN
                db_cursor.execute(
                    "INSERT INTO votes (position, candidate, full_name, prn) VALUES (%s, %s, %s, %s)",
                    (position, candidate, session['full_name'], session['prn'])
                )
                votes_inserted += 1

        if votes_inserted > 0:
            db_conn.commit()  # Save changes to the database

        return redirect('/thankyou')

    return render_template('vote.html', candidates=candidates)

# Thank you page route
@app.route('/thankyou')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
