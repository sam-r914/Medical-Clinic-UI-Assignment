import json
from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
from clinic.patient_record import PatientRecord

from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON(PatientDAO):
    #; Note: Class expects all calls to be valid
    # (exception checking is done before calling this class)

    # Purpose: Initializes Class, attempting to load patients from file if autosave is on 
    def __init__(self, autosave=False):
        self.autosave = autosave
        self.filename = 'clinic/patients.json'
        
        # Attempt to restore patients from file
        if self.autosave:  
            try:
                with open(self.filename, 'r') as jfile:
                    # restore patients and num patients
                    self.__patient_list = json.loads(jfile.read(), cls=PatientDecoder)
                    self.__numPatients = len(self.__patient_list)

                    #restore patient notes
                    for patient in self.__patient_list:
                        patient.record = PatientRecord(self.autosave, patient.phn)
                        patient.record.load_record(patient.phn)
                        #restore patient record based on patients phn
            except: #no file to restore from or issue reading it
                self.__patient_list = []
                self.__numPatients = 0
                
        else:   #if autosave off, start with a new patient_list
            self.__patient_list = []
            self.__numPatients = 0
        
    # Purpose:  saves patient_list to file when called if and only if autosave is True
    #               file is 'patients.json' and is stored in the 'clinic' directory
    def saving(self):
        if self.autosave:
            with open(self.filename, 'w') as jfile:
                jfile.write(json.dumps(self.__patient_list, cls=PatientEncoder))
   

    # Purpose:      Adds new patient to patient_list
    #                 And saves to disk if autosave is on
    # Parameters:   phn : personal health number of patient
    #               name : name of patient
    #               birth_dat : birth date of patient
    #               phone : phone number of patient
    #               email : email of patient
    #               address : current address of patient
    # returns:      newly created patient
    def create_patient(self, phn, name, birth_date, phone, email, address):
        #create patient object
        patient1 = Patient(phn, name, birth_date, phone, email, address,autosave=self.autosave)

        #add new patient object
        self.__patient_list.append(patient1)
        self.__numPatients += 1

        self.saving()    #save to file if autosave is on
        
        return patient1   

    # Purpose:  searches through patient list for patient with the given phn
    # Parameters: phn : personal health number of patient
    # Returns: Patient if found, 'None' otherwise
    def search_patient(self, phn):
        if(self.__numPatients == 0):
            return  #no patients to look thorugh
        for patient in self.__patient_list:
            if (patient.phn == phn):
                return patient
        return 
    
    # Purpose: returns all patiens with 'name' anywhere in their name
    # Parameters: name : string to search for in patient names
    # Returns: list of patiens, 'None' if no patient found    
    def retrieve_patients(self, name):
        listPatients = []
        for patient in self.__patient_list:
            if(patient.name.find(name) != -1):
                listPatients.append(patient)
        
        return listPatients

    # Purpose:      Updates the info about a patient in patient_list
    #               And saves to disk if autosave is on
    # Parameters:   oldPhn : phn of patient to update
    #               the rest : same as create_patient
    # returns:      True if sucessfully updated
    def update_patient(self, oldPhn, phn, name, birth_date, phone, email, address):
        newPatient = Patient(phn, name, birth_date, phone, email, address)

        #updates patient
        for i in range(self.__numPatients):
            if (self.__patient_list[i].phn == oldPhn):  
                self.__patient_list[i] = newPatient
                
                self.saving()    #save to file if autosave is on
                
                return True

    # Purpose:      Deletes patient from patient_list with given phn
    #                 also saves to disk if autosave is on
    # Paramaters:   phn : personal health number of patient to delete
    # returns:      True if succesfully deleted
    def delete_patient(self, phn):
        for patient in self.__patient_list:
            if (patient.phn == phn):
                self.__patient_list.remove(patient)
                self.__numPatients -= 1
                patient.record.delete_record(patient.phn)
                self.saving()    #save to file if autosave is on

                return True

    # Purpose:  returns a list of all patients
    # Parameters: none
    # Returns: list of patients
    def list_patients(self):
        return self.__patient_list

