# -*- coding: utf-8 -*-
import copy
import inspect

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from factory_sqlachemy.generators import GENERATORS


_table_classes = dict()
_factories = dict()


def add_class_table_to_factory(cls):
    _table_classes[cls.__tablename__] = cls
    return cls


class BaseFactory(object):
    @classmethod
    def build(cls, _db=None, *args, **kwargs):
        cls._factory_arguments = dict()

        # get arguments of FACTORY_FOR __init__
        inspect_init_factory = inspect.getargspec(cls.FACTORY_FOR.__init__)

        # set default values from FACTORY_FOR __init__ method
        if len(inspect_init_factory.args) > 1:  # self is one
            cls._set_factory_init_params(inspect_init_factory, cls._factory_arguments)

        # complete object from table definition
        cls._set_arguments_from_table(cls._factory_arguments, _db=_db)

        # set from kwargs
        for key, value in kwargs.iteritems():
            cls._factory_arguments[key] = value

        cls._instance = cls.FACTORY_FOR(**cls._factory_arguments)
        return cls._instance

    @classmethod
    def create(cls, _db=None, *args, **kwargs):
        dbsession = cls._get_db_instance(_db)
        instance = cls.build(_db=_db, *args, **kwargs)
        dbsession.add(instance)
        dbsession.flush()
        return instance

    @classmethod
    def _get_db_instance(cls, _db):
        database_config = copy.deepcopy(_db)
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
    def _set_arguments_from_table(cls, factory_arguments, _db=None):
        table = cls.FACTORY_FOR.__table__
        for key in table.columns.keys():
            defined = cls.__dict__.get(key)
            foreign_keys = table.columns[key].foreign_keys
            if len(foreign_keys) > 0:
                foreign_table_class_name = [x.target_fullname.split('.') for x in foreign_keys][0][0]
                ForeignKeyClass = _table_classes.get(foreign_table_class_name)
                ForeignKeyClassFactory = _factories.get(foreign_table_class_name)
                if ForeignKeyClassFactory is None:
                    class ForeignKeyClassFactory(BaseFactory):
                        FACTORY_FOR = ForeignKeyClass
                if _db is not None:
                    foreign_instance = ForeignKeyClassFactory.create(_db=_db)
                else:
                    foreign_instance = ForeignKeyClassFactory.build()
                factory_arguments[key] = foreign_instance.id
            if key not in factory_arguments:
                if defined is not None:
                    factory_arguments[key] = defined
                else:
                    class_type = table.columns[key].type
                    factory_arguments[key] = GENERATORS[class_type.__class__].create()
