# -*- coding: utf-8 -*-
import inspect
import unittest

from factory_sqlachemy import BaseFactory
from .fixture import Actor, create_db, db_config, drop_db


class TestConfigFactory(unittest.TestCase):

    class ActorFactory(BaseFactory):
        FACTORY_FOR = Actor

        def __init__(self):
            pass

    class ActorFactory2(BaseFactory):
        FACTORY_FOR = Actor

        def __init__(self, name):
            self.name = name

    def test_get_args_from_factory_without_constructor(self):
        args = dict()
        inspect_result = inspect.getargspec(self.ActorFactory.__init__)
        self.ActorFactory._get_factory_init_params(inspect_result, args)
        self.assertEqual({}, args)

    def test_get_args_from_factory_with_constructor(self):
        args = dict()
        inspect_result = inspect.getargspec(self.ActorFactory2.__init__)
        self.ActorFactory2._get_factory_init_params(inspect_result, args)
        self.assertEqual(1, len(args))
        self.assertListEqual(['name'], args.keys())

    def test_get_args_from_model(self):
        args = dict()
        self.ActorFactory._get_arguments_from_table(args)
        self.assertEqual(2, len(args))
        self.assertListEqual(['id', 'name'], args.keys())


class TestFactoryCRUD(unittest.TestCase):
    def setUp(self):
        self.engine, self.dbsession = create_db()

    def tearDown(self):
        drop_db(self.engine)

    class ActorFactory(BaseFactory):
        FACTORY_FOR = Actor

        name = 'Juan'

    def test_create_that_should_store_in_database(self):
        args = dict()
        actor = self.ActorFactory.create(_db=db_config)
        self.assertEqual('Juan', actor.name)
