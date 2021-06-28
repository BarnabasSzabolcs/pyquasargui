import datetime
from abc import ABCMeta
from typing import TYPE_CHECKING, Callable, List, Dict, Generic, TypeVar, Union

from quasargui.tools import print_error, get_path, set_path_value
from quasargui.typing import ValueType, PathType, PathSegmentType

if TYPE_CHECKING:
    from quasargui.main import Api

T = TypeVar('T')
CallbackType = Callable[[], None]


class Renderable:
    def render_as_data(self) -> dict:
        raise NotImplementedError

    def render_mustache(self) -> str:
        return "{{" + self.js_var_name + "}}"

    @property
    def js_var_name(self) -> str:
        raise NotImplementedError


class Reactive(Renderable, Generic[T], metaclass=ABCMeta):

    @property
    def value(self) -> T:
        raise NotImplementedError

    def add_callback(self, fun: CallbackType):
        raise NotImplementedError

    @property
    def callbacks(self) -> List[CallbackType]:
        raise NotImplementedError

    def set_api(self, api: 'Api', _flush: bool = True):
        raise NotImplementedError

    def remove_api(self):
        raise NotImplementedError


class Model(Reactive, Generic[T]):
    """
    Model handles data that can change
    both in the frontend and the backend
    (typically the value of an Input)

    There are two types of Model's,
    Model's with and without path.
    If a Model has no path, it stores value,
    a Model with path represents access to a "deep" value.
    Model's with path have a path-less counterpart that manages the value handling.
    """
    max_id = 0
    model_dic: Dict[int, 'Model'] = {}
    model_dependent_count: Dict[int, int] = {}

    @staticmethod
    def no_conversion(value):
        return value

    def __init__(self, value: T = None,
                 to_python: Callable[[ValueType], T] = None,
                 from_python: Callable[[T], ValueType] = None,
                 _id: int = None,
                 _path: PathType = None
                 ):
        if _id is not None:
            self.id = _id
            if value is not None:
                raise AssertionError
            Model.model_dependent_count[self.id] += 1
        else:
            Model.max_id += 1
            self.id = Model.max_id
            Model.model_dic[self.id] = self
            Model.model_dependent_count[self.id] = 1
            self._value = value
        self.path = _path or []
        if to_python is not None:
            self.to_python = to_python
        elif type(value) not in {dict, list}:
            self.to_python = type(value)
        else:
            self.to_python = self.no_conversion
        self.from_python = from_python or self.no_conversion
        self.api = None
        self._callbacks: List[CallbackType] = []
        self._immediate_callbacks: List[CallbackType] = []
        self.modifiers = set()

    def __del__(self):
        Model.model_dependent_count[self.id] -= 1
        if Model.model_dependent_count.get(self.id, 0) == 0:
            del self.model_dic[self.id]

    def set_api(self, api: 'Api', _flush: bool = True):
        if self.api == api:
            return
        self.api = api
        if self.path:
            Model.model_dic[self.id].set_api(api, _flush)
            return
        api.set_model_data(self.id, self.path, self.from_python(self.value))
        for cb in self._immediate_callbacks:
            cb()
        if _flush:
            api.flush_model_data(self.id)

    def remove_api(self):
        self.api = None
        if self.path:
            Model.model_dic[self.id].remove_api()

    def __getitem__(self, item) -> 'Model':
        return Model(_id=self.id, _path=self.path + [item])

    def __setitem__(self, key: PathSegmentType, value: any):
        self.value[key] = value

    @property
    def value(self) -> T:
        if not self.path:
            return self._value
        else:
            return get_path(self.model_dic[self.id]._value, self.path)

    @value.setter
    def value(self, value: T):
        self.set_value(value)

    def set_value(self, value: T, _jsapi=False):

        def _set_value(val):
            if not self.path:
                self._value = val
            else:
                set_path_value(self.model_dic[self.id]._value, self.path, val)

        if _jsapi:
            # noinspection PyBroadException
            try:
                value = self.to_python(value)
            except Exception:
                # if value == '' and self._type in {int, float}:
                #     value = self._type(0)
                if self.api is not None and self.api.debug:
                    print('WARNING: could not convert {value} using {converter}'.format(
                        value=value, converter=self.to_python))
        if self.value == value:
            return
        _set_value(value)
        self.update(_jsapi)

    def update(self, _jsapi=False):
        if self.api is not None and not _jsapi:
            self.api.set_model_data(self.id, self.path, self.from_python(self._value))
        for callback in self._callbacks:
            callback()
        if self.api is not None and not _jsapi:
            self.api.flush_model_data(self.id)

    def set_conversion(self, to_python: Callable[[ValueType], T], from_python: Callable[[T], ValueType] = None):
        self.to_python = to_python
        if from_python:
            self.from_python = from_python

    def render_as_data(self) -> dict:
        data = {'@': self.id}
        if self.path:
            data['path'] = self.path
        else:
            data['value'] = self.from_python(self._value)
        if self.modifiers:
            data['modifiers'] = list(self.modifiers)
        return data

    @property
    def js_var_name(self):
        if self.path:
            path = ''.join('["{}"]'.format(p) for p in self.path)
        else:
            path = ''
        return "$root.data[" + str(self.id) + "]" + path

    def add_callback(self, fun: CallbackType, immediate: bool = True):
        """
        :param fun:
        :param immediate: call callback when api is added
        :return:
        """
        self._callbacks.append(fun)
        if immediate:
            self._immediate_callbacks.append(fun)

    @property
    def callbacks(self) -> List[CallbackType]:
        return self._callbacks


