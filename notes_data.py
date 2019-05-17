""" data module """

import json

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

    def test(self):
        """ generate some test data """
        self.name = "Test category"
        for i in range(5):
            note = Note()
            note.set_data(i, "title %d" % (i), "content %d" % (i))
            self.add_note(note)


class Note():
    """ single note """

    def __init__(self):
        self.note_id = 0
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

        file_name = 'data/note_%d.json'%(self.note_id)

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
