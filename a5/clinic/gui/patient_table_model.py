from PyQt6.QtCore import Qt, QAbstractTableModel
# from clinic.controller import Controller


class PatientTableModel(QAbstractTableModel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._data = []

    def refresh_data(self):
        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    # Gets all patinets from controller and lists them in GUI array
    def listPatients(self):
        self._data = []
        patients = self.controller.list_patients()
        for i in range(len(patients)):
            s = [str(patients[i].phn), patients[i].name, patients[i].birth_date, patients[i].phone, patients[i].email, patients[i].address]
            self._data.append(s)
        self.layoutChanged.emit()

    # Retrieves patients by name from controller and lists them in GUI array
    def retrievePatients(self, name):
        self._data = []
        patients = self.controller.retrieve_patients(name)
        for patient in patients:
            s = [str(patient.phn), patient.name, patient.birth_date, patient.phone, patient.email, patient.address]
            self._data.append(s)
        self.layoutChanged.emit()

    # Clears array
    def reset(self):
        self._data = []
        # emitting the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

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
        if self._data:
            return len(self._data[0])
        else:
            return 0


    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        #creates header titles for each section
        headers = ['PHN', 'Name', 'Birth Date', 'Phone', 'Email', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)