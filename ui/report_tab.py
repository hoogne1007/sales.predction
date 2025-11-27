import os
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QPushButton, QListWidget, QListWidgetItem)
from PyQt5.QtCore import QThread, Qt, QSize
from PyQt5.QtGui import QIcon

from core.workers import ReportGenerationWorker

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Report Generation Form ---
        generator_group = QGroupBox("Historical Performance Reports")
        generator_layout = QHBoxLayout()
        generator_layout.addWidget(QLabel("Time Period:"))
        generator_layout.addWidget(QPushButton("Last 2 Years")) # Placeholder button
        generator_layout.addWidget(QLabel("Region:"))
        generator_layout.addWidget(QPushButton("Global")) # Placeholder button
        generator_layout.addStretch()
        self.generate_button = QPushButton("Generate New Report")
        self.generate_button.clicked.connect(self.start_report_generation)
        generator_layout.addWidget(self.generate_button)
        generator_group.setLayout(generator_layout)

        # --- Generated Reports List ---
        list_group = QGroupBox("Generated Reports")
        list_layout = QVBoxLayout()
        self.report_list = QListWidget()
        list_layout.addWidget(self.report_list)
        list_group.setLayout(list_layout)

        main_layout.addWidget(generator_group)
        main_layout.addWidget(list_group)
        self.setLayout(main_layout)

    def start_report_generation(self):
        # Disable button to prevent multiple clicks
        self.generate_button.setEnabled(False)
        self.generate_button.setText("Generating...")

        # Create a unique report name and path
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"Quarterly_Sales_Forecast_{timestamp}"
        output_path = os.path.join("reports", f"{report_name}.pdf")

        # Add a placeholder item to the list
        self.add_report_item(report_name, "In Progress")

        # --- Threading ---
        self.thread = QThread()
        self.worker = ReportGenerationWorker(output_path, report_name)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_report_finished)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_report_finished(self, report_path, success):
        # Find the item in the list and update its status
        for i in range(self.report_list.count()):
            item = self.report_list.item(i)
            widget = self.report_list.itemWidget(item)
            if widget.property("report_name") in report_path:
                status_label = widget.findChild(QLabel, "status_label")
                if success:
                    status_label.setText("Completed")
                    status_label.setStyleSheet("color: green;")
                else: 
                    status_label.setText("Failed")
                    status_label.setStyleSheet("color: red;")
                break
        
        self.generate_button.setEnabled(True)
        self.generate_button.setText("Generate New Report")

    def add_report_item(self, name, status):
        item = QListWidgetItem(self.report_list)
        item_widget = QWidget()
        item_layout = QHBoxLayout()

        # Icon and Text
        icon_label = QLabel()
        # You can add an icon here if you have one, e.g., QIcon('path/to/icon.png')
        item_layout.addWidget(QLabel(f"{name}\nDate: {datetime.date.today()}"))
        item_layout.addStretch()

        # Status
        status_label = QLabel(status)
        status_label.setObjectName("status_label") # For finding it later
        item_layout.addWidget(status_label)

        # View Button
        view_button = QPushButton("View")
        view_button.clicked.connect(lambda: self.view_report(name))
        item_layout.addWidget(view_button)

        item_widget.setLayout(item_layout)
        item_widget.setProperty("report_name", name) # Store name for identification
        
        item.setSizeHint(item_widget.sizeHint())
        self.report_list.addItem(item)
        self.report_list.setItemWidget(item, item_widget)
        
    def view_report(self, report_name):
        report_path = os.path.join("reports", f"{report_name}.pdf")
        if os.path.exists(report_path):
            print(f"Opening report: {report_path}")
            # This is a cross-platform way to open a file with the default app
            os.startfile(os.path.abspath(report_path))
        else:
            print(f"Report not found: {report_path}")