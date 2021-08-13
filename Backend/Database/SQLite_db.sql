CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
nickname text NOT NULL UNIQUE,
email text NOT NULL UNIQUE,
password text NOT NULL,
avatar BLOB DEFAULT NULL,
time integer NOT NULL
);