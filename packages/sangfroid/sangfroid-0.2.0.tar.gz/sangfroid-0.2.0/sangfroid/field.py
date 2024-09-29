import logging
from enum import Enum
import bs4
import sangfroid.value as v

logger = logging.getLogger('sangfroid')

class Field:
    """
    An attribute of a Layer, which represents a value within
    a Synfig layer class.

    For example, a circle has a radius, so Circle layers
    have a Field attribute named "radius".

    Field itself is an abstract superclass, because field
    data can be fetched in various ways. Each way has its
    own subclass, defined later in this file.

    Attributes:
        type_ (type): the permissible type of this value.
            Note the underscore, to avoid a clash with the
            reserved word. This value can live either within
            builtins (such as float or int), or within
            the `sangfroid.value` package..
        default (type_): the default value. This is what
            you get if you create a new Layer and
            don't specify any other value.
        name (str): the name of this layer, such as "radius".
            Usually we figure this out automatically, but
            you can specify it in the constructor because
            sometimes the name we want to use is a
            reserved word.
        owner (any): the class this Field lives in.
        doc (str): the docstring. (Should this live here?)

    """
    def __init__(self,
                 type_,
                 default,
                 name = None,
                 doc = None,
                 ):
        self.type_ = type_
        self.default = default
        self.name = name
        self.owner = None
        self.doc = doc

        self.__doc__ = doc or ''
        self.__doc__ += f"\n\nType: {type_.__name__}"
        if default is not None:
            # yes, this is the right way round; think about it
            self.__doc__ += ' or None'

        if issubclass(type_, Enum):
            self.__doc__ += '\n\nPossible values (integer or constants):\n\n'

            max_length = max([len(s) for s in type_.__members__],
                             default=0)

            self.__doc__ += '\n'.join([
                '%4d %*s %s' % (
                    i,
                    max_length,
                    s,
                    '...', # doc, FIXME
                    )
                for i, s in enumerate(type_.__members__)])

    def __set_name__(self, owner, name):
        self.owner = owner
        if self.name is None:
            self.name = name

    def __get__(self, obj, obj_type=None):
        raise NotImplementedError()

    def __set__(self, obj, value):
        raise NotImplementedError()

    def __str__(self):

        result = f'[{self.__class__.__name__}'

        result += '%20s of %20s (%20s)' % (
                self.name,
                self.owner.__name__,
                self.type_,)

        result += ']'

        return result

    __repr__ = __str__

class NotImplementedField(Field):
    """
    A Field we haven't implemented yet.

    You're welcome to load or save the layer, but attempting
    to access the value within Python will throw
    NotImplementedError.

    Attributes:
        typename (str): the name of the type which doesn't exist.
    """
    def __init__(self, typename = None):
        super().__init__(
                type_ = str,
                default = None,
                )
        self.typename = typename

    def _throw_not_implemented(self):
        if self.typename is None:
            raise NotImplementedError(
                    f"The type {self.owner} has not been "
                    "implemented yet. Patches welcome.")
        else:
            raise NotImplementedError(
                    f"The type {self.owner} requires a value "
                    f"of type f{self.type_}, but that hasn't been "
                    "implemented yet. Patches welcome.")

    def __get__(self, obj, obj_type=None):
        self._throw_not_implemented()

    def __set__(self, obj, value):
        self._throw_not_implemented()

class TagAttrField(Field):
    """
    A Field found in the attributes of a tag.

    For example, in
    ```
    <layer active="true" ...>
    ```

    the field `active` is a tag attribute field.

    Usually, the `type_` of a tag attribute field must be `str`,
    because it's encoded in an XML attribute. If you set the
    attribute `type_override` to another type, the string
    will be coerced to and from that type.

    Attributes:
        type_override (builtin type): the type you want to set and get,
            even though the attribute itself is a string.
            If you pass None to the constructor, this will
            be set to the same value as `type_`.
    """

    def __init__(self,
                 *args,
                 type_override = None,
                 **kwargs):

        super().__init__(*args, **kwargs)

        self.type_override = type_override or self.type_
        assert self.type_override.__module__=='builtins', self.type_override

    def __get__(self, obj, obj_type=None):

        if self.name not in obj._tag.attrs:
            logger.debug("no %s field; returning default: %s",
                         self.name,
                         self.default,
                         )
            return self.default

        value = obj._tag.get(self.name)
        logger.debug("%s field is %s",
                     self.name,
                     value,
                     )

        if value is None:
            return None
        elif issubclass(self.type_override, bool):
            return str(value).lower()=='true'
        else:
            return self.type_override(value)

    def __set__(self, obj, value):
        if issubclass(self.type_override, bool):
            if value:
                value = 'true'
            else:
                value = 'false'
        else:
            value = self.type_override(value)

        obj._tag[self.name] = value

