# -*- coding: utf-8 -*-
import unittest

from factory_sqlachemy import BaseFactory
from .configs import Actor, create_db, db_config, drop_db


class TestCreateFactory(unittest.TestCase):

    def setUp(self):
        self.engine, self.dbsession = create_db()

    def tearDown(self):
        drop_db(self.engine)

    class ActorFactory(BaseFactory):
        FACTORY_FOR = Actor

        name = 'Juan'

    def test_create_that_should_store_in_database(self):
        actor = self.ActorFactory.create(_db=db_config)
        self.assertEqual('Juan', actor.name)
        # TODO: check on db
