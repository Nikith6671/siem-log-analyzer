create table logs (
    id serial primary key,
    timestamp timestamp,
    level varchar(10),
    message text
);

create table users (
    id serial primary key,
    username varchar(50),
    password text,
    role varchar(20)
);