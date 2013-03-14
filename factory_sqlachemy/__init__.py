# -*- coding: utf-8 -*-
import inspect

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from factory_sqlachemy.generators import GENERATORS


class BaseFactory(object):
    @classmethod
    def build(cls, *args, **kwargs):
        cls._factory_arguments = {}

        factory_for = None

        if kwargs.get('FACTORY_FOR'):
            factory_for = cls.FACTORY_FOR = kwargs.get('FACTORY_FOR')
            del kwargs['FACTORY_FOR']
        else:
            factory_for = cls.FACTORY_FOR

        # get arguments of FACTORY_FOR __init__
        inspect_init_factory = inspect.getargspec(factory_for.__init__)

        # set default values from FACTORY_FOR __init__ method
        if len(inspect_init_factory.args) > 1:  # self is one
            cls._set_factory_init_params(inspect_init_factory, cls._factory_arguments)

        # complete object from table definition
        cls._set_arguments_from_table(cls._factory_arguments)

        # set from kwargs
        for key, value in kwargs.iteritems():
            cls._factory_arguments[key] = value

        cls._instance = cls.FACTORY_FOR(**cls._factory_arguments)
        return cls._instance

    @classmethod
    def create(cls, *args, **kwargs):
        dbsession = cls._get_db_instance(kwargs)
        instance = cls.build(*args, **kwargs)
        dbsession.add(instance)
        dbsession.flush()
        return instance

    @classmethod
    def _get_db_instance(cls, kwargs):
        database_config = kwargs.get('_db')
        if database_config is not None:
            db_url = database_config.get('URL')
            del database_config['URL']
            engine = create_engine(db_url, **database_config)
            dbsession = scoped_session(
                sessionmaker(
                    autocommit=True,
                    autoflush=True,
                    expire_on_commit=False,
                    bind=engine
                )
            )
            del kwargs['_db']
        return dbsession

    @classmethod
    def _set_factory_init_params(cls, inspect_result, factory_arguments):
        factory_arguments_tmp = dict()
        for arg in inspect_result.args:
            if arg != 'self' and arg not in factory_arguments:
                factory_arguments_tmp[arg] = None

        # get defaults of FACTORY_FOR
        if inspect_result.defaults is not None:
            for key, value in zip(
                inspect_result.args[-len(inspect_result.defaults):],
                inspect_result.defaults
            ):
                if arg in factory_arguments_tmp:
                    factory_arguments[arg] = value

        # if value defined, set it
        for key, value in factory_arguments.iteritems():
            defined = cls.__dict__.get(key)
            if defined is not None:
                factory_arguments[key] = defined

    @classmethod
    def _set_arguments_from_table(cls, factory_arguments):
        for key in cls.FACTORY_FOR.__table__.columns.keys():
            defined = cls.__dict__.get(key)
            if key not in factory_arguments:
                if defined is not None:
                    factory_arguments[key] = defined
                else:
                    class_type = cls.FACTORY_FOR.__table__.columns[key].type
                    factory_arguments[key] = GENERATORS[class_type.__class__].create()
