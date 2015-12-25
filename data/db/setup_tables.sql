CREATE TABLE Schools (
  dbn char(6) PRIMARY KEY,
  title text,
  phone char(12),
  fax char(12),
  email text,
  shared_space boolean,
  address text,
  zip char(5),
  website text,
  total_students int,
  dress_code boolean,
  start_time datetime,
  end_time datetime,
  accessibility boolean
);

CREATE TABLE Buses (
  id int PRIMARY KEY,
  line varchar(7)
);

CREATE TABLE Trains (
  id int PRIMARY KEY,
  line int
);

CREATE TABLE School_Types(
  id int PRIMARY KEY,
  title text
);

CREATE TABLE Langs (
  id int PRIMARY KEY,
  title text
);

CREATE TABLE AP_Classes (
  id int PRIMARY KEY,
  title text
);

CREATE TABLE Xtra_Curr (
  id int PRIMARY KEY,
  title text
);

CREATE TABLE Sports (
  id int PRIMARY KEY,
  title text
);

CREATE TABLE Bus_School (
  bus_id int,
  school_dbn char(6),
  FOREIGN KEY(bus_id) REFERENCES Buses(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE Train_School (
  train_id int,
  school_dbn char(6),
  FOREIGN KEY(train_id) REFERENCES Trains(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Type_School (
  type_id int,
  school_dbn char(6),
  FOREIGN KEY(type_id) REFERENCES School_Types(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Grades (
  grade int,
  school_dbn char(6),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Lang (
  lang_id int,
  school_dbn char(6),
  FOREIGN KEY(lang_id) REFERENCES Langs(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_AP (
  class_id int,
  school_dbn char(6),
  FOREIGN KEY(class_id) REFERENCES AP_Classes(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Xtracurr (
  xtracurr_id int,
  school_dbn char(6),
  FOREIGN KEY(xtracurr_id) REFERENCES Xtra_Curr(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);

CREATE TABLE School_Sports (
  sport_id int,
  school_dbn char(6),
  psal boolean,
  gender varchar(5),
  FOREIGN KEY(sport_id) REFERENCES Sports(id),
  FOREIGN KEY(school_dbn) REFERENCES Schools(dbn)
);