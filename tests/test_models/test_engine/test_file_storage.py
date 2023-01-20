#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import unittest

FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def setUp(self):
        """Sets up test methods"""
        self.storage = FileStorage()
        self.bm = BaseModel()
        self.u = User()
        self.p = Place()
        self.s = State()
        self.c = City()
        self.a = Amenity()
        self.r = Review()
        self.storage.save()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Tests the get method"""
        self.assertEqual(self.storage.get(BaseModel, self.bm.id), self.bm)
        self.assertEqual(self.storage.get(User, self.u.id), self.u)
        self.assertEqual(self.storage.get(Place, self.p.id), self.p)
        self.assertEqual(self.storage.get(State, self.s.id), self.s)
        self.assertEqual(self.storage.get(City, self.c.id), self.c)
        self.assertEqual(self.storage.get(Amenity, self.a.id), self.a)
        self.assertEqual(self.storage.get(Review, self.r.id), self.r)
        self.assertIsNone(self.storage.get(Review, "fake_id"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Tests the count method"""
        self.storage.new(self.bm)
        self.storage.new(self.u)
        self.storage.new(self.p)
        self.storage.new(self.s)
        self.storage.new(self.c)
        self.storage.new(self.a)
        self.storage.new(self.r)
        self.assertEqual(self.storage.count(), 7)
        self.assertEqual(self.storage.count(BaseModel), 1)
        self.assertEqual(self.storage.count(User), 1)
        self.assertEqual(self.storage.count(Place), 1)
        self.assertEqual(self.storage.count(State), 1)
        self.assertEqual(self.storage.count(City), 1)
        self.assertEqual(self.storage.count(Amenity), 1)
        self.assertEqual(self.storage.count(Review), 1)
        self.assertEqual(self.storage.count(object), 0)
        with self.assertRaises(TypeError):
            self.storage.count(int)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_reload(self):
        """Tests the reload method"""
        # create a new file_storage object and save it
        st = FileStorage()
        st.save()
        # remove the file
        import os
        os.remove(st._FileStorage__file_path)
        # reload the file should not raise an error
        st.reload()
