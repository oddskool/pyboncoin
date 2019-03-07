import os
import pickle


class DB(object):

    def __init__(self, path, reset=False):
        self.path = path
        if os.path.exists(path) and reset != 'true':
            self.db = pickle.load(open(path, 'rb'))
        else:
            self.db = dict()
        print("db ready with", len(self.db), "entries")

    def save(self):
        pickle.dump(self.db, open(self.path, 'wb'))

    def __setitem__(self, key, value):
        self.db[key] = value

    def __getitem__(self, key):
        return self.db[key]

    def __contains__(self, item):
        return item in self.db

