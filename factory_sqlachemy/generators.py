# -*- coding: utf-8 -*-
import datetime
import random
import sys

import sqlalchemy
from random_words import RandomWords


_get_class = lambda name: sqlalchemy.types.__getattribute__(name)
_types = [(_get_class(name), None) for name in sqlalchemy.types.__all__]
GENERATORS = dict(_types)


class Generator():
    def create(self, *args, **kargs):
        raise NotImplementedError("Should have implemented this")


rw = RandomWords()


class StringGenerator(Generator):
    def create(self):
        return rw.random_word()


class IntegerGenerator(Generator):
    def create(self):
        return random.randint(0, sys.maxint)


class DateTimeGenerator(Generator):
    def create(self):
        return datetime.datetime.now()


GENERATORS[_get_class('String')] = StringGenerator()
GENERATORS[_get_class('Integer')] = IntegerGenerator()
GENERATORS[_get_class('DateTime')] = DateTimeGenerator()