class DateTimeModel(Model[datetime.datetime]):
    def __init__(self, value: datetime.datetime):
        super().__init__(value, self._to_python, self._from_python)

    @staticmethod
    def _to_python(s):
        try:
            return datetime.datetime.fromisoformat(s.replace('/', '-').replace('.', '-'))
        except ValueError:
            return None

    @staticmethod
    def _from_python(dt):
        try:
            return dt.isoformat(sep=' ').rsplit('.', 1)[0]
        except AttributeError:
            return None


class PropVar(Renderable):
    """
    PropVar is the substitution for Model when a function is passed to a Slot's children parameter,
    instead of an array (eg. Table, QTree).
    PropVar can be considered as a limited version of a Model.
    It has item accessors and can be used exactly as models, except they cannot be get/set a value directly.

    Internally, prop's are rendered as prop1, prop2 etc,
    with prop paths as prop1['path']['subpath'][0] etc.
    PropVar's appear when a Slot receives a function as children, and with VFor.
    PropVar's are invisible for the users.
    """
    max_id = 0

    def __init__(self, _id: int = None, _path: PathType = None):
        if _id is not None:
            self.id = _id
            if _path is None:
                raise AssertionError
            self.path = _path
        else:
            PropVar.max_id += 1
            self.id = PropVar.max_id
            if _path is not None:
                raise AssertionError
            self.path = []

    def __getitem__(self, item) -> 'PropVar':
        return PropVar(_id=self.id, _path=self.path + [item])

    def render_as_data(self) -> dict:
        return {'@p': 'prop{}'.format(self.id), 'path': self.path}

    @property
    def js_var_name(self):
        if self.path:
            path = ''.join("['{}']".format(p) for p in self.path)
        else:
            path = ''
        return 'prop{}{}'.format(self.id, path)


class Computed(Reactive, Generic[T]):
    """
    Computed values are updated automatically whenever their arguments
    (Models or other Computed) change.
    Also, Computed values are independently calculated for PropVars when necessary.

    Do not use Computed with PropVars outside a children argument's callable value.

    see: quasargui/examples/prop_vars.py
    """
    max_id = 0
    computed_dic: Dict[int, 'Computed'] = {}

    def __init__(self, fun: Callable, *args: Union[Reactive, PropVar]):
        """
        :param fun: is assumed to be an idempotent function (that its value changes only if args changes)
        :param args:
        """
        Computed.max_id += 1
        self.id = self.max_id
        Computed.computed_dic[self.id] = self
        self.fun = fun
        if not all(isinstance(arg, Reactive) or isinstance(arg, PropVar) for arg in args):
            raise AssertionError('args have to be Reactive or PropVar.')
        self.props = any(isinstance(arg, PropVar) for arg in args)
        self.args = args
        if not self.props:
            self.model = Model(None)
            self.calculate()
            self.model.set_conversion(type(self.model.value))
            for arg in args:
                arg.add_callback(self.calculate)

    def calculate(self):
        if self.props:
            raise AssertionError('calculate can be only called if the object does not depend on PropVar')
        values = [a.value for a in self.args]
        try:
            self.model.value = self.fun(*values)
        except Exception as e:
            print_error(e)

    @classmethod
    def _calculate_for_props_value(cls, computed_id: int, props: any):
        return cls.computed_dic[computed_id].fun(*props)

    @property
    def value(self) -> T:
        if self.props:
            raise AssertionError('value works only if the object does not depend on PropVar')
        return self.model.value

    @property
    def js_var_name(self) -> str:
        """
        scoped Slots come with a callable children argument.
        The callable children argument is called with a PropVar,
        but it does not represent a single component but a component template.
        Therefore the Computed represents multiple arguments instead of a single one.
        """
        if not self.props:
            return self.model.js_var_name
        # noinspection PyTypeChecker
        var_names = [arg.js_var_name for arg in self.args]
        arg_list = ', '.join(var_names)
        return "calculateWithProp({}, {}).value".format(self.id, arg_list)

    def render_as_data(self) -> dict:
        if not self.props:
            return self.model.render_as_data()
        else:
            return {'$': self.js_var_name}

    def set_api(self, api: 'Api', _flush: bool = True):
        if not self.props:
            self.model.set_api(api, _flush=_flush)

    def remove_api(self):
        if not self.props:
            self.model.remove_api()

    def add_callback(self, fun: CallbackType):
        if self.props:
            raise AssertionError('Callbacks work only if the object does not depend on PropVar')
        self.model.add_callback(fun)

    @property
    def callbacks(self) -> List[CallbackType]:
        if self.props:
            raise AssertionError('Callbacks work only if the object does not depend on PropVar')
        return self.model.callbacks


class Not(Computed):
    def __init__(self, var: Reactive):
        super().__init__(lambda x: not x, var)


class And(Computed):
    def __init__(self, *arguments: Reactive):
        super().__init__(lambda *args: all(args), *arguments)


class Or(Computed):
    def __init__(self, *arguments: Reactive):
        super().__init__(lambda *args: any(args), *arguments)


class TrueFalse(Computed):
    def __init__(self, true_value, false_value, argument: Reactive):
        super().__init__(lambda a: true_value if a else false_value, argument)
