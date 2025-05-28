class Note:
    import datetime
    def __init__(self, code, text, timestamp = datetime.datetime.now()): #class constructor, setting timestamp to current time and date
        self.code = code
        self.text = text
        self.timestamp = timestamp
    #Purpose: converts object into readable string
    def __str__(self): 
         return f'Note {self.code}: \"{self.text}\" Timestamp: {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
    
    #Purpose: coverts list object string into readable string
    def __repr__(self):
        return str(self)
    
    #Purpose: tests current object's variables against other object's variables to test for equality
    def __eq__(self, other):
        return self.code == other.code and self.text == other.text

    #Purpose: updates current text to new text passed and updates timestamp to time of execution
    #Parameters: self
    #            text
    #Returns: nothing
    def update(self, text, timestamp = datetime.datetime.now()): #updates text and timestamp to new text and current timestamp
        self.text = text
        self.timestamp = timestamp