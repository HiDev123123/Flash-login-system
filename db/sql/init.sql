
--  Delete table syntext: DROP TABLE IF EXISTS admin;
-- DROP TABLE IF EXISTS student;


CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dob DATE,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    class TEXT,
    password TEXT,
    roll TEXT
);



CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL ,
    phone INTEGER NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    dob DATE,
    password text
);

-- -- alter query
-- ALTER TABLE admin ADD COLUMN role TEXT DEFAULT 'admin';
-- ALTER TABLE student ADD COLUMN role TEXT DEFAULT 'student';



-- insert queery
-- INSERT INTO admin (name, phone, email, dob, password)
-- VALUES
--     ('John Doe', 100, 'johndoe@example.com', '1990-01-01', '100'),
--     ('Jane Smith', 101, 'janesmith@example.com', '1985-05-15', '101');