from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPlainTextEdit
from PyQt6.QtWidgets import QPushButton, QMessageBox, QGridLayout

class CreateNoteWindow(QMainWindow):
    sig = pyqtSignal() #signal emitted to refresh list in AppointmentGUI
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Create New Note")
        
        #establishing layout elements
        layout = QGridLayout()
        self.label = QLabel("Write Note")
        self.text_note = QPlainTextEdit()
        self.text_note.clear()
        self.text_note.setFixedSize(300, 200)
        self.add_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")
        
        #making add button default to activate when 'enter' is pressed
        self.add_button.setAutoDefault(True)
        self.add_button.setDefault(True)
        
        #setting up layout
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.text_note, 0, 1)
        layout.addWidget(self.add_button, 1, 0)
        layout.addWidget(self.cancel_button, 1, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #button clicking functionalities
        self.add_button.clicked.connect(self.add_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

    #Purpose: Takes text from PlainTextEdit and creates a new note
    #Parameters: None
    #Returns: None when successful, Warning message when failed
    def add_button_clicked(self):
        text = self.text_note.toPlainText()
        try:
            self.controller.create_note(text)
            self.cancel_button_clicked()
        except:
            QMessageBox.warning(self, "Error", "Failed to make note")

    #Purpose: Exits out of window when pressed
    #Parameters: None
    #Returns: Emits signal to refresh list
    def cancel_button_clicked(self):
        self.text_note.clear()
        self.sig.emit()
        self.hide()


class DeleteNoteWindow(QMainWindow):
    sig = pyqtSignal() #signal emitted to refresh list in AppointmentGUI
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Delete Note")
        self.resize(300, 100)
        
        #Creating layout elements
        layout = QGridLayout()
        self.label = QLabel("Note Code:")
        self.text_code = QLineEdit()
        self.text_code.clear()
        self.delete_button = QPushButton("Delete")
        self.cancel_button = QPushButton("Cancel")

        #setting delete button as default selection when 'enter' is pressed
        self.delete_button.setAutoDefault(True)
        self.delete_button.setDefault(True)

        #setting up layout
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.text_code, 0, 1)
        layout.addWidget(self.delete_button, 1, 0)
        layout.addWidget(self.cancel_button, 1, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #button clicked connections
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

    #Purpose: takes inputed text from user, finds note of specified code and deletes it
    #Parameter: None
    #Returns: Nothing when successful, warning QMessageBox when failed
    def delete_button_clicked(self):
        code = self.text_code.text()
        try:
            self.controller.delete_note(int(code))
            self.cancel_button_clicked()
        except:
            QMessageBox.warning(self, "Error", "Note '"+str(code)+"' does not exist. Please enter valid numerical code.")

    #Purpose: Exits out of window when connected button is pressed
    #Parameters: None
    #Returns: Emits signal to refresh list
    def cancel_button_clicked(self):
        self.text_code.clear()
        self.sig.emit()
        self.hide()


class RetrieveNoteWindow(QMainWindow):
    sig = pyqtSignal() #signal to start listing operation in AppointmentGUI
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Retrieve Notes")
        self.resize(400, 100)
        
        #creating up layout elements
        self.label = QLabel("Keyword to Search For: ")
        self.text_searchwords = QLineEdit()
        self.text_searchwords.clear()
        self.search_button = QPushButton("Search")
        self.cancel_button = QPushButton("Cancel")

        #setting search button as default selection when 'enter' is pressed
        self.search_button.setAutoDefault(True)
        self.search_button.setDefault(True)

        #setting up layout
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.text_searchwords, 0, 1)
        layout.addWidget(self.search_button, 1, 0)
        layout.addWidget(self.cancel_button, 1, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.list1 = [] #initializing empty list for retrieved notes to be stored
        
        #button clicked connections
        self.search_button.clicked.connect(self.search_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)


    #Purpose: takes inputted text and searches for notes containing text, storing list of valid notes
    #Parameters: None
    #Returns: Emits Signal for AppointmentGUI to pickup to print the retrieved list
    def search_button_clicked(self):
        text = self.text_searchwords.text()
        self.list1 = self.controller.retrieve_notes(str(text))
        if text == "":
            self.list1 = []
        self.sig.emit()
        self.cancel_button_clicked()
        
    #Purpose: Exits out of Window
    #Parameters: None
    #Returns: Nothing
    def cancel_button_clicked(self):
        self.text_searchwords.clear()
        self.hide()


class UpdateNoteWindow(QMainWindow):
    sig = pyqtSignal() #signal to refresh list in AppointmentGUI
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Update Note Contents")
        self.resize(600, 200)
        
        #creating layout elements
        self.labelll = QLabel("Please input code of note to be updated first, then press 'Search'")
        self.label = QLabel("Note Code to Update:")
        self.text_code = QLineEdit()
        self.text_code.clear()
        self.label2 = QLabel("Note Text to Change: ")
        self.text_content = QPlainTextEdit()
        self.text_content.clear()
        self.text_content.setEnabled(True)
        self.lookup_button = QPushButton("Search")
        self.update_button = QPushButton("Update")
        self.cancel_button = QPushButton("Cancel")

        #setting update button as default selection when 'enter' is pressed
        self.lookup_button.setAutoDefault(True)
        self.lookup_button.setDefault(True)

        #setting up layout
        layout = QGridLayout()
        layout.addWidget(self.labelll, 0, 0, 1, 3)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.text_code, 1, 1, 1, 2)
        layout.addWidget(self.label2, 2, 0)
        layout.addWidget(self.text_content, 2, 1, 1, 2)
        layout.addWidget(self.lookup_button, 3, 0)
        layout.addWidget(self.update_button, 3, 1)
        layout.addWidget(self.cancel_button, 3, 2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        #button clicked connections
        self.lookup_button.clicked.connect(self.lookup_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.update_button.clicked.connect(self.update_button_clicked)
    
    #Purpose: takes input from code text line, searches for note and displays note text in plaintextedit
    #Parameters: None
    #Returns: text_content changed when successsful, warning QMesssageBox when failed
    def lookup_button_clicked(self):
        code = self.text_code.text()
        try:
            note = self.controller.search_note(int(code))
            self.text_content.clear()
            self.text_content.appendPlainText(str(note.text))      

        except:
            QMessageBox.warning(self, "Error", "Note not found. Please enter numerical code of note")
    
    #Purpose: takes input from text edit plaintextedit and updates note of inputed code above
    #Parameters: None
    #Returns: Nothing when successful, warning QMessageBox when failed
    def update_button_clicked(self):
        text1 = self.text_content.toPlainText()
        code = self.text_code.text()
        try:
            code = int(code)
            text1 = str(text1)
        except:
            QMessageBox.warning(self, "Error", "Please use correct syntax")
        try:
            self.controller.update_note(code, text1)
            self.cancel_button_clicked()
        except:
            QMessageBox.warning(self, "Error", "Could not update note")

    #Purpose: exits out of window
    #Parameters: None
    #Returns: Emits signal to refresh list
    def cancel_button_clicked(self):
        self.text_code.clear()
        self.text_content.clear() 
        self.sig.emit()
        self.hide()
