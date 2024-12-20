Redis (election_redis_1):

Image: redis:alpine
🚀 Role: Redis is used for caching or queuing tasks in the voting system.
🔌 Port: 6379/tcp

____________________________________________________________________________________________________________________
Vote App (election_vote-app_1):

Image: election_vote-app
🗳️ Role: A Python-based web application that allows users to vote.
🌍 Port: 5000 (Exposed to 0.0.0.0:3000)

____________________________________________________________________________________________________________________
PostgreSQL Database (election_db_1):

Image: postgres:latest
💾 Role: PostgreSQL is used to store votes and election-related data.
🔒 Port: 5432/tcp

____________________________________________________________________________________________________________________
Result App (election_result-app_1):

Image: election_result-app
📊 Role: A Python web application that processes and displays the results of the election.
🌍 Port: 5001 (Exposed to 0.0.0.0:3001)

____________________________________________________________________________________________________________________
Worker (election_worker_1):

Image: election_worker
🛠️ Role: A background worker that performs various tasks asynchronously (e.g., processing votes, sending emails, etc.).
🔄 No exposed ports as it runs in the background.

____________________________________________________________________________________________________________________
How to Run:
Docker Compose:
This project is designed to be run using Docker Compose. To get started, simply run:

docker-compose build
docker-compose up
____________________________________________________________________________________________________________________
Ports:

The Vote App is accessible on http://localhost:3000 🌐.
The Result App is accessible on http://localhost:3001 📈.
Redis and PostgreSQL are running in the background and do not require direct access unless you need to connect to them for troubleshooting or development purposes.

________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
Services:

🗳️ election_vote-app_1 handles user voting.
📊 election_result-app_1 displays election results.
🛠️ election_worker_1 processes background tasks.
💾 election_db_1 stores the election data (votes, user details).
🚀 election_redis_1 helps with caching or queuing.

____________________________________________________________________________________________________________________
Technologies:
🐳 Docker: To containerize the services and run them in isolated environments.
🐍 Python: For the backend logic of the apps and worker.
🚀 Redis: For task queuing or caching.
💾 PostgreSQL: For persistent data storage.
________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
To check the database entry
docker exec -it election_db_1 psql -U user -d voting_db
______________________________________________________

