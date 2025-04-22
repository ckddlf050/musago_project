drop database if exists final_project;
create database final_project;

use final_project;
-- 센서 측정 데이터

-- 1. 센서 측정 데이터 테이블
CREATE TABLE SensorData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,    -- 예: temperature, gas, noise, power
    value FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    process_id VARCHAR(20)
);

-- 2. 센서별 임계값 기준 테이블
CREATE TABLE ThresholdSetting (
    sensor_type VARCHAR(50) PRIMARY KEY,
    threshold_value FLOAT NOT NULL,
    status_if_exceeded VARCHAR(20)       -- 예: 주의, 위험
);

-- 3. 임계값 초과 이벤트 기록
CREATE TABLE ThresholdEvent (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_data_id INT,
    threshold_type VARCHAR(50),
    threshold_value FLOAT,
    actual_value FLOAT,
    status VARCHAR(10),                  -- Green, Yellow, Red
    detected_at DATETIME,
    FOREIGN KEY (sensor_data_id) REFERENCES SensorData(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 4. 에너지 소비량 기록 테이블
CREATE TABLE EnergyUsage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    process_id VARCHAR(20),
    measured_at DATETIME NOT NULL,
    consumption_kwh FLOAT NOT NULL,
    reference_kwh FLOAT
);

-- 5. 에너지 효율 등급 테이블
CREATE TABLE EfficiencyGrade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    energy_usage_id INT,
    efficiency_ratio FLOAT,
    grade VARCHAR(20),                  -- 예: High, Medium, Low
    FOREIGN KEY (energy_usage_id) REFERENCES EnergyUsage(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 6. 경고 알림 로그 테이블
CREATE TABLE AlertLog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT,
    alert_type VARCHAR(20),             -- 예: popup, sms, email
    message TEXT,
    sent_at DATETIME,
    FOREIGN KEY (event_id) REFERENCES ThresholdEvent(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 7. 사고 발생 로그 테이블
CREATE TABLE IncidentLog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT,
    description TEXT,
    recorded_at DATETIME,
    FOREIGN KEY (event_id) REFERENCES ThresholdEvent(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 8. 리포트 출력 이력 테이블
CREATE TABLE Report (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(50),            -- 예: 에너지, 사고, 안전
    created_at DATETIME,
    related_incident_id INT,
    FOREIGN KEY (related_incident_id) REFERENCES IncidentLog(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
