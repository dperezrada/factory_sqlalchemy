import inspect

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


class BaseFactory(object):
    @classmethod
    def build(cls, *args, **kwargs):
        cls._factory_arguments = {}

        # get arguments of FACTORY_FOR
        inspect_result = inspect.getargspec(cls.FACTORY_FOR.__init__)

        # case factory_for has a __init__ method defined
        if len(inspect_result.args) > 1:
            cls._get_factory_init_params(inspect_result, cls._factory_arguments)
        # get data from table definition
        else:
            cls._get_arguments_from_table(cls._factory_arguments)

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
    def _get_factory_init_params(cls, inspect_result, factory_arguments):
        for arg in inspect_result.args:
            if arg != 'self':
                factory_arguments[arg] = None

        # get defaults of FACTORY_FOR
        if inspect_result.defaults is not None:
            for key, value in zip(
                inspect_result.args[-len(inspect_result.defaults):],
                inspect_result.defaults
            ):
                factory_arguments[arg] = value

        # if value defined, set it
        for key, value in factory_arguments.iteritems():
            defined = cls.__dict__.get(key)
            if defined is not None:
                factory_arguments[key] = defined

    @classmethod
    def _get_arguments_from_table(cls, factory_arguments):
        for key in cls.FACTORY_FOR.__table__.columns.keys():
            defined = cls.__dict__.get(key)
            if defined is not None:
                factory_arguments[key] = defined
            else:
                factory_arguments[key] = None
