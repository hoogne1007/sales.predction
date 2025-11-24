from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QCheckBox, QLineEdit, QSlider, QPushButton,
                             QProgressBar, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QThread
from core.workers import ModelTrainingWorker

class PredictionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None
        self.init_ui()
        
        # Connect signals to slots
        self.retrain_button.clicked.connect(self.start_training)
        self.cancel_button.clicked.connect(self.cancel_training)

    def init_ui(self):
        # 1. Create the main vertical layout for the entire tab
        final_layout = QVBoxLayout(self)
        # 2. Create a horizontal layout for the three content columns
        content_layout = QHBoxLayout()
        # --- Left, Center, Right columns setup (no changes here) ---
        left_vbox = QVBoxLayout()
        feature_group = QGroupBox("Feature Selection")
        feature_layout = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        feature_layout.addWidget(self.search_bar)
        self.feature_checkboxes = {
            "Historical Sales Data": QCheckBox("Historical Sales Data"),
            "Economic Indicators": QCheckBox("Economic Indicators"),
            "Competitor Activity": QCheckBox("Competitor Activity"),
            "Website Traffic": QCheckBox("Website Traffic"),
        }
        self.feature_checkboxes["Historical Sales Data"].setChecked(True)
        self.feature_checkboxes["Economic Indicators"].setChecked(True)
        for name, checkbox in self.feature_checkboxes.items():
            feature_layout.addWidget(checkbox)
        feature_layout.addStretch(1)
        feature_group.setLayout(feature_layout)
        left_vbox.addWidget(feature_group)
        content_layout.addLayout(left_vbox, 1)
        center_vbox = QVBoxLayout()
        algo_group = QGroupBox("Algorithm Choice")
        algo_layout = QVBoxLayout()
        self.algo_gradient_boosting = QCheckBox("Gradient Boosting")
        self.algo_random_forest = QCheckBox("Random Forest")
        self.algo_neural_network = QCheckBox("Neural Network")
        self.algo_gradient_boosting.setChecked(True)
        algo_layout.addWidget(self.algo_gradient_boosting)
        algo_layout.addWidget(self.algo_random_forest)
        algo_layout.addWidget(self.algo_neural_network)
        algo_group.setLayout(algo_layout)
        center_vbox.addWidget(algo_group)
        hyper_group = QGroupBox("Hyperparameters")
        hyper_layout = QVBoxLayout()
        hyper_layout.addWidget(QLabel("N_Estimators"))
        self.n_estimators_slider = QSlider(Qt.Horizontal)
        self.n_estimators_slider.setRange(100, 1000)
        self.n_estimators_slider.setValue(100)
        hyper_layout.addWidget(self.n_estimators_slider)
        hyper_layout.addWidget(QLabel("Max Training:"))
        self.max_training_slider = QSlider(Qt.Horizontal)
        self.max_training_slider.setValue(100)
        hyper_layout.addWidget(self.max_training_slider)
        hyper_group.setLayout(hyper_layout)
        center_vbox.addWidget(hyper_group)
        content_layout.addLayout(center_vbox, 1)
        right_vbox = QVBoxLayout()
        self.training_progress = QProgressBar()
        self.training_progress.setRange(0, 100)
        self.training_progress.setValue(0)
        self.training_progress.setTextVisible(True)
        self.training_progress.setFormat("Training Model... %p%")
        right_vbox.addWidget(self.training_progress, alignment=Qt.AlignCenter)
        summary_group = QGroupBox("Last Training Summary")
        summary_layout = QVBoxLayout()
        self.summary_label_progress = QLabel("Training Progress: -")
        self.summary_label_accuracy = QLabel("Achieved Accuracy: -")
        self.summary_label_model_id = QLabel("Model ID: -")
        summary_layout.addWidget(self.summary_label_progress)
        summary_layout.addWidget(self.summary_label_accuracy)
        summary_layout.addWidget(self.summary_label_model_id)
        summary_group.setLayout(summary_layout)
        right_vbox.addWidget(summary_group)
        content_layout.addLayout(right_vbox, 1)
        # --- End of columns setup ---
        final_layout.addLayout(content_layout)
        bottom_hbox = QHBoxLayout()
        self.retrain_button = QPushButton("RETRAIN MODEL")
        self.cancel_button = QPushButton("CANCEL TRAINING")
        self.cancel_button.setEnabled(False)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_hbox.addSpacerItem(spacer)
        bottom_hbox.addWidget(self.cancel_button)
        bottom_hbox.addWidget(self.retrain_button)
        final_layout.addLayout(bottom_hbox)


    def start_training(self):
        """Gathers UI settings and starts the worker thread."""
        print("UI: Starting training process...")
        # Prevent starting a new training run while one is active
        if self.thread and self.thread.isRunning():
            print("UI: A training process is already running.")
            return

        # 1. Update UI to reflect training state
        self.retrain_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.training_progress.setValue(0)

        # 2. Gather data from UI
        selected_features = [name for name, cb in self.feature_checkboxes.items() if cb.isChecked()]
        
        # 3. Create a QThread and a worker object
        self.thread = QThread()
        self.worker = ModelTrainingWorker(
            selected_features=selected_features,
            algorithm_choice="Gradient Boosting",
            hyperparameters={"n_estimators": self.n_estimators_slider.value()}
        )
        
        # 4. Move worker to the thread
        self.worker.moveToThread(self.thread)
        
        # 5. Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_training_finished)
        self.worker.progress.connect(self.set_progress)
        
        # Cleanup connections
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        # 6. Start the thread
        self.thread.start()

    def cancel_training(self):
        """Stops the training thread."""
        print("UI: Attempting to cancel training...")
        if self.thread and self.thread.isRunning():
            self.worker.stop()
            self.thread.quit()
            self.thread.wait() # Wait for the thread to finish
            print("UI: Training canceled.")
            self.retrain_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            self.training_progress.setValue(0)
            self.training_progress.setFormat("Cancelled")

    def set_progress(self, value):
        """Updates the progress bar."""
        self.training_progress.setValue(value)
        self.training_progress.setFormat(f"Training Model... {value}%")

    def on_training_finished(self, results):
        """Handles the results from the worker thread."""
        print("UI: Worker finished, received results.")
        self.summary_label_accuracy.setText(f"Achieved Accuracy: {results['achieved_accuracy']}")
        self.summary_label_model_id.setText(f"Model ID: {results['model_id']}")
        self.training_progress.setFormat("Completed")
        
        # Re-enable the UI
        self.retrain_button.setEnabled(True)
        self.cancel_button.setEnabled(False)