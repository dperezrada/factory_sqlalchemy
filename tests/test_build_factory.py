# -*- coding: utf-8 -*-
import unittest

from factory_sqlachemy import BaseFactory
from .configs import Actor, Actor2


class TestPriorityFieldBuildFactory(unittest.TestCase):

    class ActorFactoryRandom(BaseFactory):
        FACTORY_FOR = Actor

    class ActorFactoryDefined(BaseFactory):
        FACTORY_FOR = Actor
        name = 'Juan'

    class ActorFactoryDefault(BaseFactory):
        FACTORY_FOR = Actor2

    class ActorFactoryDefinedOverDefault(BaseFactory):
        FACTORY_FOR = Actor2
        name = 'Daniel'

    class ActorFactory3(BaseFactory):
        def __init__(self, name="Felipe"):
            self.name = name

    def test_random_name(self):
        actor = self.ActorFactoryRandom.build()
        self.assertIsNotNone(actor.name)
        self.assertIsInstance(actor.name, unicode)

    def test_default_name(self):
        actor = self.ActorFactoryDefined.build()
        self.assertEqual('Juan', actor.name)

    def test_defined_name(self):
        actor = self.ActorFactoryDefault.build()
        self.assertEqual('Felipe', actor.name)

    def test_defined_over_default_name(self):
        actor = self.ActorFactoryDefinedOverDefault.build()
        self.assertEqual('Daniel', actor.name)

    def test_force_over_all_name(self):
        actor = self.ActorFactoryDefinedOverDefault.build(name='Diego')
        self.assertEqual('Diego', actor.name)

    def test_you_can_define_factory_for_in_init(self):
        actor = self.ActorFactory3.build(name='Daniel', FACTORY_FOR=Actor)
        self.assertEqual('Daniel', actor.name)
