import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtCore import QFile, QTextStream

from ui.prediction_tab import PredictionTab
from ui.overview_tab import OverviewTab
class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()

class SalesForecastApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Forecast Platform")
        self.setGeometry(100, 100, 1280, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.overview_tab = OverviewTab()
        
        self.prediction_tab = PredictionTab()

        self.reports_tab = ReportsTab()

        self.tabs.addTab(self.overview_tab, "OVERVIEW")
        self.tabs.addTab(self.prediction_tab, "PREDICTION")
        self.tabs.addTab(self.reports_tab, "REPORTS")

        self.tabs.setCurrentWidget(self.prediction_tab)

    def load_stylesheet(self, filename):
        style_file = QFile(filename)
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style_file)
            self.setStyleSheet(stream.readAll())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SalesForecastApp()
    window.show()
    sys.exit(app.exec_())