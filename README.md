docker exec -it election_db_1 psql -U user -d voting_db
_________________________________________________________\
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    position VARCHAR(50),
    candidate VARCHAR(100),
    full_name VARCHAR(100),
    prn VARCHAR(50)
);
______________________________________________________________\
SELECT * FROM votes;
____________________________________________________________\

