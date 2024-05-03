SET max_parallel_maintenance_workers TO 80;
SET maintenance_work_mem TO '16 GB';

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER
);

CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

create table messages (
    id BIGSERIAL primary key,
    sender_id integer not null REFERENCES users(id),
    message text not null,
    created_at timestamp not null default current_timestamp,
    id_urls INTEGER REFERENCES urls(id_urls)
);

--ALTER TABLE messages ADD COLUMN tsv tsvector;
--set default_text_search_config = default;
--update messages set tsv = to_tsvector(message);

CREATE TABLE fts_word (
    word text PRIMARY KEY
);

CREATE EXTENSION IF NOT EXISTS RUM;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

--CREATE INDEX idx_fts_word ON fts_word USING GIN(word gin_trgm_ops);

--CREATE INDEX are_credentials_good_create_message_account_deleted ON users(username, password, id);
CREATE INDEX retrieve_messages ON messages(created_at, id, sender_id, message);
--CREATE INDEX retrieve_messages2 ON users(id, username, password, age);
CREATE INDEX query_messages2 ON messages USING RUM(to_tsvector('english', message));
