from PyQt6.QtCore import Qt, QAbstractTableModel

class DataInputModel(QAbstractTableModel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._data = [["", "", "", "", "", ""]]
        # self._data = [["12345678", "firstname middle lastname", "YYYY-MM-DD", "+1-123-456-7890", "randomemail@emailprovider.mail", "some real address St Dr"]]
        self.refresh_data()

    # Sets all input fields to ""
    def set_blank(self):
        self._data = [["", "", "", "", "", ""]]
        self.layoutChanged.emit()

    # Sends signal to refresh individual data fields
    def refresh_data(self):
        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    # Attempts to add patient based on given info
    # Returns text based on success
    def addPatient(self, key, name, birth, phone, email, addr):
        try:
            self.controller.create_patient(int(key), name, birth, phone, email, addr)
            return "Patient succesfully added"
        except Exception as err:
            return "Given PHN already exists in system"
    
    # Attempts to update patient
    # returns 1 if sucessful, and 2 if not
    def updatePatient(self, oldphn, newphn, name, birth, phone, email, addr):
        try:
            self.controller.update_patient(int(oldphn), int(newphn), name, birth, phone, email, addr)
            return 1
        except:
            return 2

    # Gets patient by name
    # Returns 1 if unsucessful and 0 if it is successful
    def getPatient(self, key):
        patient = self.controller.search_patient(int(key))
        if(patient is None):
            return 1
        else:
            self._data = [[str(patient.phn), str(patient.name), str(patient.birth_date), str(patient.phone), str(patient.email), str(patient.address)]]
            return 0

    # Attempts to delete patinet
    # If successful, returns None
    # Otherwise returns whatever is excepted
    def deletePatient(self, key):
        try:
            self.controller.delete_patient(int(key))
            return
        except Exception as err:
            return err

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]

            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight
            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value
            
            return value

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ['PHN', 'Name', 'Birth Date', 'Phone Number', 'Email', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)
