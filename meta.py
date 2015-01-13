def equivalent_property(*names, **kwargs):
    def decorator(method):
        method.__equivalent_names = names
        method.__equivalent_default = kwargs.get('default')
        return method
    return decorator


import types
class EquivalentProperties(type):
    def __new__(cls, cls_name, cls_bases, cls_attrs):
        new_cls_attrs = {}
        for attr, method in cls_attrs.iteritems():
            if type(method) != types.FunctionType:
                # We can ignore properties.
                new_cls_attrs[attr] = method
            elif hasattr(method, '__equivalent_names'):
                names = method.__equivalent_names
                first_name = attr
                var_name = '__' + first_name
                new_cls_attrs[var_name] = method.__equivalent_default
                names = names + (attr,)
                for name in names:
                    # We need these bind_ function to deal with the otherwise
                    # late-binding of `var_name' and `method'.
                    def bind_getter(var_name):
                        def getter(self):
                            return getattr(self, var_name)
                        return getter
                    def bind_setter(var_name, method):
                        def setter(self, value):
                            value = method(self, value)
                            setattr(self, var_name, value)
                        return setter
                    prop = property(bind_getter(var_name))
                    prop = prop.setter(bind_setter(var_name, method))
                    new_cls_attrs[name] = prop
            else:
                # And we ignore methods which haven't been annotated with
                # `@equiv'.
                new_cls_attrs[attr] = method
        return super(EquivalentProperties, cls).__new__(cls, cls_name, cls_bases, new_cls_attrs)
