from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt6.QtWidgets import QPushButton, QGridLayout

# Window to confirm when updating or deleting patient
class PatientConfirmDeletionWindow(QMainWindow):
    # Signals to connect to clinic_gui
    confirm_signal = pyqtSignal()
    cancel_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Please Confirm")
        self.resize(400,200)
        layout = QGridLayout()
        label_phn = QLabel("Are you sure you wish to delete this patient?")
        self.button_confirm = QPushButton("Confirm")
        self.button_cancel = QPushButton("Cancel")
        
        #setting up layout
        layout.addWidget(label_phn, 0, 0)
        layout.addWidget(self.button_confirm, 1, 0)
        layout.addWidget(self.button_cancel, 1, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #butoon click connections
        self.button_confirm.clicked.connect(self.confirm_button_clicked)
        self.button_cancel.clicked.connect(self.cancel_button_clicked)

    # 
    def confirm_button_clicked(self):
        self.confirm_signal.emit()
        self.hide()
    
    def cancel_button_clicked(self):
        self.cancel_signal.emit()
        self.hide()

#Window to confirm changes to patients data
class PatientConfirmChangeWindow(QMainWindow):
    # Signals to connect to clinic_gui
    confirm_update_signal = pyqtSignal()
    cancel_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Please Confirm")
        self.resize(400,200)
        layout = QGridLayout()
        label_phn = QLabel("Are you sure you wish to update this patient?")
        self.button_confirm = QPushButton("Confirm")
        self.button_cancel = QPushButton("Cancel")
        
        layout.addWidget(label_phn, 0, 0)
        layout.addWidget(self.button_confirm, 1, 0)
        layout.addWidget(self.button_cancel, 1, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.button_confirm.clicked.connect(self.confirm_button_clicked)
        self.button_cancel.clicked.connect(self.cancel_button_clicked)

    def confirm_button_clicked(self):
        self.confirm_update_signal.emit()
        self.hide()
    
    def cancel_button_clicked(self):
        self.cancel_signal.emit()
        self.hide()