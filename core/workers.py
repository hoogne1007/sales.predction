
import time
import random
import os
from PyQt5.QtCore import QObject, pyqtSignal
from core.report_generator import generate_report_pdf

from ml.model_handler import train_model 

class ModelTrainingWorker(QObject):
    finished = pyqtSignal(dict)      # Signal to emit when training is done, carrying the results dictionary
    progress = pyqtSignal(int)       # Signal to emit for progress updates, carrying an integer (0-100)
    
    def __init__(self, selected_features, algorithm_choice, hyperparameters):
        super().__init__()
        self.selected_features = selected_features
        self.algorithm_choice = algorithm_choice
        self.hyperparameters = hyperparameters
        self.is_running = True

    def run(self):
        """The main work method."""
        for i in range(1, 6):
            if not self.is_running:
                break # Exit if canceled
            time.sleep(1) # Simulate one part of the training
            self.progress.emit(i * 15) # Emit progress (15, 30, 45, 60, 75)

        if self.is_running:
            # Call the actual (now fast) training function
            results = train_model(
                self.selected_features, self.algorithm_choice, self.hyperparameters
            )
            self.progress.emit(100)
            self.finished.emit(results)

    def stop(self):
        """Stops the worker."""
        self.is_running = False
        
class ReportGenerationWorker(QObject):
    """
    A worker that runs the PDF report generation in a separate thread.
    """
    finished = pyqtSignal(str, bool) # Emits the report path and success status

    def __init__(self, output_path, report_name):
        super().__init__()
        self.output_path = output_path
        self.report_name = report_name

    def run(self):
        """The main work method."""
        try:
            # Simulate a bit of a delay for data fetching/processing
            time.sleep(2)
            
            # Call the actual PDF generator
            generate_report_pdf(self.output_path, self.report_name)
            
            # Emit success signal
            self.finished.emit(self.output_path, True)
        except Exception as e:
            print(f"Error generating report: {e}")
            # Emit failure signal
            self.finished.emit(str(e), False)