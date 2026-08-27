-- many-to-one relationship (many students -> one room)
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    sex CHAR(1) NOT NULL CHECK(sex in ('M', 'F')),
    room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE RESTRICT
);