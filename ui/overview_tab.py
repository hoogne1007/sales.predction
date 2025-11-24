from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QGroupBox, QLabel)
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ml.predictor import generate_prediction_data

class OverviewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_dashboard()

    def init_ui(self):
        # --- Main Layout ---
        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # --- Top Section: Chart and KPIs ---
        # Chart
        chart_group = QGroupBox("Quarterly Sales Projections")
        self.chart_layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=8, height=4, dpi=100)
        self.chart_layout.addWidget(self.canvas)
        chart_group.setLayout(self.chart_layout)
        top_layout.addWidget(chart_group, 3) # Give chart more space (ratio 3:1)

        # KPIs
        kpi_group = QGroupBox("Prediction Summary")
        kpi_layout = QVBoxLayout()
        self.kpi_prediction_label = QLabel("15.2M")
        self.kpi_prediction_label.setFont(QFont("Arial", 48, QFont.Bold))
        self.kpi_title_label = QLabel("NEXT QUARTER PREDICTION")
        self.kpi_details_label = QLabel("+3.5% vs. Previous Quarter\nTOP PERFORMING SEGMENT: Enterprise")
        kpi_layout.addWidget(self.kpi_prediction_label)
        kpi_layout.addWidget(self.kpi_title_label)
        kpi_layout.addWidget(self.kpi_details_label)
        kpi_group.setLayout(kpi_layout)
        top_layout.addWidget(kpi_group, 1)

        # --- Bottom Section: Performance Metrics ---
        # Model Performance
        model_perf_group = QGroupBox("Model Performance")
        self.model_perf_layout = QGridLayout()
        # We will populate this grid layout in update_dashboard
        model_perf_group.setLayout(self.model_perf_layout)
        bottom_layout.addWidget(model_perf_group)

        # Feature Weights
        feature_group = QGroupBox("Feature Weights")
        self.feature_layout = QGridLayout()
        # We will populate this grid layout in update_dashboard
        feature_group.setLayout(self.feature_layout)
        bottom_layout.addWidget(feature_group)
        
        # Data Quality
        quality_group = QGroupBox("Data Quality Score")
        quality_layout = QVBoxLayout()
        self.quality_score_label = QLabel("92%")
        self.quality_score_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.quality_score_label.setStyleSheet("color: #4CAF50;") # Green color
        quality_layout.addWidget(self.quality_score_label)
        quality_group.setLayout(quality_layout)
        bottom_layout.addWidget(quality_group)

        # --- Assemble Layouts ---
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

    def update_dashboard(self):
        """Fetches new data and updates all UI elements."""
        data = generate_prediction_data()

        # Update Chart
        self.canvas.axes.clear() # Clear previous plot
        self.canvas.axes.plot(data['historical_x'], data['historical_y'], marker='o', label='Actual Sales History')
        self.canvas.axes.plot(data['predicted_x'], data['predicted_y'], marker='o', linestyle='--', label='Predicted')
        self.canvas.axes.set_title("Revenue Forecast")
        self.canvas.axes.set_xlabel("Time Period")
        self.canvas.axes.set_ylabel("Revenue (Units)")
        self.canvas.axes.legend()
        self.canvas.axes.grid(True)
        self.canvas.draw()

        # Update KPI
        self.kpi_prediction_label.setText(data['next_quarter_prediction'])

        # Update Model Performance Table (clear and repopulate)
        self.clear_layout(self.model_perf_layout)
        self.model_perf_layout.addWidget(QLabel("<b>Metric</b>"), 0, 0)
        self.model_perf_layout.addWidget(QLabel("<b>Value</b>"), 0, 1)
        row = 1
        for key, value in data['model_performance'].items():
            self.model_perf_layout.addWidget(QLabel(key), row, 0)
            self.model_perf_layout.addWidget(QLabel(value), row, 1)
            row += 1

        # Update Feature Weights Table (clear and repopulate)
        self.clear_layout(self.feature_layout)
        self.feature_layout.addWidget(QLabel("<b>Feature</b>"), 0, 0)
        self.feature_layout.addWidget(QLabel("<b>Weight</b>"), 0, 1)
        row = 1
        for key, value in data['feature_weights'].items():
            self.feature_layout.addWidget(QLabel(key), row, 0)
            self.feature_layout.addWidget(QLabel(value), row, 1)
            row += 1

        # Update Data Quality Score
        self.quality_score_label.setText(f"{data['data_quality_score']}%")

    def clear_layout(self, layout):
        """Helper function to clear all widgets from a layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class MplCanvas(FigureCanvas):
    """A custom Matplotlib canvas widget to embed in PyQt."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)