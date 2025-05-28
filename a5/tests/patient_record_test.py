from unittest import TestCase
from unittest import main
from clinic.patient import *

class Patient_Record_Test(TestCase):
    #Purpose: testing creating notes attached to a patient instance
    def test_create_note(self):
        #creating patient
        patient1 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        #creating expected Note and actual Note
        expected_1 = Note(1, "Patient has headache")
        expected_2 = Note(2, "Patient has taken pain relief pills")
        actual_note_1 = patient1.record.create_note("Patient has headache")
        actual_note_2 = patient1.record.create_note("Patient has taken pain relief pills")
        #testing here
        self.assertEqual(actual_note_1, expected_1)
        self.assertEqual(actual_note_2, expected_2)
        self.assertNotEqual(actual_note_1, actual_note_2)

        patient1.record.clean() #clearing all instances

    #Purpose: testing search_note through a list
    def test_search(self): #testing search note
        #creating patient instance
        patient3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        #creating expected output and actual output instances
        expected_1 =  Note(1, "Patient has headache")
        expected_2 = Note(2, "Patient has taken pain relief pills")
        patient3.record.create_note("Patient has headache")
        patient3.record.create_note("Patient has taken pain relief pills")
        #testing here
        self.assertEqual(patient3.record.search_note(1), expected_1)
        self.assertEqual(patient3.record.search_note(2), expected_2)
        self.assertIsNone(patient3.record.search_note(3))
        #clearing all instances
        patient3.record.clean()

    #Purpose: testing retrieve_note and comparing list sizes
    def test_retrieve(self): #testing retrieve using a piece of text
        #creating patient instance
        patient2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        #creating patient record notes
        patient2.record.create_note("Patient comes with headache and high blood pressure.")
        patient2.record.create_note("Patient complains of a strong headache on the back of neck.")
        patient2.record.create_note("Patient is taking medicines to control blood pressure.")
        patient2.record.create_note("Patient feels general improvement and no more headaches.")
        patient2.record.create_note("Patient says high BP is controlled, 120x80 in general.")
        #creating empty lists to store relevent retrieved notes
        retrieved_list = []
        retrieved_list2 = []
        retrieved_list = patient2.record.retrieve_notes("headache")
        #testing if length of returned list matches expected length
        self.assertEqual(len(retrieved_list), 3)
        #same test, different search word
        retrieved_list2 = patient2.record.retrieve_notes("neck")
        self.assertEqual(len(retrieved_list2), 1)
        list3 = []
        self.assertEqual(patient2.record.retrieve_notes("ankle"), list3)
        #clearing all instances from patient
        patient2.record.clean()

    #Purpose testing update_note for text changes and delete method for functionality
    def test_update_and_delete(self): #testing updating note and the delete method
        #creating patient instance
        patient = Patient(8197815917, "Jane Hill", "2005-005-04", "250 404 0167", "ocelot4@yahoo.ca", "11518 Harvey St, Summerland")
        #creating note to be updated with more detail
        patient.record.create_note("Patient comes with lump on neck")
        #updating note
        patient.record.update_note(1, "Patient comes with lump on front left side of neck")
        #adding another note for testing purposes
        patient.record.create_note("Patient taken for CAT scan")
        #creating expected note and wrong note for comparison purposes
        expected_note1 = Note(1, "Patient comes with lump on front left side of neck")
        notexpected_note2 = Note(1, "Patient comes with lump on neck")
        #testing here for update
        self.assertEqual(patient.record.search_note(1), expected_note1)
        self.assertNotEqual(patient.record.search_note(1), notexpected_note2)
        #testing delete method
        self.assertTrue(patient.record.delete_note(2))
        self.assertTrue(patient.record.delete_note(1))
        self.assertFalse(patient.record.delete_note(2))
        #testing invalid codes excess deletes
        for i in range(-3,5):
            self.assertFalse(patient.record.delete_note(i))
        #clearing all instances
        self.assertTrue(patient.record.clean())

    def test_getters(self):
        #creating patient instance
        patient = Patient(8197815917, "Jane Hill", "2005-005-04", "250 404 0167", "ocelot4@yahoo.ca", "11518 Harvey St, Summerland")
        #creating note to be updated with more detail
        note1 = patient.record.create_note("Patient comes with lump on neck")
        note2 = patient.record.create_note("Patient takes headache medication")
        note3 = patient.record.create_note("Patient broke a bone")

        note_list = [note1, note2, note3]

        self.assertEqual(patient.record.getCount(), 4, "next note is #4")
        self.assertEqual(patient.record.getNot(), note_list, "note list is correct")

              

        
