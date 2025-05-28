from unittest import TestCase
from unittest import main
from clinic.note import *

class Note_Test(TestCase):
    
    #Purpose: testing note constructor str and eq methods
    def test_note(self):
        #creating note instances
        note_1 = Note(1, "Testing note, kabam")
        note_2 = Note(2, "another note but different")
        note_3 = Note(1, "testing note of same code")
        note_4 = Note(3, "same text")
        note_5 = Note(3, "same text")
        #testing equality
        #inequality first
        self.assertNotEqual(note_1, note_2, "Should be False")
        self.assertNotEqual(note_1, note_3, "codes are same text is different")
        #equality
        self.assertEqual(note_4, note_5)

        note_4.update("new note text")

        self.assertNotEqual(note_4, note_5)
        