class ParamTagField(Field):
    """
    A Field which lives in a `<param>` tag within its layer.

    The `type_` field cannot be a builtin type. It should be
    a class from the `sangfroid.value` package, because we'll
    need to encode and decode it from XML.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.type_.__module__!='builtins', self.type_

    def _get_value(self, obj):
        holder = obj._tag.find('param',
                               attrs={
                                   'name': self.name,
                                   },
                               )

        if holder is None:
            raise AttributeError(self.name)

        contents = [t for t in holder.children
                    if isinstance(t, bs4.Tag)]
        if len(contents)!=1:
            raise ValueError(
                    "Param tags should have one child tag, which holds "
                    "the value of the param. However, this tag:\n\n"
                    f"{obj.tag}\n\n"
                    f"contains {len(contents)}.")

        result = v.Value.from_tag(contents[0])
        return result

    def __get__(self, obj, obj_type=None):
        result = self._get_value(obj)
        assert isinstance(result, self.type_), f"{result} {type(result)} {self.type_}"
        return result

    def __set__(self, obj, value):
        value_obj = self._get_value(obj)
        value_obj.value = value

class TagField(Field):
    """
    A Field representing the XML tag of the layer itself.

    Read-only.
    """
    def __init__(self):
        super().__init__(
                name = 'tag',
                type_ = bs4.Tag,
                default = None,
                doc = """The BeautifulSoup tag behind this item.""",
                )
 
    def __get__(self, obj, obj_type=None):
        return obj._tag

    def __set__(self, obj, value):
        raise KeyError("You can't put a different tag into an object.")

class NamedChildField(Field):
    """
    A Field which lives in a child tag of the layer, where the
    name of the child tag is the same as the field's name.

    For example, if the name was "wombat", the XML might look
    like this:

    ```
    <layer>
      <wombat>
        whatever the value is
      </wombat>
    </layer>
    """
    def __init__(self, type_, default, name=None, doc=None):
        super().__init__(
                type_ = type_,
                default = default,
                name = name,
                doc = doc,
                )

    def get_subtag_for_obj(self, obj):
        return obj._tag.find(self.name)
 
    def __get__(self, obj, obj_type=None):

        subtag = self.get_subtag_for_obj(obj)

        if subtag is None:
            return ''
        else:
            return subtag.string

    def __set__(self, obj, value):

        subtag = self.get_subtag_for_obj(obj)

        subtag.string = value

"""
A field which accesses a key in the value of another field.

For example, `g.offset` might be short for
`g.transformation['offset']`.

Use the `include_from` decorator classmethod to introduce
these fields from an existing field.
"""
class ShortcutField(Field):
    def __init__(self, upstream, upstream_field,
                 ):
        self.upstream = upstream
        self.name = upstream_field

    def __get__(self, obj, obj_type=None):
        v = self.upstream.__get__(obj, obj_type)
        result = v[self.name]
        return result

    def __set__(self, obj, value):
        self.upstream.__set__(obj,
                              {
                                  self.name: value,
                                  })

    """
    Decorator. Imports all the keys of the named field as
    ShortcutFields.

    Args:
        name (str): the name of the method to access

    Raises:
        AttributeError: if there is no field called `name`
        KeyError: if the keys already exist within the class
    """
    @classmethod
    def include_from(cls, name):
        def inner(c):
            try:
                a = c.__getattribute__(c, name)
            except AttributeError:
                raise AttributeError(
                        f"{c} has no attribute called {repr(name)}.\n"
                        f"But it does have: {' '.join(dir(c))}.")

            for subfield in a.type_._subfields():
                try:
                    print(c.__getattribute__(c, subfield))
                    raise KeyError(subfield)
                except AttributeError:
                    pass
                setattr(c, subfield,
                        cls(a, subfield))
            return c
        return inner

class BlendMethodField(ParamTagField):
    def __init__(self, foo):
        super().__init__(v.Real, -1)

class ParamArrayField(ParamTagField):
    pass

class SwitchCanvasField(NotImplementedField):
    pass

class DuplicatesIndexField(NotImplementedField):
    pass

class TypeNameField(TagAttrField):
    def __init__(self, *args, **kwargs):
        super().__init__(
                type_ = str,
                name = 'type',
                doc = (
                    "The name Synfig uses internally for this type of layer.\n"
                    "\n"
                    "In Python, you must spell this as `type_`, because\n"
                    "`type` is a reserved word."
                    ),
                default = None,
            )

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        self.default = owner.__name__.lower()

    def __set__(self, obj, value):
        raise ValueError("You can't change the name of a type.")

class SynfigVersionField(TagAttrField):
    def __init__(self, *args, **kwargs):
        super().__init__(
                type_ = float,
                name = 'version',
                doc = (
                    "The earliest version of Synfig which will interpret\n"
                    "the value of this field correctly."
                    ),
                default = None,
            )

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        self.default = owner.SYNFIG_VERSION

class DescField(TagAttrField):
    """
    A Field for the description of a layer.

    This is unlike most TagAttrFields because it can be None or ''
    with different meanings. If it's None, the layer has no desc
    attribute set. If it's '', the layer has desc=''.

    This is not used on the outermost Animation layer: "desc" there
    is a TagField.
    """

    def __init__(self):
        super().__init__(
                type_ = str,
                default = None,
                name = 'desc',
                doc = "A description of this field. Can be None.",
                )

    def __get__(self, obj, obj_type=None):

        if self.name not in obj._tag.attrs:
            return None
        else:
            return super().__get__(obj, obj_type)

    def __set__(self, obj, value):
        if value is None:
            del obj._tag[self.name]
        else:
            super().__set__(obj, value)
