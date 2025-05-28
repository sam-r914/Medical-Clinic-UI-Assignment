# controller.py
import hashlib
#file r/w
import os
from pathlib import Path
#local classes
from clinic.patient import *
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.patient_record import *
from clinic.note import *
#local exceptions
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class Controller():

    # initializer
    def __init__(self, autosave=False):
        self.__loggedIn = False
        self.__currentPatient = None 
        self.patients_dao = PatientDAOJSON(autosave)
        self.autosave = autosave
        self.__users = self.load_users() 
        
        
        #File IO
    # Purpose:      Reads users.txt to load usernames and password hashes
    # Parameters:   None
    # Returns:      users : dictionary of users who can log in + their password hashes
    def load_users(self):
        users = {}
        main_path = os.path.dirname(__file__)
        file_path = os.path.join(main_path, 'users.txt')
        with open(file_path, 'r') as file:
            for line in file:
                x = line.split(',')
                x[0] = x[0].strip()
                x[1] = x[1].strip()
                users.update({x[0]:x[1]})
        return users
    
        # Login and Logout
    # Purpose:   logs into controller if usr and passwd are in the __users dics
    #               if not logged in, cannot use any other functions
    #            users and password hashes are read from users.txt file
    # Parameters:  usr : username to log in with
    #              passwd: password to log in iwth
    # Returns:   True: if logged in succesfully
    # Raises:   DuplicateLoginException : tried to log in if already logged in
    #           InvalidLoginException : user/password not in system 
    def login(self, usr, passwd):
        if(self.__loggedIn):
            raise DuplicateLoginException #already logged in
        if(usr in self.__users):
            passwd = self.get_password_hash(passwd)
            if(passwd == self.__users[usr]):
                self.__loggedIn = True
                return True            #successful login
        raise InvalidLoginException   #unseccessful login


    def get_password_hash(self, password):
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        hex_dig = hash_object.hexdigest()
        return hex_dig
    # Purpose: logs out of controller
    # Parameters: none
    # Returns: True if logged user out
    # Raises:  InvalidLogoutException : if user is already logged out
    def logout(self):
        if(self.__loggedIn == True):
            self.__loggedIn = False
            return True
        else:
            raise InvalidLogoutException          

        # Patient processing
    # Purpose:creates a new patient, adding it to a list and incrementing __numPatients
    # Parameters: phn : personal health number of patient
    #             name : name of patient
    #             birth_dat : birth date of patient
    #             phone : phone number of patient
    #             email : email of patient
    #             address : current address of patient
    # Returns: patient object if succesfuly created, 'None' otherwise
    # Raises:   IllegalAccessException : not logged in
    #           IllegalOperationException : new phn already in use
    def create_patient(self, phn, name, birth_date, phone, email, address):
        if(not self.__loggedIn):
            raise IllegalAccessException 

        #checks in given phn is already in use
        tempPatient = self.patients_dao.search_patient(phn)
        if (tempPatient is not None):
            raise IllegalOperationException #patient with given health number exists

        return self.patients_dao.create_patient(phn, name, birth_date, phone, email, address)
 
    # Purpose:  searches through patient list for patient with the given phn
    # Parameters: phn : personal health number of patient
    # Returns: Patient if found, 'None' otherwise
    # Raises:   IllegalAccessException : not logged in
    def search_patient(self, phn):
        if(not self.__loggedIn):
            raise IllegalAccessException
        return self.patients_dao.search_patient(phn)

    # Purpose: returns all patiens with 'name' anywhere in their name
    # Parameters: name : string to search for in patient names
    # Returns: list of patiens, 'None' if no patient found
    # Raises:   IllegalAccessException : not logged in
    def retrieve_patients(self, name):
        if(not self.__loggedIn):
            raise IllegalAccessException
        return self.patients_dao.retrieve_patients(name)


    # Purpose: updates a patient with the new data
    #           Return False if new phn is already in use
    #           Alse returns false if patient to update is currently selected
    # Parameters: oldPhn : phn of patient to update
    #             the rest : same as create_patient
    # Returns: True if sucessfully updated
    # Raises:   IllegalAccessException : not logged in
    #           NoCurrentPatientException : no current patient selected
    #           IllegalOperationException : new phn already in use
    #                                        or patient to update is selected
    #                                        or phn given not in system
    def update_patient(self, oldPhn, phn, name, birth_date, phone, email, address):
        if(not self.__loggedIn):
            raise IllegalAccessException

        #tests if new phn is already in the system (if new is diffirent from old one)
        if(oldPhn != phn):
            tempPatient = self.patients_dao.search_patient(phn)
            if (tempPatient is not None):
                raise IllegalOperationException   #cannot update patient to have a phn that is already used
        tempPatient = self.patients_dao.search_patient(oldPhn)
        if(tempPatient is None):
            raise IllegalOperationException # oldPhn given is not in system
        if(self.__currentPatient is not None and tempPatient == self.__currentPatient):
            raise IllegalOperationException # cannot update currently selected patinet

        return self.patients_dao.update_patient(oldPhn, phn, name, birth_date, phone, email, address)


    # Purpose:  deletes patient object with given phn
    #             Returns False if no patient with given phn 
    #               Or if patient to delete is currently selected
    # Parameters: phn : personal health number of patient to delete
    # Returns: True if successfully deleted
    # Raises:   IllegalAccessException : not logged in
    #           IllegalOperationException : attempt to delete currently selected patient
    #                                        or given phn not in system
    def delete_patient(self, phn):
        if (not self.__loggedIn):
            raise IllegalAccessException
        tempPatient = self.patients_dao.search_patient(phn)
        if(tempPatient is None):
            raise IllegalOperationException # given phn not in system
        if(self.__currentPatient is not None and tempPatient == self.__currentPatient):
            raise IllegalOperationException    #cannot delete currently selected patient

        return self.patients_dao.delete_patient(phn)


    # Purpose:  returns a list of all patients
    # Parameters: none
    # Returns: list of patients
    # Raises:   IllegalAccessException : not logged in
    def list_patients(self):
        if(not self.__loggedIn):
            raise IllegalAccessException
        return self.patients_dao.list_patients()

        # Set/unset Current patient
    # Purpose: returns selected patient if one is selected
    # Parameters: none
    # Returns: currently selected patient or None if no selected
    # Raises:   IllegalAccessException : not logged in
    def get_current_patient(self):
        if(not self.__loggedIn):
            raise IllegalAccessException
        return self.__currentPatient
        
    # Purpose: updates current patient to patient with given phn
    # Parameters: phn : personall health number of new patient to select
    # Returns: Nothing
    # Raises:   IllegalAccessException : not logged in
    def set_current_patient(self, phn):
        if(not self.__loggedIn):
            raise IllegalAccessException
        tempPatient = self.patients_dao.search_patient(phn)
        if(tempPatient is None):
            raise IllegalOperationException #given phn not in system
        else:
            self.__currentPatient = tempPatient

    # Purpose: unsets current patient
    # Parameters: none
    # Returns: nothing
    # Raises:   IllegalAccessException : not logged in
    def unset_current_patient(self):
        if (not self.__loggedIn):
            raise IllegalAccessException
        self.__currentPatient = None
        

        # Processing of Notes
    # See PatientRecord.create_note
    # Raises:   IllegalAccessException : not logged in
    #           NoCurrentPatientException : no patient selected
    def create_note(self, text):
        if (not self.__loggedIn):
            raise IllegalAccessException
        if(self.__currentPatient is None):
            raise NoCurrentPatientException
        return self.__currentPatient.record.create_note(text)

    # See PatientRecord.search_note
    # Raises:   IllegalAccessException : not logged in
    #           NoCurrentPatientException : no patient selected
    def search_note(self, int):
        if (not self.__loggedIn):
            raise IllegalAccessException
        if(self.__currentPatient is None):
            raise NoCurrentPatientException
        return self.__currentPatient.record.search_note(int)        

    # See PatientRecord.retrieve_notes
    # Raises:   IllegalAccessException : not logged in
    #           NoCurrentPatientException : no patient selected
    def retrieve_notes(self, text):
        if (not self.__loggedIn):
            raise IllegalAccessException
        if(self.__currentPatient is None):
            raise NoCurrentPatientException
        return self.__currentPatient.record.retrieve_notes(text)

    # See PatientRecord.update_note
    # Raises:   IllegalAccessException : not logged in
    #           NoCurrentPatientException : no patient selected
    #           IllegalOperationException : no notes to update
    def update_note(self, num, text):
        if (not self.__loggedIn):
            raise IllegalAccessException
        if(self.__currentPatient is None):
            raise NoCurrentPatientException

        if(self.__currentPatient.record.getCount() == 1):
            return False #no notes to update
        return self.__currentPatient.record.update_note(num, text)
        
    
    # See PatientRecord.delete_note
    # Raises:   IllegalAccessException : not logged in
    #           IllegalOperationException : no notes to update
    def delete_note(self, num):
        if (not self.__loggedIn):
            raise IllegalAccessException
        if(self.__currentPatient is None):
            raise NoCurrentPatientException
        if(self.__currentPatient.record.getCount() == 1):
            return False #no notes to delete
        return self.__currentPatient.record.delete_note(num)

    # Purpose: returns all the notes of a patient from newest to oldest
    # Parameters: none
    # Returns: list of notes
    # Raises:   IllegalAccessException : not logged in
    #           IllegalOperationException : no notes to update
    def list_notes(self):
        if (not self.__loggedIn):
            raise IllegalAccessException
        if(self.__currentPatient is None):
            raise NoCurrentPatientException
        
        return self.__currentPatient.record.list_notes()

    #resets all variables to default
    def clean(self):
        self.__currentPatient = None
        self.__loggedIn = False
        for patient in self.__patient_list:
            patient.record.clean()
        self.__patient_list = []
        self.__numPatients = 0
        return True
        

if __name__ == "__main__":
    main()

