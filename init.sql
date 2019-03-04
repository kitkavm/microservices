drop table IF EXISTS users;
drop table IF EXISTS articles;

create TABLE  IF NOT EXISTS users(
	Id INTEGER PRIMARY KEY ASC,
	username TEXT,
	password TEXT
);

create TABLE IF NOT EXISTS articles(
	Id INTEGER PRIMARY KEY ASC,
	article_Id INTEGER,
	article_title TEXT,
	article_author TEXT,
	creation_timestamp TEXT,
	last_modified_timestap TEXT,
	FOREIGN KEY (article_author) REFERENCES users(id)
);


insert into users (username, password) values ('a', 'password');
insert into users (username, password) values ('b', 'password');
insert into users (username, password) values ('c', 'password');
insert into users (username, password) values ('d', 'password');
insert into users (username, password) values ('e', 'password');
insert into users (username, password) values ('kavit', '12345');
insert into users (username, password) values ('kevin', '12345');