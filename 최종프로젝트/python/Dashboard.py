import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem, QSizePolicy, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt

import os
import subprocess
import time

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False


class RealtimePredictDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("실시간 예측 통합 대시보드")
        self.setGeometry(200, 200, 1300, 750)

        self.index = 0
        self.max_rows = 0
        self.main_process = None

        # 모든 예측 결과 파일 경로
        base_path = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data"
        self.sensor_path = os.path.join(base_path, "sensor_result.csv")
        self.prediction_paths = {
            "이상치 탐지": os.path.join(base_path, "anomaly_prediction.csv")
        }

        self.sensor_df = pd.DataFrame()
        self.predictions = {}

        # 레이아웃 구성
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("🔍 실시간 센서 및 예측 대시보드")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        # 실행/정지 버튼
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶ 실행")
        self.stop_btn = QPushButton("■ 종료")
        self.start_btn.clicked.connect(self.start_stream)
        self.stop_btn.clicked.connect(self.stop_stream)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.sensor_tab = None
        self.prediction_tabs = {}

        # 타이머 (초기 정지 상태)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_tables)

    def load_data(self):
        self.sensor_df = pd.read_csv(self.sensor_path, encoding="utf-8-sig")
        self.max_rows = len(self.sensor_df)

        for key, path in self.prediction_paths.items():
            self.predictions[key] = pd.read_csv(path, encoding="utf-8-sig")

    def start_stream(self):
        self.index = 0
        print("▶ 예측 메인 자동화 스크립트 실행 중...")

        # 예측 메인 스크립트 실행
        self.main_process = subprocess.Popen(
            ["python", "C:/Users/user/Desktop/최종프로젝트/python/main_auto_predictor.py"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # 센서 결과 생성 기다리기
        while not os.path.exists(self.sensor_path):
            print("⏳ 센서 데이터 준비 대기 중...")
            time.sleep(0.5)

        # 데이터 로드
        self.load_data()

        # UI 탭 구성
        self.tabs.clear()
        self.sensor_tab = self.create_tab(self.sensor_df.columns.tolist(), "센서 데이터")
        self.tabs.addTab(self.sensor_tab["widget"], "센서 데이터")

        self.prediction_tabs = {}
        for label, df in self.predictions.items():
            columns = df.columns.tolist()
            tab = self.create_tab(columns, label)
            self.tabs.addTab(tab["widget"], label)
            self.prediction_tabs[label] = tab

        self.timer.start(1000)
        print("✅ 실시간 시각화 시작됨")

    def stop_stream(self):
        self.timer.stop()
        if self.main_process:
            self.main_process.terminate()
            self.main_process = None
        print("■ 스트리밍 및 메인 프로세스 종료")

    def create_tab(self, columns, label):
        tab_widget = QWidget()
        layout = QVBoxLayout()
        tab_widget.setLayout(layout)

        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.verticalHeader().setVisible(False)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(table)

        figure = Figure(figsize=(8, 3))
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        return {"widget": tab_widget, "table": table, "figure": figure, "canvas": canvas, "columns": columns, "label": label}

    def update_tables(self):
        if self.index >= self.max_rows:
            self.timer.stop()
            print("⏹ 모든 데이터 출력 완료")
            return

        sensor_row = self.sensor_df.iloc[self.index]
        self.append_row(self.sensor_tab["table"], sensor_row)
        self.update_plot(self.sensor_tab["figure"], self.sensor_df.iloc[:self.index+1], "timestamp", self.sensor_df.columns[1])

        for label, df in self.predictions.items():
            row = df.iloc[self.index]
            tab = self.prediction_tabs[label]
            self.append_row(tab["table"], row)
            col_name = tab["columns"][-1]
            self.update_plot(tab["figure"], df.iloc[:self.index+1], df.columns[0], col_name)

        self.index += 1

    def append_row(self, table, row_data):
        row_idx = table.rowCount()
        table.insertRow(row_idx)
        for col_idx, val in enumerate(row_data):
            table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def update_plot(self, fig, df, x_col, y_col):
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(pd.to_datetime(df[x_col]), df[y_col], label=y_col)
        ax.set_title(f"{y_col} 실시간 추이")
        ax.set_xlabel("시간")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        ax.legend()
        fig.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = RealtimePredictDashboard()
    dashboard.show()
    sys.exit(app.exec_())