CREATE TABLE alumni (
    id INTEGER NOT NULL PRIMARY KEY,
    year INTEGER NOT NULL,
    last TEXT NOT NULL,
    first TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL, 
    state TEXT NOT NULL,
    zip INTEGER NOT NULL,
    email TEXT NOT NULL,
    alt_email TEXT NOT NULL,
    cell INTEGER NOT NULL,
    home INTEGER NOT NULL,
    employer TEXT NOT NULL,
    emp_address TEXT NOT NULL,
    update_date TEXT NOT NULL
);

CREATE TABLE latlong (
    id INTEGER NOT NULL PRIMARY KEY,
    alumni_id INTEGER NOT NULL,
    lat NUMERIC NOT NULL,
    lng NUMERIC NOT NULL,
    FOREIGN KEY (alumni_id) REFERENCES alumni (id)
);
