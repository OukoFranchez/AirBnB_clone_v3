#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from console import HBNBCommand
from datetime import datetime
import inspect
import MySQLdb
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User
import json
from os import getenv
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', 'Tesing DBStorage only')
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the class for tests"""
        cls.command = HBNBCommand()

    def setUp(self):
        """ create a MySQLdb connection """
        uname = getenv("HBNB_MYSQL_USER")
        passw = getenv("HBNB_MYSQL_PWD")
        dbhost = getenv("HBNB_MYSQL_HOST")
        dbname = getenv("HBNB_MYSQL_DB")
        self.test_engine = MySQLdb.connect(
            host=dbhost,
            user=uname, password=passw,
            database=dbname
        )

    def tearDown(self):
        """ close the db connection """
        self.test_engine.close()

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        # self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_model_storage(self):
        """ Test storage is an instance of DBStorage """
        self.assertTrue(isinstance(storage, DBStorage))

    def test_create(self):
        """ Test adding a new object """
        # initialize sqlalchemy connection
        storage.reload()

        # get the initial objects
        cur = self.test_engine.cursor()
        cur.execute("SELECT * FROM states;")
        init_objs = cur.fetchall()

        # create a new object and commit transaction to save the new object
        self.command.onecmd('create State name="California"')
        self.test_engine.commit()

        # Retrieve the data
        cur.execute("SELECT * FROM states;")
        new_objs = cur.fetchall()

        # Confirm the results
        self.assertTrue(len(new_objs) > len(init_objs))

    def test_count_method(self):
        """ Test method_to get count """
        # initialize sqlalchemy connection
        storage.reload()

        # get the initial objects
        cur = self.test_engine.cursor()
        cur.execute("SELECT * FROM states;")
        init_objs = cur.fetchall()

        # get the number of objects using count method
        count = storage.count(State)

        # Confirm the results
        self.assertEqual(len(init_objs), count)

    def test_get_method(self):
        """ Test method_to get created object """
        # initialize sqlalchemy connection
        storage.reload()

        # create a user object
        user = User(email='jdoe@mail.com', password='1234',
                    first_name='John', last_name='Doe')
        storage.new(user)
        storage.save()

        # get the created object
        stored_user = storage.get(User, user.id)

        # Confirm the results
        self.assertEqual(user, stored_user)
