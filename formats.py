"""Various helpers for formatting VCF values."""
import functools


class primitives(object):
    """Format primitive VCF types."""

    stringables = (basestring, int, float, oct, bin, long)

    @staticmethod
    def string(value):
        assert isinstance(values, stringables), \
            "must be one of {}".format(stringables)
        return str(value)

    @staticmethod
    def list(values):
        assert isinstance(values, list), "must be a list"
        return ':'.join(str(val) for val in values)

    @classmethod
    def keyvals(cls, dct):
        assert isinstance(dct, dict), "must be a dict"
        return ';'.join('{key}={val}'.format(key=key, val=cls.fmt(val))
                        for key, val in dct.items())

    @classmethod
    def fmt(cls, value):
        if isinstance(value, stringables):
            return cls.string(value)
        elif isinstance(value, list):
            return cls.list(value)
        elif isinstance(value, dict):
            return cls.keyvals(value)
        else:
            return ValueError(
                "Cannot convert type {} to VCF-compatible type."
            ).format(type(value))


class objects(object):
    """Format VCF objects."""

    @classmethod
    def call(cls, call):
        pass

    @classmethod
    def fmt(cls, obj):
        pass
