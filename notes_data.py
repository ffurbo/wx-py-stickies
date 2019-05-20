""" data module """

import json
from pathlib import Path

class Category():
    """ category notes """

    def __init__(self):
        self.category_id = 0
        self.name = ""
        self.notes = []

    def load_data(self):
        """ load data from server """
        if self.category_id == 0:
            return False
        else:
            pass

    def add_note(self, note):
        """ add new note """
        self.notes.append(note)

    def load_files(self):
        """ generate some test data """
        self.name = "Test category"

        data_path = Path('data/')

        for path in data_path.glob('note_*.json'):
            note = Note()
            note.load_from_file(str(path))
            self.add_note(note)

        # for i in range(5):
        #     note = Note()
        #     note.load_from_file('data/note_%d.json'%(i))
        #     self.add_note(note)


class Note():
    """ single note """

    def __init__(self):
        self.note_id = ""
        self.title = ""
        self.content = ""

    def set_data(self, note_id, title, content):
        """ set fields """
        self.note_id = note_id
        self.title = title
        self.content = content

    def load_data(self):
        """ load data from server """
        if self.note_id == 0:
            return False
        else:
            pass

    def save_to_file(self):
        """ save data to file """

        file_name = 'data/note_%s.json'%(self.note_id)

        data = {
            'note_id': self.note_id,
            'title': self.title,
            'content': self.content
        }

        try:
            file = open(file_name, 'w')
            file.write(json.dumps(data))
        except OSError as err:
            print("can't save data: {0}".format(err))
        else:
            file.close()
            print("data saved")
        finally:
            print("Function execution completed")

    def load_from_file(self, file_name):
        """ load note from file """

        try:
            file = open(file_name, 'r')
            datastr = file.read()
        except OSError as err:
            print("can't read data: {0}".format(err))
        else:
            file.close()
            data = json.loads(datastr)

            self.note_id = data['note_id']
            self.title = data['title']
            self.content = data['content']

            print("data read")

def new_note(title):
    """ create new note locally """

    note_path = Path('data/note_%s.json'%title)
    if note_path.is_file():
        print("path exist")
        # Store configuration file values
    else:
        file_name = 'data/note_%s.json'%title

        data = {
            'note_id': title,
            'title': title,
            'content': ""
        }

        try:
            file = open(file_name, 'w')
            file.write(json.dumps(data))
        except OSError as err:
            print("can't save data: {0}".format(err))
            return None
        else:
            file.close()

            note = Note()
            note.note_id = data['note_id']
            note.title = data['title']
            note.content = data['content']
            print("data saved")
            return note
