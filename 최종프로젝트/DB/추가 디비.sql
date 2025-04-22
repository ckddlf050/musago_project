

USE musago_db;

CREATE TABLE IF NOT EXISTS event_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    humidity FLOAT,
    co2 FLOAT,
    vibration FLOAT,
    energy_usage FLOAT,
    risk_prediction VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS fault_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    vibration FLOAT,
    fault_prediction VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS risk_level_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    humidity FLOAT,
    co2 FLOAT,
    vibration FLOAT,
    energy_usage FLOAT,
    risk_level_prediction VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS anomaly_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    temperature FLOAT,
    humidity FLOAT,
    co2 FLOAT,
    vibration FLOAT,
    energy_usage FLOAT,
    anomaly_prediction VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS energy_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    energy_usage FLOAT,
    energy_prediction VARCHAR(10)
);
