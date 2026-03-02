import sys, requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from requests import HTTPError, RequestException


class WeatherApp(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.city_label = QLabel("Enter city name" ,self)
        self.city_input = QLineEdit(self)
        self.get_data_button = QPushButton("Get weather data", self)
        self.temp_label, self.icon_label, self.desc_label = QLabel(self), QLabel(self), QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 250, 250, 300)
        self.city_input.setFixedHeight(35)

        #layout manager
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label), vbox.addWidget(self.city_input), vbox.addWidget(self.get_data_button)
        vbox.addWidget(self.temp_label), vbox.addWidget(self.icon_label), vbox.addWidget(self.desc_label)
        self.setLayout(vbox)
        for i, label in enumerate((self.city_label, self.city_input, self.temp_label, self.icon_label, self.desc_label, self.get_data_button)):
            try: label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            except AttributeError: pass
            label.setObjectName(f"{i}_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Calibri;
            }
            QLabel#0_label {
                font-size: 40px;
                font-weight: bold;
            }
            QLineEdit#1_label {
                font-size: 20px;
            }
            QPushButton#5_label {
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#2_label {
                font-size: 40px;
            }
            QLabel#3_label {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#4_label {
                font-size: 50px;
            }
        """)

        self.get_data_button.clicked.connect(self.getWeather)

    def getWeather(self):
        api_key = "d4614e4b9516f9a70cce74855b7312e9"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            #normally try doesnt catch this
            response.raise_for_status()
            response = response.json()
            if response["cod"] == 200:
                self.displayWeather(response)

        except requests.exceptions.HTTPError as http_err:
            match http_err.response.status_code:
                case 400:
                    self.displayError("Bad Request:\nPlease check your input.")
                case 401:
                    self.displayError("Unauthorized:\nPlease ensure API key is correct.")
                case 403:
                    self.displayError("Forbidden:\nAccess denied.")
                case 404:
                    self.displayError("Not Found:\nCity not found.")
                case 500:
                    self.displayError("Internal Server Error:\nPlease try again later.")
                case 502:
                    self.displayError("Bad Gateway:\nInvalid response from the server.")
                case 503:
                    self.displayError("Service Unavailable:\nServer is down.")
                case 504:
                    self.displayError("Gateway Timeout:\nNo response from the server.")
                case _:
                    self.displayError(f"HTTP error occurred:\n{http_err}")
        except requests.exceptions.ConnectionError:
            self.displayError("Connection error:\nCheck your internet connection.")
        except requests.exceptions.Timeout:
            self.displayError("Timeout error:\nCheck your internet connection.")
        except requests.exceptions.TooManyRedirects:
            self.displayError("Too many redirects:\nCheck the URl.")
        except requests.exceptions.RequestException as req_err:
            self.displayError(f"Request error:\n{req_err}")

    def displayError(self, error_msg):
        self.temp_label.setStyleSheet("font-size: 25px;")
        self.temp_label.setText(error_msg)
        self.icon_label.clear(), self.desc_label.clear()

    def displayWeather(self, data):
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        weather_desc = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temp_label.setText(f"{temp_c:.2f}°C")
        self.temp_label.setStyleSheet("font-size: 40px;")

        self.icon_label.setText(self.getWeatherIcon(weather_id))
        self.desc_label.setText(weather_desc.title())

    @staticmethod
    def getWeatherIcon(weather_id):

        icon = next((
            v for k, v in {
            (200 <= weather_id <= 232): "🌧",
            (300 <= weather_id <= 321): "🌦",
            (500 <= weather_id <= 531): "🌧",
            (600 <= weather_id <= 622): "🌨",
            (701 <= weather_id <= 741): "🌫",
            (weather_id == 762): "🌋",
            (weather_id == 771): "💨",
            (weather_id == 781): "🌪",
            (weather_id == 800): "🌞",
            (801 <= weather_id <= 804): "☁",
        }.items() if k
        ), " ")
        return icon

def main():
    app, w = QApplication(sys.argv), WeatherApp()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__': main()
