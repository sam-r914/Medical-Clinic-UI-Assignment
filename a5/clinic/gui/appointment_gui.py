from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtWidgets import QMainWindow
from clinic.gui.note_crud import CreateNoteWindow, DeleteNoteWindow, RetrieveNoteWindow, UpdateNoteWindow
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPlainTextEdit
from PyQt6.QtWidgets import QPushButton, QMessageBox, QGridLayout

class SelectPatientGUI(QMainWindow):
    selectsignal = pyqtSignal()
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Select Patient")
        self.resize(400,200)
       
        #creating layout elements
        layout = QGridLayout()
        label_phn = QLabel("Input PHN")
        self.text_phn = QLineEdit()
        self.text_phn.clear()
        self.button_search = QPushButton("Search")
        self.button_cancel = QPushButton("Cancel")
        
        #setting up default button when 'enter' is pressed as search button
        self.button_search.setAutoDefault(True)
        self.button_search.setDefault(True)
        
        #setting up layout
        layout.addWidget(label_phn, 0, 0)
        layout.addWidget(self.text_phn, 0, 1)
        layout.addWidget(self.button_search, 1, 0)
        layout.addWidget(self.button_cancel, 1, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #button clicked connections
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_cancel.clicked.connect(self.cancel_button_clicked)

    #Purpose: Searches for Patient in System from inputted text and sets patient as current patient to start appointment
    #Parameters: None
    #Returns: Emits signal to open AppointmentGUI when successful, warning QMessageBox when failed
    def search_button_clicked(self):
        phn = self.text_phn.text()
        try:
            phn = int(phn)
        except:
            QMessageBox.warning(self, "Error", "Ensure your input contains only numbers")
        patient = self.controller.search_patient(phn)
        if patient is None: #unsuccessful search of patient
            QMessageBox.warning(self, "Error", "could not find in database")   
        else: #successful search of patient
            self.controller.set_current_patient(phn)
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Patient Found")
            msgBox.setText("Start Appointment with '"+str(patient.name)+"'?")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            bttn = msgBox.exec()

                #Activating AppointmentGUI window
            if bttn == QMessageBox.StandardButton.Yes:
                self.text_phn.clear()
                self.appointment_menu = AppointmentGUI(self.controller)
                self.appointment_menu.showMaximized()
                self.hide()
            else:
                self.text_phn.clear()
        


    #Purpose: cancels operation and exits out of window
    #Parameters: None
    #Returns: Nothing
    def cancel_button_clicked(self):
        self.text_phn.clear()
        self.hide()
    
    #defines close event
    def closeEvent(self, event):
        self.cancel_button_clicked()

class AppointmentGUI(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Appointment")
        
        #creating layout elements
        layout = QGridLayout()
        self.listings = QPlainTextEdit()
        self.listings.appendPlainText("Press 'Add New Note' to get started") #initial default text to aid in system navigation
        self.listings.appendPlainText("Press 'List All Notes' to see all current notes and changes made")
        self.listings.setEnabled(False)
        self.listed = False
        width = 200
        height = 100
        self.create_button = QPushButton("Add New Note")
        self.create_button.setFixedSize(QSize(width, height))
        self.delete_button = QPushButton("Delete Note")
        self.delete_button.setFixedSize(QSize(width, height))
        self.retrieve_button = QPushButton("Retrieve Notes")
        self.retrieve_button.setFixedSize(QSize(width, height))
        self.update_button = QPushButton("Update Note")
        self.update_button.setFixedSize(QSize(width, height))
        self.list_button = QPushButton("List All Notes")
        self.list_button.setFixedSize(QSize(width, height))
        self.end_button = QPushButton("End Appointment")
        self.end_button.setFixedSize(QSize(width, height))

        #setting up layout
        layout.addWidget(self.listings, 0, 1, 7, 1)
        layout.addWidget(self.create_button, 0, 0)
        layout.addWidget(self.delete_button, 1, 0)
        layout.addWidget(self.retrieve_button, 2, 0)
        layout.addWidget(self.update_button, 3, 0)
        layout.addWidget(self.list_button, 4, 0)
        layout.addWidget(self.end_button, 5, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #initializing CRUD windows
        self.delete_note = DeleteNoteWindow(self.controller, parent=self)
        self.create_note = CreateNoteWindow(self.controller)
        self.retrieve_note = RetrieveNoteWindow(self.controller, parent=self)
        self.update_note = UpdateNoteWindow(self.controller, parent=self)

        #button clicked connections
        self.create_button.clicked.connect(self.button_create_clicked)
        self.delete_button.clicked.connect(self.button_delete_clicked)
        self.retrieve_button.clicked.connect(self.button_retrieve_clicked)
        self.update_button.clicked.connect(self.button_update_clicked)
        self.list_button.clicked.connect(self.button_list_clicked)
        self.end_button.clicked.connect(self.button_end_clicked)

    #Purpose: Activates create note window, catches signal to refresh listings
    #Parameters: None
    #Returns: Nothing
    def button_create_clicked(self):
        self.create_note.show()
        self.create_note.sig.connect(self.refresh)
    
    #Purpose: Activates delete note window, catches signal to refresh listings
    #Parameters: None
    #Returns: Nothing
    def button_delete_clicked(self):
        self.delete_note.show()
        self.delete_note.sig.connect(self.refresh)

    #Purpose: Activates retrieve note window, catches signal to activate list_retrieved function
    #Parameters: None
    #Returns: Nothing
    def button_retrieve_clicked(self):
        self.retrieve_note.show()
        
        self.retrieve_note.sig.connect(self.list_retrieved)

    #Purpose: Prints list of notes retrieved by retrieve notes window in listings widget
    #Parameters: None
    #Returns: Nothing  
    def list_retrieved(self):
        self.listings.clear()
        listt = self.retrieve_note.list1
        for note in listt:
            self.listings.appendPlainText(note.__repr__())

    #Purpose: Activates update note window
    #Parameters: None
    #Returns: Nothing
    def button_update_clicked(self):
        self.update_note.show()
        self.update_note.sig.connect(self.refresh)

    #Purpose: Lists all current notes in listings widget
    #Parameters: None
    #Returns: Nothing
    def button_list_clicked(self):
        self.listings.clear()
        self.listed = True
        for note in self.controller.list_notes():
            self.listings.appendPlainText(note.__repr__())

    #Purpose: Refreshes list shown in listings widget when self.listed is true
    #Parameters: None
    #Returns: Nothing
    def refresh(self):
        if self.listed == True:
            self.button_list_clicked()

    #Purpose: Exits out of AppointmentGUI
    #Parameters: None
    #Returns: Nothing
    def button_end_clicked(self):
        self.listings.clear()
        self.hide()

