import copy
import bs4
import functools
import copy
from sangfroid.registry import Registry
from sangfroid.t import T

class Value:

    ANIMATED = 'animated'

    def __init__(self, *args):

        if len(args)==1 and isinstance(args[0], bs4.element.Tag):
            self._tag = args[0]
        else:
            self._tag = self._get_empty_tag()
            if len(args)==1:
                self.value = args[0]
            else:
                self.value = args

        assert self._tag is not None

    @classmethod
    def _get_empty_tag(cls, name=None):
        name = name or cls.get_name_for_tag()
        result = bs4.Tag(name=name)
        return result

    @property
    def tag(self):
        return self._tag

    @property
    def is_animated(self):
        """
        Whether the value is animated.

        Returns:
            bool
        """
        return self._tag.name==self.ANIMATED

    @is_animated.setter
    def is_animated(self, v):
        self._set_animated(v)

    def _set_animated(self,
                      whether,
                      adjust_contents = True,
                      ):
        whether = bool(whether)
        if whether==self.is_animated:
            pass
        elif whether:

            if adjust_contents:
                former_value = self.value

            our_type = self._tag.name
            self._tag.attrs = {}
            self._tag.name = self.ANIMATED
            self._tag['type'] = our_type

            if adjust_contents:
                self._tag.clear()
                self.timeline[0] = former_value
        else:

            if adjust_contents:
                timeline = self.timeline
                first_value = timeline.values()[0]
            else:
                first_value = None

            self._tag.clear()

            new_tag = self._get_empty_tag()
            self._tag.replace_with(new_tag)
            self._tag = new_tag

            if first_value is not None:
                old_tag = self._tag

                self._tag = copy.deepcopy(first_value.value._tag)
                if old_tag.parent is not None:
                    old_tag.replace_with(self._tag)

    @property
    def timeline(self):
        result = Timeline.__new__(Timeline)
        result.parent = self
        return result

    @timeline.setter
    def timeline(self, v):

        if isinstance(v, list) and all([n for n in v if isinstance(n, Waypoint)]):
            self._set_waypoints(v)
        elif isinstance(v, dict):
            self.timeline = list(v.values())
        elif isinstance(v, Timeline):
            if v.parent is self:
                return
            self._set_waypoints(v.values())
        else:
            raise TypeError("A timeline can only be set to another timeline or "
                            "a dict or list of Waypoints.")

    def _waypoint_tags(self):
        """
        A list of Beautiful Soup tags of waypoints on our timeline.

        The list is in the same order it appears in the file.
        If we're not animated, the list will have no members.

        Returns:
            list of Tag
        """

        if self._tag.name!=Value.ANIMATED:
            return []

        result = [wt for wt in self._tag
                  if isinstance(wt, bs4.element.Tag)]

        return result

    def _waypoints(self):
        """
        A dict of Waypoints on our timeline.

        If we're not animated, the dict will have no members.

        Returns:
            dict mapping T to Waypoint
        """

        waypoints = self._waypoint_tags()

        if not waypoints:
            return {}

        our_type = self._tag['type']

        values = [Waypoint.from_tag(wt,
                                    our_type = our_type,
                                    )
                  for wt in waypoints]

        result = dict([(v.time, v) for v in values])

        return result

    def _set_waypoints(self, v):
        """
        Sets our timeline to contain exactly the given sequence of waypoints.

        They will be stored sorted, with newlines between them.

        This necessarily involves setting whether we're animated.

        Args:
            v (list of Waypoints): the waypoints.
        """

        if not v:
            self._set_animated(
                    whether = False,
                    )
            return

        self._set_animated(
                whether = True,
                adjust_contents = False,
                )
        self._tag.clear()

        for i, w in enumerate(sorted(v)):
            if i!=0:
                self._tag.append('\n')
            self._tag.append(w.tag)

    def __len__(self):
        return len(self._waypoints())

    @property
    def our_type(self):
        """
        The name of the Synfig layer type.

        For example, 'circle' or 'group'.

        Returns:
            str
        """
        result = self._tag.name
        if result==Value.ANIMATED:
            result = self._tag['type']

        return result

    def _str_inner(self):
        return str(self.value)

    def __str__(self):
        if self.is_animated:
            return '(animated)'
        else:
            return self._str_inner()

    def __repr__(self):
        return '['+self.__class__.__name__+' '+str(self)+']'

    @classmethod
    def _subfields(cls):
        """
        Returns a set of names of keys
        generally found within values of this class.

        Used by sangfroid.layer.include_shortcuts().

        Returns:
            set
        """
        return set()

    @property
    def value(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.value == other.value

        return self.value == other

    def as_python_expression(self):
        """
        A Python expression which could be passed to the constructor
        of this class in order to recreate this value.

        Used by `etc/pick-and-mix-to-layers.py`.
        """
        return str(self)

    @classmethod
    def get_name_for_tag(cls):
        return cls.__name__.lower()

    ########################

    # Factories, and setup for factories

    handles_type = Registry()

    @classmethod
    def from_tag(cls, tag,
                 ):

        if tag.name==cls.ANIMATED:

            type_name = tag['type']
            if type_name is None:
                raise ValueError(f"Animated values need a type: {tag}")

        else:
            type_name = tag.name

        result_type = cls.handles_type.from_name(name=type_name)
        result = result_type._construct_from(tag)

        return result

    @classmethod
    def _construct_from(cls, tag):
        return cls(tag)

#######################

class Timeline:
    r"""
    A wrapper for a Value, giving access to its Waypoints.

    This can't be created directly; it should only be created by
    a Value. It holds no state of its own, other than the reference
    to the Value which created it.

    Fields:
        parent (Value): the Value which created this Timeline
    """

    def __init__(self):
        raise NotImplementedError(
                "Don't construct timelines directly."
                )

    def __iter__(self):
        for t,w in sorted(self.parent._waypoints().items()):
            yield w

    def _ensure_fps(self, t):
        if isinstance(t, (int, float, str)):
            return T(t, ref = self.parent._tag)
        elif isinstance(t, T):
            if t._fps is None:
                return T(t._frames, self.parent._tag)
            else:
                return t
        else:
            raise TypeError("I need T, or an int, float, str to create a T. "
                    f"You gave me {type(t)}.")

    def keys(self):
        return list(self.parent._waypoints().keys())

    def values(self):
        return list(self.parent._waypoints().values())

    def items(self):
        return list(self.parent._waypoints().items())

    def __iadd__(self, waypoints):
        self.add(waypoints,
            overwrite = True,
                 )

    def add(self, waypoints,
            overwrite = False,
            ):

        def raise_argument_error():
            raise TypeError(
                    "The argument to add() "
                    "must be either a Waypoint or a list of Waypoints.")

        if isinstance(waypoints, Waypoint):
            waypoints = [waypoints]
        elif isinstance(waypoints, list):
            pass
        else:
            raise_argument_error()

        # check they're sensible
        for w in waypoints:
            if not isinstance(w, Waypoint):
                raise_argument_error()
            elif not isinstance(w.tag, bs4.Tag):
                raise TypeError(
                        f'{w} has a tag of type {type(w.tag)}')

        existing = self.parent._waypoints()
        clashes = [
            (old.time, new.time)
                for old in existing.values()
                for new in waypoints
                if old.time==new.time
                ]

        if overwrite:
            for old, _ in clashes:
                del existing[old]
        elif clashes:
            raise ValueError("There are already Waypoints with those "
                             "times in this timeline:\n"
                             f"{clashes}")

        self.parent.is_animated = True

        existing |= dict([(w.time, w) for w in waypoints])

        self.parent.tag.clear()

        for w in sorted(existing.values()):
            self.parent.tag.append(w.tag)

        return self

    def __getitem__(self, time):
        if 'x_y' in str(self.parent._tag):
            raise ValueError()
        for t, wt in self.parent._waypoints().items():
            if t==time:
                return wt
            elif t>time:
                raise KeyError(time)

        raise KeyError(time)

    def __setitem__(self, t, v):

        t = self._ensure_fps(t)

        if isinstance(v, Waypoint):
            new_waypoint = v
            new_waypoint.time = t
        elif isinstance(v, self.parent.__class__):
            new_waypoint = Waypoint(
                    time = t,
                    value = v,
                    ref = self.parent.tag,
                    )
        else:
            new_waypoint = Waypoint(
                    time = t,
                    value = self.parent.__class__(v),
                    ref = self.parent.tag,
                    )

        if not self.parent.is_animated:
            self.parent._tag.clear()
            self.parent._set_animated(
                    whether = True,
                    adjust_contents = False,
                    )

        waypoints = self.parent._waypoints()

        waypoints[t] = new_waypoint

        self.parent._set_waypoints(waypoints.values())

    def __delitem__(self, t):

        if isinstance(t, (int, float, str)):
            t = T(t, ref = self.parent._tag)
        elif isinstance(t, T):
            t = self._ensure_fps(t)

        waypoints = self.parent._waypoints()

        waypoints.__delitem__(t)

        self.parent._set_waypoints(waypoints.values())

    def __eq__(self, other):
        if isinstance(other, Timeline):
            return self.values()==other.values()
        else:
            return self.values()==list(other)

    def __str__(self):
        result = (
                f'[timeline of {self.parent.__class__.__name__}:'
                f'{self.parent._waypoints()}]'
                )
        return result

    def __len__(self):
        return len(self.keys())

    def __bool__(self):
        return len(self)!=0

    __repr__ = __str__

#######################

INTERPOLATION_TYPES = {
        # UI name    SVG name   emoji
        'tcb':      ('auto',     '🟢'),
        'clamped':  ('clamped',  '🔶'),
        'constant': ('constant', '🟥'),
        'linear':   ('linear',   '🌽'), # yeah, I know it's sweetcorn
        'ease':     ('halt',     '🫐'), # blueberry
        'undefined': (None,      '🪨'), # rock
        }

INTERPOLATION_TYPE_SYNONYMS = dict(
        [(v[0], k)
         for k,v in INTERPOLATION_TYPES.items()
         if v[0] is not None])

@functools.total_ordering
class Waypoint:
    def __init__(self, time, value, before='clamped', after='clamped',
                 ref = None,
                 ):

        if not isinstance(value, Value):
            raise TypeError(value)

        if value.is_animated:
            raise ValueError("Waypoints can't have animated values")

        if isinstance(time, T):
            self.time = time
        elif isinstance(time, (int, float, str)):
            self.time = T(time,
                          ref = ref,
                          )
        else:
            raise TypeError(
                    f"time parameter should be T, or numeric, or str: {time}")

        self._before = self._check_interpolation_type(before, True)
        self._after = self._check_interpolation_type(after, True)
        self.value = value

    @property
    def before(self):
        return self._before

    @before.setter
    def before(self, v):
        self._before = self._check_interpolation_type(v, False)

    @property
    def after(self):
        return self._after

    @after.setter
    def after(self, v):
        self._after = self._check_interpolation_type(v, False)

    @classmethod
    def _check_interpolation_type(cls, v, from_constructor):

        if v=='undefined':
            if from_constructor:
                raise ValueError(
                        "Waypoints can't have interpolations "
                        "of 'undefined'."
                        )
            else:
                raise ValueError(
                        "You can't set waypoint interpolations "
                        "to 'undefined'."
                        )

        if v in INTERPOLATION_TYPES:
            return v

        if v in INTERPOLATION_TYPE_SYNONYMS:
            return INTERPOLATION_TYPE_SYNONYMS[v]

        raise ValueError(f"Unknown interpolation type: {v}")

    @property
    def tag(self):
        result = bs4.Tag(name="waypoint")
        result['time'] = self.time
        result['before'] = self._before
        result['after'] = self._after
        result.append(
                copy.copy(
                    self.value.tag
                    )
                )
        return result

    @classmethod
    def from_tag(cls, tag,
                 our_type = None,
                 ):
        if tag.name!='waypoint':
            raise ValueError("Waypoints must be called <waypoint>: "
                                f"{tag}")

        try:
            time = T(tag['time'], ref=tag)
        except ValueError:
            raise ValueError(
                    "If a value isn't attached to a document, "
                    "T-values in its timeline must be"
                    "expressed in frames: {tag}"
                    )

        v = [t for t in tag.children if isinstance(t, bs4.element.Tag)]

        if len(v)==0:
            raise ValueError(f"Waypoint without a value: {w}")
        elif len(v)!=1:
            raise ValueError(
                    f"Waypoint with multiple values: {w}")
        elif v[0].name==Value.ANIMATED:
            raise ValueError("Values in waypoints cannot themselves "
                             "be animated")
        elif our_type is not None and v[0].name!=our_type:
            raise ValueError(
                    "Waypoint type must match parent: "
                    f"parent={our_type}, child={v[0].name}")

        result = cls(
                time = time,
                value = Value.from_tag(v[0]),
                before = tag['before'],
                after = tag['after'],
                )

        return result

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        if not isinstance(other, Waypoint):
            return False

        return self.time == other.time

    def __str__(self):
        return '[%3s ' % (self.time,) + (
                f'{INTERPOLATION_TYPES[self.before][1]}-'
                f'{INTERPOLATION_TYPES[self.after][1]} - '
                f'{self.value}]'
                )

    __repr__ = __str__

__all__ = [
        'Value',
        'Waypoint',
        ]
