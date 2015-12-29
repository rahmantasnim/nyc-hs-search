CREATE TABLE Schools (
  dbn char(6) PRIMARY KEY,
  title text,
  phone char(12),
  fax char(12),
  email text,
  shared_space boolean,
  address text,
  zip INTEGER,
  website text,
  total_students INTEGER,
  dress_code boolean,
  start_time datetime,
  end_time datetime,
  accessibility boolean
);

CREATE TABLE Buses (
  id INTEGER PRIMARY KEY,
  title varchar(7)
);

CREATE TABLE Trains (
  id INTEGER PRIMARY KEY,
  title varchar(3)
);

CREATE TABLE School_Types(
  id INTEGER PRIMARY KEY,
  title text
);

CREATE TABLE Langs (
  id INTEGER PRIMARY KEY,
  title text
);

CREATE TABLE AP_Classes (
  id INTEGER PRIMARY KEY,
  title text
);

CREATE TABLE Xtra_Curr (
  id INTEGER PRIMARY KEY,
  title text
);

CREATE TABLE Sports (
  id INTEGER PRIMARY KEY,
  title text
);

CREATE TABLE Bus_School (
  bus_id INTEGER,
  school_dbn char(6),
  FOREIGN KEY(bus_id) REFERENCES Buses(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE Train_School (
  train_id INTEGER,
  school_dbn char(6),
  stop text,
  FOREIGN KEY(train_id) REFERENCES Trains(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Type_School (
  type_id INTEGER,
  school_dbn char(6),
  FOREIGN KEY(type_id) REFERENCES School_Types(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Grades (
  grade INTEGER,
  school_dbn char(6),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Lang (
  lang_id INTEGER,
  school_dbn char(6),
  FOREIGN KEY(lang_id) REFERENCES Langs(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_AP (
  class_id INTEGER,
  school_dbn char(6),
  FOREIGN KEY(class_id) REFERENCES AP_Classes(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Xtracurr (
  xtracurr_id INTEGER,
  school_dbn char(6),
  FOREIGN KEY(xtracurr_id) REFERENCES Xtra_Curr(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Sports (
  sport_id INTEGER,
  school_dbn char(6),
  psal boolean,
  gender char(1),
  FOREIGN KEY(sport_id) REFERENCES Sports(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);