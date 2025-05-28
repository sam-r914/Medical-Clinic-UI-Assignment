from clinic.note import *
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.dao.note_dao_pickle import NoteDAOPickle
class PatientRecord:

    #constructor
    def __init__(self, autosave=False, phn = '0'):
        self.autosave = autosave
        self.phn = phn
        self.notes_dao = NoteDAOPickle(self.phn, autosave)
        

    #toString
    def __str__(self):
        return str(self.__note_list)
    
    #toString for listing
    def __repr__(self):
        return str(self)
    
    #Purpose: checks if record has note of same code, creates Note instance and adds to note_list
    #Parameters: self
    #            text
    #Returns: new_note instance if successful
    #Raises: IllegalOperationsException if note of specific code already exists
    def create_note(self, text):
        if self.search_note(self.notes_dao.get_count()):
                raise IllegalOperationException
        return self.notes_dao.create_note(text)

    #Purpose: searches note_list for note of provided code
    #Parameters: self
    #            code
    #Returns: note of code passed if found, nothing if not
    def search_note(self, code):
        return self.notes_dao.search_note(code)

    #Purpose: searches note_list for note whose text contains word passed, adds to new list
    #Parameters: self
    #            search_text
    #Returns: found_note, a list of notes containing search text string
    def retrieve_notes(self, search_text):
        return self.notes_dao.retrieve_notes(search_text)
    
    #Purpose: searches for note of specified code, once found updates associated text to new text
    #Parameters: self
    #            code
    #            new_text
    #Returns: True if updated successfully, False if not
    def update_note(self, code, text):
        return self.notes_dao.update_note(code, text)
    
    #Purpose: searches note_list for note of code, once found deletes note from list
    #Parameters: self
    #            code
    #Returns: True if successfully deleted, False if not
    def delete_note(self, code):
        return self.notes_dao.delete_note(code)
    
    # Purpose: returns all the notes from note_list
    # Parameters: self
    # Returns: list of all Note objects
    def list_notes(self):
        return self.notes_dao.list_notes()
    
    def load_record(self, phn):
        return self.notes_dao.load_record(phn)
    
    def delete_record(self, phn):
        return self.notes_dao.delete_record(phn)

    #Purpose: resets entire PatientRecord class to default
    #Parameters: self
    #Returns: True
    def clean(self):
        return self.notes_dao.clean()

    #Purpose: returns autocounter
    def getCount(self):
        return self.notes_dao.get_count()
    
    #Purpose: returns note_list
    def getNot(self):
        return self.notes_dao.list_notes()