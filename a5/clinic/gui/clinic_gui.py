import sys
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow
from clinic.controller import Controller
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit
from PyQt6.QtWidgets import QPushButton, QMessageBox, QGridLayout

controller = Controller(autosave=True)
class LoginGUI(QMainWindow):
    loggedSignal = pyqtSignal() #signal to activate ClinicGUI window
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(400,200)
        
        #creating layout elements
        self.layout = QGridLayout()
        label_username = QLabel("Username")
        self.text_username = QLineEdit()
        label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button_login = QPushButton("Login")
        self.button_quit = QPushButton("Quit")
        
        #activating click function on login button when selected and 'enter' is pressed
        self.button_login.setDefault(True)
        self.button_login.setAutoDefault(True)

        #setting up layout
        self.layout.addWidget(label_username, 0, 0)
        self.layout.addWidget(self.text_username, 0, 1)
        self.layout.addWidget(label_password, 1, 0)
        self.layout.addWidget(self.text_password, 1, 1)
        self.layout.addWidget(self.button_login, 2, 0)
        self.layout.addWidget(self.button_quit, 2, 1)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        #button clicked connections
        self.button_login.clicked.connect(self.login_button_clicked)
        self.button_quit.clicked.connect(self.quit_button_clicked)
        self.show()

    #Purpose: Takes input text and logs in using controller
    #Parameters: None
    #Returns: Emits Signal for main ClinicGUI to activate when successful, warning QMessageBox when failed
    def login_button_clicked(self):
        username = self.text_username.text()
        password = self.text_password.text()
        try:
            controller.login(username, password)
            self.text_password.clear()
            self.text_username.clear()
            self.loggedSignal.emit()
            self.hide()
        except:
            QMessageBox.critical(self, "Unsuccessful Login", "Incorrect User or Password. Try again")
            self.text_password.clear()
            self.text_username.clear()

    def quit_button_clicked(self):
        sys.exit()

