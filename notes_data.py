""" data module """

import json
import time
import os
from pathlib import Path

class Category():
    """ category notes """

    def __init__(self, category_name):
        self.category_id = 0
        self.name = category_name
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
        """ load notes from files """
        # self.name = "Test category"

        data_path = Path('data/categories/%s'%self.name)

        for path in data_path.glob('note_*.json'):
            note = Note(self)
            note.load_from_file(str(path))
            self.add_note(note)

    def __str__(self):
        return "---> name: %s, %s"%(self.name, self.notes)
        # for i in range(5):
        #     note = Note()
        #     note.load_from_file('data/note_%d.json'%(i))
        #     self.add_note(note)


class Note():
    """ single note """

    def __init__(self, category):
        self.note_id = ""
        self.title = ""
        self.content = ""
        self.category = category

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

        file_name = 'data/categories/%s/note_%d.json'%(self.category.name, self.note_id)

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

    def __str__(self):
        return "%d - %s"%(self.note_id, self.title)


def new_note(title, category):
    """ create new note locally """

    note_id = int(time.time())
    file_name = 'data/categories/%s/note_%d.json'%(category.name, note_id)

    note_path = Path(file_name)
    if note_path.is_file():
        print("path exist")
    else:
        data = {
            'note_id': note_id,
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

            note = Note(category)
            note.note_id = data['note_id']
            note.title = data['title']
            note.content = data['content']
            print("data saved")
            return note


def new_category(title):
    """ create new category locally """

    dir_name = "data/categories/%s"%title
    # Create target Directory if don't exist
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Directory ", dir_name, " Created ")
        category = Category(title)
        return category
    else:
        print("Directory ", dir_name, " already exists")
        return None
