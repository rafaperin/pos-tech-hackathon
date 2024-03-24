create table if not exists users (
    user_id uuid primary key,
    username varchar(60) not null,
    registration_number integer unique not null,
    password VARCHAR(64) not null,
    created_at TIMESTAMP default now(),
    modified_at TIMESTAMP default now()
);

create table if not exists time_sheets (
    record_id uuid primary key,
    registration_number integer REFERENCES users(registration_number),
    record_time TIME not null,
    record_type VARCHAR(64) not null,
    record_date DATE
);

ALTER TABLE time_sheets
ADD CONSTRAINT constraint_user_registration_number
FOREIGN KEY (registration_number)
REFERENCES users (registration_number);