import datetime
from typing import TYPE_CHECKING, Callable, List, Dict, Generic, TypeVar

from quasargui.tools import print_error, get_path, set_path_value
from quasargui.typing import ValueType, PathType, PathSegmentType

if TYPE_CHECKING:
    from quasargui.main import Api


T = TypeVar('T')
CallbackType = Callable[[], None]


class Reactive(Generic[T]):

    @property
    def value(self) -> T:
        raise NotImplementedError

    def render_as_data(self) -> dict:
        raise NotImplementedError

    def render_mustache(self) -> str:
        raise NotImplementedError

    def set_api(self, api: 'Api', _flush: bool = True):
        raise NotImplementedError

    def add_callback(self, fun: CallbackType):
        raise NotImplementedError

    @property
    def callbacks(self) -> List[CallbackType]:
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
    max_id = 1
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
            self.id = Model.max_id
            Model.max_id += 1
            Model.model_dic[self.id] = self
            Model.model_dependent_count[self.id] = 1
            self._value = value
        self._path = _path or []
        if to_python is not None:
            self.to_python = to_python
        elif type(value) not in {dict, list}:
            self.to_python = type(value)
        else:
            self.to_python = self.no_conversion
        self.from_python = from_python or self.no_conversion
        self.api = None
        self._callbacks: List[CallbackType] = []
        self.modifiers = set()

    def __del__(self):
        Model.model_dependent_count[self.id] -= 1
        if Model.model_dependent_count.get(self.id, 0) == 0:
            del self.model_dic[self.id]

    def set_api(self, api: 'Api', _flush: bool = True):
        if self.api == api:
            return
        self.api = api
        if self._path:
            Model.model_dic[self.id].set_api(api, _flush)
            return
        api.set_model_data(self.id, self._path, self.from_python(self.value))
        if _flush:
            api.flush_data(self.id)

    def __getitem__(self, item) -> 'Model':
        return Model(_id=self.id, _path=self._path + [item])

    def __setitem__(self, key: PathSegmentType, value: any):
        self.value[key] = value

    @property
    def value(self) -> T:
        if not self._path:
            return self._value
        else:
            return get_path(self.model_dic[self.id]._value, self._path)

    @value.setter
    def value(self, value: T):
        self.set_value(value)

    def set_value(self, value: T, _jsapi=False):

        def _set_value(val):
            if not self._path:
                self._value = val
            else:
                set_path_value(self.model_dic[self.id]._value, self._path, val)

        if _jsapi:
            # noinspection PyBroadException
            try:
                value = self.to_python(value)
            except Exception:
                # if value == '' and self._type in {int, float}:
                #     value = self._type(0)
                if self.api is not None and self.api.debug:
                    print(f'WARNING: could not convert {value} using {self.to_python}')
        if self.value == value:
            return
        _set_value(value)
        if self.api is not None and not _jsapi:
            self.api.set_model_data(self.id, self._path, self.from_python(self._value))
        for callback in self._callbacks:
            callback()
        if self.api is not None and not _jsapi:
            self.api.flush_data(self.id)

    def set_conversion(self, to_python: Callable[[ValueType], T], from_python: Callable[[T], ValueType] = None):
        self.to_python = to_python
        if from_python:
            self.from_python = from_python

    def render_as_data(self) -> dict:
        data = {'@': self.id}
        if self._path:
            data['path'] = self._path
        else:
            data['value'] = self.from_python(self._value)
        if self.modifiers:
            data['modifiers'] = list(self.modifiers)
        return data

    def render_mustache(self) -> str:
        if self._path:
            path = ''.join(f'["{p}"]' for p in self._path)
            return "{{$root.data[" + str(self.id) + "]" + path + "}}"
        else:
            return "{{$root.data[" + str(self.id) + "]}}"

    def add_callback(self, fun: CallbackType):
        self._callbacks.append(fun)

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


class Computed(Reactive, Generic[T]):
    """
    Computed values are updated automatically whenever their arguments
    (Models or other Computed) change.
    """
    def __init__(self, fun: Callable[[...], T], *args: Reactive):
        self.fun = fun
        self.args = args
        self.model = Model(None)
        self.calculate()
        self.model.set_conversion(type(self.model.value))
        for arg in args:
            if isinstance(arg, Reactive):
                arg.add_callback(self.calculate)

    def calculate(self):
        values = [a.value for a in self.args]
        try:
            self.model.value = self.fun(*values)
        except Exception as e:
            print_error(e)

    @property
    def value(self) -> T:
        return self.model.value

    def render_as_data(self) -> dict:
        return self.model.render_as_data()

    def render_mustache(self) -> str:
        return self.model.render_mustache()

    def set_api(self, api: 'Api', _flush: bool = True):
        self.model.set_api(api, _flush=_flush)

    def add_callback(self, fun: CallbackType):
        self.model.add_callback(fun)

    @property
    def callbacks(self) -> List[CallbackType]:
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
