#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <sstream>
#include <iomanip>
#include <direct.h>   // _mkdir
#include <io.h>       // _access
#include <windows.h>  // 실행 경로 확인용

using namespace std;

int main() {
    // ✅ 난수 시드 설정 (매번 다른 센서값 생성)
    srand(static_cast<unsigned int>(time(NULL)));

    // ✅ 고정된 저장 경로 (절대 경로 or 프로젝트 기준 상대경로)
    string folderPath = "C:/Users/user/Desktop/최종프로젝트/cpp/sensor_simulator/shared/data";
    string filePath = folderPath + "/sensor_result.csv";

    // ✅ 폴더 없으면 생성
    if (_access(folderPath.c_str(), 0) == -1) {
        _mkdir(folderPath.c_str());
    }

    // ✅ 파일 열기
    ofstream file(filePath);
    if (!file.is_open()) {
        cerr << "❌ sensor_result.csv 파일을 열 수 없습니다." << endl;
        return 1;
    }

    // ✅ CSV 헤더
    file << "timestamp,temperature,humidity,co2,vibration,energy_usage,"
        << "temp_status,hum_status,co2_status,vib_status,energy_status\n";

    for (int i = 0; i < 50; i++) {
        time_t now = time(0) + i;

        struct tm localTime;
        localtime_s(&localTime, &now);

        stringstream ss;
        ss << put_time(&localTime, "%Y-%m-%d %H:%M:%S");
        string timestamp = ss.str();

        // 센서값 생성
        float temp = static_cast<float>(rand() % 15 + 20);
        float hum = static_cast<float>(rand() % 40 + 30);
        float co2 = static_cast<float>(rand() % 1000 + 300);
        float vib = static_cast<float>(rand() % 100) / 10.0f;
        float energy = static_cast<float>(rand() % 1000 + 200);

        // 상태 판단
        string temp_status = (temp > 30) ? "red" : (temp > 27 ? "yellow" : "green");
        string hum_status = (hum < 35) ? "red" : (hum < 45 ? "yellow" : "green");
        string co2_status = (co2 > 1000) ? "red" : (co2 > 700 ? "yellow" : "green");
        string vib_status = (vib > 8.0f) ? "red" : (vib > 5.0f ? "yellow" : "green");
        string energy_status = (energy > 1000) ? "red" : (energy > 800 ? "yellow" : "green");

        // CSV 작성
        file << timestamp << "," << temp << "," << hum << "," << co2 << "," << vib << "," << energy << ","
            << temp_status << "," << hum_status << "," << co2_status << "," << vib_status << "," << energy_status << "\n";
    }

    file.close();
    cout << "✅ sensor_result.csv 생성 완료!" << endl;
    return 0;
}
