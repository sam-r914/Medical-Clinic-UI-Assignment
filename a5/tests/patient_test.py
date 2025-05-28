from unittest import TestCase
from unittest import main
from clinic.patient import *

class patient_test(TestCase):
    
    #Purpose: testing patient constructor, str and eq methods
    def test_patient(self):
        #creating patient instances
        patient_1 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        patient_2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        patient_3 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        #testing when patients are different
        self.assertNotEqual(patient_1, patient_2, "are not equal")
        #testing when patients are the same
        self.assertEqual(patient_2, patient_3, "are equal")

        patient_4 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.ca", "300 Moss St, Victoria")
        self.assertNotEqual(patient_3, patient_4, "1 field diffirence = not equal")

    #Purpose: testing patient constructor, str and eq methods again with more instances
    def test_patient_again_and_str(self):
        #creating patient instances
        patient_1 = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        patient_2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        patient_3 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        patient_4 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        #testing here
        #testing inequality first
        self.assertNotEqual(patient_1, patient_2)
        self.assertNotEqual(patient_3, patient_1)
        #testing equality
        self.assertEqual(patient_3, patient_4)
        #testing string
        self.assertEqual(str(patient_1), "Joe Hancock - 9792225555", "string representation is correct")


