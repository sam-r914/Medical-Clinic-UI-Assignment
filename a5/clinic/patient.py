from clinic.patient_record import *
class Patient:

    def __init__(self, phn, name, birth_date, phone, email, address, record = None, autosave=False): #class constructor
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.record = PatientRecord(autosave, self.phn)
        self.record.clean() #ensuring that patient record doesnt carry over from another patient
    #Purpose: compares all variables of object to matching variables of another object
    #Parameters: self
    #            other - Patient
    #Returns: True if equal, False if not
    def __eq__(self, other):
        return self.phn == other.phn and self.name == other.name and self.birth_date == other.birth_date and self.phone == other.phone and self.email == other.email and self.address == other.address
    
    #Purpose: converts object into string format
    def __str__(self): #setting string version of patient
        return f'{self.name} - {self.phn}'
    
    #Purpose: converts list object string into readable format
    def __repr__(self): #setting object string representation of patient
        return str(self)
    