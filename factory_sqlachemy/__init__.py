import inspect


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
        instance = cls.build(*args, **kwargs)
        #  TODO: pass session
        # database = instance.metadata._bind.url.database.replace('test_', '')
        # dbsessions[database].add(instance)
        # dbsessions[database].flush()
        return instance

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
