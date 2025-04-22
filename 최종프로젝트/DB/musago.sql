-- 1. 데이터베이스 생성 (한 번만 실행)
CREATE DATABASE IF NOT EXISTS musago_db;
USE musago_db;

-- 2. 기존 테이블 삭제 (있다면)
DROP TABLE IF EXISTS sensor_data;

-- 3. sensor_data 테이블 새로 생성
CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    gas FLOAT,
    power FLOAT,
    sound FLOAT,
    risk TEXT
);
CREATE TABLE IF NOT EXISTS event_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    gas FLOAT,
    power FLOAT,
    sound FLOAT,
    risk TEXT
);

CREATE TABLE IF NOT EXISTS efficiency_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    predicted_power FLOAT,
    actual_power FLOAT,
    efficiency_ratio FLOAT, -- 예측 대비 효율 (%)
    efficiency_grade VARCHAR(10), -- High / Medium / Low
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

