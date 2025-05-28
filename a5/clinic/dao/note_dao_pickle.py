from pickle import load, dump
import os
from clinic.note import Note
from clinic.dao.note_dao import NoteDAO
from clinic.exception.illegal_operation_exception import IllegalOperationException

class NoteDAOPickle(NoteDAO):
    #Constructor
    def __init__(self, phn, autosave=False):
        self.autosave = autosave
        self.filename = 'clinic/records/' + str(phn) + '.dat'
        
        if self.autosave:
            if not os.path.exists('clinic/records'): #if folder to store records does not exist, create it
                os.makedirs('clinic/records')
            try:
                with open(self.filename, 'rb') as bfile:
                    #load all notes from patient into list
                    self.__note_list = load(bfile)
                self.__autocounter = len(self.__note_list)+1 #updating number of notes
            except:
                self.__note_list = []
                self.__autocounter = 1
            

    def saving(self):
        if self.autosave:
            with open(self.filename, 'wb') as bfile1:
                dump(self.__note_list, bfile1)

    def create_note(self, text):
        new_note = Note(self.__autocounter, text)
        self.__note_list.append(new_note)
        self.__autocounter += 1
        self.saving()
        return new_note

    def search_note(self, code):
        for x in self.__note_list:
            if x.code == code:
                return x
        return
    
    def retrieve_notes(self, search_text):
        found_notes = []
        for x in self.__note_list:
            if x.text.find(search_text) != -1:
                found_notes.append(x)
        return found_notes

    def update_note(self, code, text):
        for x in self.__note_list:
            if x.code == code:
                x.update(text)
                self.saving()
                return True
        return False
    
    def delete_note(self, code):
        if self.__autocounter == 1:
            return #no notes to remove
        if code >= self.__autocounter:
            raise IllegalOperationException
        for x in self.__note_list:
            if x.code == code:
                self.__note_list.remove(x)
                self.__autocounter -= 1
                self.reorder_notes()
                self.saving()
                return True
        return False
    
    def reorder_notes(self):
        i = 1
        for x in self.__note_list:
            x.code = i
            i += 1

    def load_record(self, phn):
        self.filename = 'clinic/records/' + str(phn) + '.dat'
        if not os.path.exists('clinic/records'): #if folder to store records does not exist, create it
            os.makedirs('clinic/records')
        try:
            with open(self.filename, 'rb') as bfile:
                #load all notes from patient into list
                self.__note_list = load(bfile)
            self.__autocounter = len(self.__note_list)+1 #updating number of notes
        except: #if file does not exist
            self.__note_list = []
            self.__autocounter = 1

    def delete_record(self, phn):
        filename1 = 'clinic/records/' + str(phn) + '.dat'
        if os.path.exists(filename1):
            os.remove(filename1)
    
    def clean(self):
        self.__autocounter = 1
        self.__note_list = []
        return True
    
    def list_notes(self):
        return list(reversed(self.__note_list))
    
    def get_count(self):
        return self.__autocounter