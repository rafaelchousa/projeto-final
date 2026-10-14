CREATE DATABASE IF NOT EXISTS spotify
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE spotify;

CREATE TABLE IF NOT EXISTS tracks (
    track_id VARCHAR(20) PRIMARY KEY,
    track_name VARCHAR(255),
    artist_name VARCHAR(255),
    album_name VARCHAR(255),
    release_date DATE,
    genre VARCHAR(50),
    duration_ms INT,
    popularity INT,
    danceability DECIMAL(5,3),
    energy DECIMAL(5,3),
    `key` INT,
    loudness DECIMAL(6,2),
    mode TINYINT,
    instrumentalness DECIMAL(5,3),
    tempo DECIMAL(6,2),
    stream_count BIGINT,
    country VARCHAR(100),
    explicit TINYINT(1),
    label VARCHAR(100)
);
DELETE FROM tracks WHERE track_id = 'track_id';
SELECT COUNT(*) FROM tracks;
SELECT * FROM tracks;