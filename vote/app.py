from flask import Flask, render_template, request, redirect
import psycopg2
import redis
import os

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        # Collect votes for each position
        for position in candidates.keys():
            candidate = request.form.get(position)  # Get the selected candidate for each position
            if candidate:  # Check if a candidate was selected
                redis_conn.rpush('votes', f'{position}:{candidate}')
        return redirect('/thankyou')
    return render_template('vote.html', candidates=candidates)

@app.route('/thankyou')
def thank_you():
    return "Thank you for voting!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
