CREATE TABLE IF NOT EXISTS users (
    id               SERIAL PRIMARY KEY,
    name             TEXT NOT NULL UNIQUE,
    password         TEXT NOT NULL,
    joinedDate       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    university       TEXT NOT NULL,
    educationGroup   TEXT DEFAULT NULL,
    groupRole        TEXT NOT NULL,
    isConfirmed      BOOLEAN DEFAULT FALSE,
    avatarUrl        TEXT DEFAULT NULL,
    email            TEXT DEFAULT NULL UNIQUE,
    isAdmin          BOOLEAN DEFAULT FALSE
    --posts []
);

CREATE TABLE IF NOT EXISTS posts (
    id             SERIAL PRIMARY KEY,
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    createdDate    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    privacy        TEXT NOT NULL,
    author         SERIAL NOT NULL REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS calendars (
    id             SERIAL PRIMARY KEY,
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    --lessons []
    --events []
    createdDate    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    privacy        TEXT NOT NULL,
    author         SERIAL NOT NULL REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS events (
    id             SERIAL PRIMARY KEY,
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    date           TIMESTAMP WITH TIME ZONE NOT NULL,
    type           TEXT NOT NULL,
    --participants []
    createdDate    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    privacy        TEXT NOT NULL,
    author         SERIAL NOT NULL REFERENCES users(id),
    calendar       SERIAL REFERENCES calendars(id)
);

CREATE TABLE IF NOT EXISTS lessons (
    id             SERIAL PRIMARY KEY,
    title          TEXT NOT NULL,
    teacherName    TEXT DEFAULT NULL,
    type           TEXT NOT NULL,
    start          TIMESTAMP WITH TIME ZONE NOT NULL,
    "end"          TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    userId   SERIAL NOT NULL REFERENCES users(id),
    token    TEXT NOT NULL,
    expires  TIMESTAMP WITH TIME ZONE
);