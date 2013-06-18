CREATE TABLE intruders (
  id INTEGER PRIMARY KEY,
  surname TEXT(20),
  name TEXT(15),
  patronymic TEXT(20),
  company TEXT(20),
  post TEXT(20),
  number NUMERIC(5),
  status INTEGER
);

CREATE TABLE violation (
  id_int INTEGER,
  vdata TEXT(15),
  vtype TEXT(20),
  vww TEXT(20),
  vresume TEXT(30),
  vnote TEXT(30),
  id INTEGER PRIMARY KEY
);