from PyQt6.QtWidgets import QTableView
from clinic.gui.patient_table_model import PatientTableModel
from clinic.gui.data_input_model import DataInputModel
from clinic.gui.appointment_gui import SelectPatientGUI
from clinic.gui.patient_confirm import PatientConfirmDeletionWindow
from clinic.gui.patient_confirm import PatientConfirmChangeWindow
class ClinicGUI(QMainWindow):
    loggedoutsignal = pyqtSignal() #signal to activate LoginGUI
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        
        #Top Right panel to show individual patient data and to Create, Read, Update, and Delete patients
        self.input_table = QTableView()
        self.layout.addWidget(self.input_table, 0, 1, 2, -1)

            # adding labels and text feilds for data input
        # creating and adding labels to top right panel
        self.phn_label = QLabel("PHN\n\n\n")
        self.layout.addWidget(self.phn_label, 0, 1, 3, 1)
        self.name_label = QLabel("Name\n\n\n")
        self.layout.addWidget(self.name_label, 0, 2, 3, 1)
        self.birth_label = QLabel("Birth Date\n\n\n")
        self.layout.addWidget(self.birth_label, 0, 3, 3, 1)
        self.phone_label = QLabel("Phone Number\n\n\n")
        self.layout.addWidget(self.phone_label, 0, 4, 3, 1)
        self.email_label = QLabel("Email\n\n\n")
        self.layout.addWidget(self.email_label, 0, 5, 3, 1)
        self.addr_label = QLabel("Address\n\n\n")
        self.layout.addWidget(self.addr_label, 0, 6, 3, 1)

        # Bottom Right panel to show bulk data about patients 
        #   I.e. when listing all patients
        self.patient_table = QTableView()
        self.layout.addWidget(self.patient_table, 2, 1, -1, -1)

        # creating and adding text input fields to top right panel
        self.text_phn = QLineEdit()
        self.text_name = QLineEdit()
        self.text_birth = QLineEdit()
        self.text_phone = QLineEdit()
        self.text_email = QLineEdit()
        self.text_addr = QLineEdit()
        self.layout.addWidget(self.text_phn, 1, 1, 1, 1)
        self.layout.addWidget(self.text_name, 1, 2, 1, 1)
        self.layout.addWidget(self.text_birth, 1, 3, 1, 1)
        self.layout.addWidget(self.text_phone, 1, 4, 1, 1)
        self.layout.addWidget(self.text_email, 1, 5, 1, 1)
        self.layout.addWidget(self.text_addr, 1, 6, 1, 1)
        
        # Information text line to display Information/warnings about operations
        self.information = QLineEdit()
        self.layout.addWidget(self.information, 1, 1, 2, -1)
        self.information.setEnabled(False)
        self.baseInfo = "Information: "
        self.information.setText(self.baseInfo)

            # Creating Buttons
        # Creating button Names and sizes
        buttonWidth = 225
        self.addNew_Button = QPushButton("Add New Patient")
        self.addNew_Button.setFixedSize(QSize(buttonWidth, 100))
        self.RemovePat_Button = QPushButton("Remove Patient")
        self.RemovePat_Button.setFixedSize(QSize(buttonWidth, 100))
        self.RetrPat_Button = QPushButton("Retrieve Patients by Name")
        self.RetrPat_Button.setFixedSize(QSize(buttonWidth, 100))
        self.changePat_Button = QPushButton("Change Patient Data")
        self.changePat_Button.setFixedSize(QSize(buttonWidth, 100))
        self.searchPat_Button = QPushButton("Search Patient by PHN")
        self.searchPat_Button.setFixedSize(QSize(buttonWidth, 100))
        self.ListPat_Button = QPushButton("List All Patients")
        self.ListPat_Button.setFixedSize(QSize(buttonWidth, 100))
        self.startAppoint_Button = QPushButton("Start Appointment With Patient")
        self.startAppoint_Button.setFixedSize(QSize(buttonWidth, 100))
        self.LogOut_Button = QPushButton("Log Out")
        self.LogOut_Button.setFixedSize(QSize(buttonWidth, 100))
        self.clear_all = QPushButton("Clear All")
        self.clear_all.setFixedSize(QSize(buttonWidth, 100))
        
        # Inserting buttons on left side of GUI
        self.layout.addWidget(self.addNew_Button, 0, 0)
        self.layout.addWidget(self.RemovePat_Button, 1, 0)
        self.layout.addWidget(self.searchPat_Button, 2, 0)
        self.layout.addWidget(self.changePat_Button, 3, 0)
        self.layout.addWidget(self.ListPat_Button, 4, 0)
        self.layout.addWidget(self.RetrPat_Button, 5, 0)
        self.layout.addWidget(self.clear_all, 6, 0)
        self.layout.addWidget(self.startAppoint_Button, 7, 0)
        self.layout.addWidget(self.LogOut_Button, 8, 0)

        #button clicked connections    
        self.ListPat_Button.clicked.connect(self.listPat_button_clicked)
        self.LogOut_Button.clicked.connect(self.LogOut_Button_clicked)
        self.startAppoint_Button.clicked.connect(self.appoint_button_clicked)
        self.addNew_Button.clicked.connect(self.addNew_Button_clicked)
        self.searchPat_Button.clicked.connect(self.searchPat_Button_clicked)
        self.RemovePat_Button.clicked.connect(self.RemovePat_Button_clicked)
        self.changePat_Button.clicked.connect(self.changePat_Button_clicked)
        self.RetrPat_Button.clicked.connect(self.RetrPat_Button_clicked)
        self.clear_all.clicked.connect(self.clear_all_clicked)

        # Setting top and bottom panels to their respective Models
        self.input_model = DataInputModel(controller)
        self.input_table.setModel(self.input_model)

        self.patient_model = PatientTableModel(controller)
        self.patient_table.setModel(self.patient_model)
        self.patient_table.doubleClicked.connect(self.add_patient_clicked)

        # var to check if patients are being listed
        self.listing = 0

        #set central widget
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        #initializing the AppointmentGUI sequence with SelectPatientGUI
        self.appointment = SelectPatientGUI(controller, parent=self)

        # Confirmation when updating/deleting patient
        self.deletion = PatientConfirmDeletionWindow()
        self.deletion.hide()
        self.deletion.confirm_signal.connect(self.deleting)
        self.deletion.cancel_signal.connect(self.notDeleting)

        self.updation = PatientConfirmChangeWindow()
        self.updation.hide()
        self.updation.confirm_update_signal.connect(self.updating)
        self.updation.cancel_signal.connect(self.notDeleting)

        # Variable to ensure deletion window is hidden after selecting option
        #   1 = confirmed
        #   0 = calceled
        self.deletingVar = 0
        self.changingVar = 0

        # Refreshes GUI after everything has been initialized
        self.refresh_Input_Table()
        
        
    # Purpose: Refreshes size of columns in the right panels and refreshes data in them
    # Trigger: Function called directly, no button connection
    def refresh_Input_Table(self):
        # Calculates the width that each column should be based on the size of the GUI
        maxWidth = self.input_table.width()
        if(width != 0):
            maxWidth = int(width * 0.87)
        usableWidth = maxWidth-(100+125+150 + 14)

        nameWidth=250
        emailWidth=250
        addressWidth=200

        if(maxWidth > 640):
            nameWidth=int(usableWidth*.4)
            emailWidth=int(usableWidth*.3)
            addressWidth=int(usableWidth*.3)

        if(self.listing == 1):
            self.patient_model.listPatients()
        if(self.listing == 2):
            name = self.text_name.text()
            self.patient_model.retrievePatients(name)

        # Updates column widths based on calcualted data
        self.input_table.setColumnWidth(0,100)  #solid
        self.input_table.setColumnWidth(1,nameWidth)  #variable
        self.input_table.setColumnWidth(2,125)  #solid
        self.input_table.setColumnWidth(3,150)  #solid
        self.input_table.setColumnWidth(4,emailWidth)  #variable
        self.input_table.setColumnWidth(5,addressWidth)  #variable

        self.patient_table.setColumnWidth(0,100)  #solid
        self.patient_table.setColumnWidth(1,nameWidth)  #variable
        self.patient_table.setColumnWidth(2,125)  #solid
        self.patient_table.setColumnWidth(3,150)  #solid
        self.patient_table.setColumnWidth(4,emailWidth)  #variable
        self.patient_table.setColumnWidth(5,addressWidth)  #variable

        # Updates data in the Input Model
        self.input_model.refresh_data()


    # Purpose: sets input fields to the data of the double clicked patient 
    # Trigger: Double clicking on a listed patient
    def add_patient_clicked(self):
        index = self.patient_table.selectionModel().currentIndex()
        self.text_phn.setText(index.sibling(index.row(), 0).data())
        self.text_name.setText(index.sibling(index.row(), 1).data())
        self.text_birth.setText(index.sibling(index.row(), 2).data())
        self.text_phone.setText(index.sibling(index.row(), 3).data())
        self.text_email.setText(index.sibling(index.row(), 4).data())
        self.text_addr.setText(index.sibling(index.row(), 5).data())
        self.refresh_Input_Table()


    # Purpose: Creates new patient when the Add New Patient button is pressed
    #   Requires all 6 data fields to have inputted data, and the the PHN given is not in use
    #   Issues will be shown in the 'Information:' text field
    #   When patient is added, their data is shown in the individual data fields at the top  
    # Trigger: Add New Button pressed
    def addNew_Button_clicked(self):
        # get data from input fields
        key = self.text_phn.text()
        addr = self.text_addr.text()
        birth = self.text_birth.text()
        email = self.text_email.text()
        name = self.text_name.text()
        phone = self.text_phone.text()

        if(not key.isdigit()):
            # Checks that the PHN is an int
            self.information.setText(self.baseInfo + "Please enter a strictly numeric PHN")
            return

        if(key == ""):
            # checks that there is a PHN given
            self.information.setText(self.baseInfo + "Please enter the new patients PHN")
        elif(addr == "" or birth == "" or email == "" or name == "" or phone == ""):
            # checks that all fields are full
            self.information.setText(self.baseInfo + "Please ensure all data fields are inputted")
        else:
            #attempts to add patient
            ret = self.input_model.addPatient(key, name, birth, phone, email, addr)
            self.information.setText(self.baseInfo + ret)
            if(ret == "Patient succesfully added"):
                self.input_model.getPatient(key)
                self.text_phn.clear()
                self.text_name.clear()
                self.text_birth.clear()
                self.text_phone.clear()
                self.text_email.clear()
                self.text_addr.clear()
            self.refresh_Input_Table()  
        
    # Purpose: Attempts to remove patient with given PHN
    #   deletion window is shown before patient is deleted to ensure misclicks do not delete patients
    # Trigger: When the Remove Patient Button is pressed
    def RemovePat_Button_clicked(self):
        # get PHN
        key = self.text_phn.text()

        if(not key.isdigit()): 
            # Checks that the PHN is an int
            self.information.setText(self.baseInfo + "Please enter a strictly numeric PHN")
            return

        if(key == ""):
            # Checks PHN is given
            self.information.setText(self.baseInfo + "Please enter the PHN of the patient to delete")
        else:
            # deletion window
            self.deletion.show()
            if(self.deletingVar == 0):
                # User pressed cancel
                return
            # User pressed confirm
            ret = self.input_model.deletePatient(key)
            if(ret is None):
                # patient is found and deleted
                self.information.setText(self.baseInfo + "Patient %s deleted" % key)
            else:
                # patient with given PHN not found or is in an appointment
                self.information.setText("Error: Patient with this PHN not found or is currently in an appointment")
        
        # Clears input fields 
        # Also sets deletingVar to 0 (As if user pressed cancel) 
        self.input_model.set_blank()
        self.text_phn.clear()
        self.text_name.clear()
        self.text_birth.clear()
        self.text_phone.clear()
        self.text_email.clear()
        self.text_addr.clear()
        self.refresh_Input_Table()
        self.deletingVar = 0
        
    # Called when 'Confirm' is pressed in the deletion window
    def deleting(self):
        self.deletingVar = 1
        self.RemovePat_Button_clicked()
        self.deletion.hide()

    # Called when 'Confirm' is pressed in the updating window
    def updating(self):
        self.changingVar = 1
        self.changePat_Button_clicked()
        self.updation.hide()

    # Called when 'Cancel' is pressed in the deletion window
    def notDeleting(self):
        self.deletingVar = 0
        self.changingVar = 0

    # Purpose: Searcher for patient with given PHN
    # Trigger: Search Patientby PHN button clicked
    def searchPat_Button_clicked(self):
        # Get PHN
        key = self.text_phn.text()

        if(not key.isdigit()): 
            # Checks that the PHN is an int
            self.information.setText(self.baseInfo + "Please enter a strictly numeric PHN")
            return

        if(key == ""):
            # Checks PHN is given
            self.information.setText(self.baseInfo + "Please enter a PHN to search for")
        else:
            # Attempts to get patient
            test = self.input_model.getPatient(key)
            if(test == 1):
                # Patient with PHN not in system
                self.information.setText(self.baseInfo + "Patient not found")
            else:
                # Patient found
                self.information.setText(self.baseInfo + "Patient succesfully found")
            self.refresh_Input_Table()

    # Purpose: Updates listed patient with new data
    #   Patient to be updates is the one shown in top fields
    # Trigger: Change Patient Data button clicked
    def changePat_Button_clicked(self):
        # Patient needs to be listed in top fields to be updated
        if(self.input_model._data[0][0] == ""):
            self.information.setText(self.baseInfo + "Please search for a patient to update first")
        else:
            # Gets new patient data
            oldkey = self.input_model._data[0][0]
            newkey = self.text_phn.text()
            addr = self.text_addr.text()
            birth = self.text_birth.text()
            email = self.text_email.text()
            name = self.text_name.text()
            phone = self.text_phone.text()

            if(not oldkey.isdigit() or not newkey.isdigit()): 
                # Checks that the PHNs are ints
                self.information.setText(self.baseInfo + "Please enter a strictly numeric PHN")
                return

            
            if(newkey == "" or addr == "" or birth == "" or email == "" or name == "" or phone == ""):
                # Checks all data fields are inputted
                self.information.setText(self.baseInfo + "Please ensure all data fields are inputted")
            else:
                # deletion Window
                self.updation.show()
                if(self.changingVar == 0):
                    # User presse cancel
                    return
                # user pressed confirm 
                # Attempts to update patient
                ret = self.input_model.updatePatient(oldkey, newkey, name, birth, phone, email, addr)
                if(ret == 1):
                    # Patient updated succesfully
                    self.information.setText(self.baseInfo + "Patient updated succesfully")
                    self.input_model.getPatient(newkey)
                    self.refresh_Input_Table()
                if(ret == 2):
                    # New PHN already in use or patient is in appointment
                    self.information.setText("Error: Please check that patient is not in appointment and new PHN not in use")

    # Purpose: Lists all patients in bottom right panel
    # Trigger: List All Patients button clicked
    def listPat_button_clicked(self):
        self.listing = 1
        self.patient_model.listPatients()

        self.refresh_Input_Table()
        self.patient_table.setEnabled(True)
        self.information.setText(self.baseInfo + "Double click a patient to add their info into the text fields.")
    # Purpose: Lists all patients with name containing whatever is in the Name input field
    #   If nothing is in Name input field, gives message that all search name is blank 
    def RetrPat_Button_clicked(self):
        self.listing = 2
        # Get Name
        name = self.text_name.text()
        self.patient_model.retrievePatients(name)

        self.refresh_Input_Table()
        self.patient_table.setEnabled(True)
        if(name == ""):
            # Name field is empty, lists all patients 
            self.information.setText(self.baseInfo + "Searched name is blank, returning all patients")
        else:
            self.information.setText(self.baseInfo + "Filtered patients shown")

    # Purpose: Clears all data on screen
    def clear_all_clicked(self):
        self.listing = 0
        self.text_addr.clear()
        self.text_birth.clear()
        self.text_email.clear()
        self.text_name.clear()
        self.text_phn.clear()
        self.text_phone.clear()
        self.patient_model.reset()
        self.refresh_Input_Table()
        self.input_model.set_blank()


    #Purpose: Activates appointment gui window
    def appoint_button_clicked(self):
        self.appointment.show()

    # Purpose: Logs out of controller and closes all windows, then opens login window
    def LogOut_Button_clicked(self):
        controller.logout()
        for window in QApplication.topLevelWidgets():
            window.hide()

        self.loggedoutsignal.emit()
        


    #defines the close event 
    def closeEvent(self, event):
        ''' close all the secondary windows when this window is closed '''
        for window in QApplication.topLevelWidgets():
            window.close()


def main():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    global width 
    width = size.width()

    login = LoginGUI()
    main = ClinicGUI()
    
    login.loggedSignal.connect(main.showMaximized)
    main.loggedoutsignal.connect(login.show)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
