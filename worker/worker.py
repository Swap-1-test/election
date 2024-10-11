import redis
import psycopg2
import os

redis_conn = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
db_conn = psycopg2.connect(os.environ['DATABASE_URL'])
db_cursor = db_conn.cursor()

def save_vote(position, candidate):
    db_cursor.execute("INSERT INTO votes (position, candidate) VALUES (%s, %s)", (position, candidate))
    db_conn.commit()

while True:
    vote = redis_conn.blpop('votes')[1].decode('utf-8')
    position, candidate = vote.split(':')
    save_vote(position, candidate)
