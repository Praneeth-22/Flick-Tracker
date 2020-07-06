DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS lists CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;

CREATE TABLE users(
    id serial PRIMARY KEY,
    first_name VARCHAR (255) NOT NULL,
    last_name VARCHAR (255),
    email VARCHAR (255) NOT NULL UNIQUE,
    password VARCHAR (255) NOT NULL
);

CREATE TABLE lists(
    id serial PRIMARY KEY,
    list_name VARCHAR (255) NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE movies(
    id serial PRIMARY KEY,
    movie_id INTEGER NOT NULL,
    movie_title VARCHAR (255) NOT NULL,
    list_id INTEGER REFERENCES lists(id) ON DELETE CASCADE
)

CREATE TABLE sessions(
    id serial PRIMARY KEY,
    session_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
