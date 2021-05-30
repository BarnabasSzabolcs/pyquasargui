from typing import TYPE_CHECKING, Callable, List, Dict, Generic, TypeVar, Type

from quasargui.tools import print_error

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
    Data is all the data that can change
    in both the GUI and on the backend
    (typically the value of an Input)
    """
    max_id = 1
    model_dic: Dict[int, 'Model'] = {}
    NO_TYPE = (lambda x: x)

    def __init__(self, value: T, type_: Type or NO_TYPE = None):
        """
        :param value:
        :param type_: type of the model is enforced and the type is assumed to be the type of the initial value.
        To disable automatic type conversions, set type_=Model.NO_TYPE.
        """
        self.id = Model.max_id
        Model.max_id += 1
        self.model_dic[self.id] = self
        self._value = value
        self._type = type_ or type(value)
        self.api = None
        self._callbacks: List[CallbackType] = []
        self.modifiers = set()

    def __del__(self):
        del self.model_dic[self.id]

    def set_api(self, api: 'Api', _flush: bool = True):
        if self.api != api:
            self.api = api
            api.set_data(self.id, self._value)
        if _flush:
            api.flush_data(self.id)

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T):
        self.set_value(value)

    def set_value(self, value: T, _jsapi=False):
        if _jsapi:
            # noinspection PyBroadException
            try:
                value = self._type(value)
            except Exception:
                # if value == '' and self._type in {int, float}:
                #     value = self._type(0)
                if self.api.debug:
                    print(f'WARNING: could not convert {value} to {self._type}')
        if self._value == value:
            return
        self._value = value
        if self.api is not None and not _jsapi:
            self.api.set_data(self.id, self._value)
        for callback in self._callbacks:
            callback()
        if self.api is not None and not _jsapi:
            self.api.flush_data(self.id)

    @property
    def type(self):
        return self._type

    def set_type(self, type_: Type):
        self._type = type_

    def render_as_data(self) -> dict:
        data = {'@': self.id, 'value': self.value}
        if self.modifiers:
            data['modifiers'] = list(self.modifiers)
        return data

    def render_mustache(self) -> str:
        return "{{$root.data[" + str(self.id) + "]}}"

    def add_callback(self, fun: CallbackType):
        self._callbacks.append(fun)

    @property
    def callbacks(self) -> List[CallbackType]:
        return self._callbacks


class Computed(Reactive, Generic[T]):
    def __init__(self, fun: Callable[[...], T], *args: Reactive):
        self.fun = fun
        self.args = args
        self.model = Model(None)
        self.calculate()
        self.model.set_type(type(self.model.value))
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
