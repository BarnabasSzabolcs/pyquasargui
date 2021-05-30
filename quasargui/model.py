from typing import TYPE_CHECKING, Any, Callable, List, Dict

if TYPE_CHECKING:
    from quasargui.main import Api


class Reactive:

    @property
    def value(self) -> str:
        raise NotImplementedError

    def render_as_data(self):
        raise NotImplementedError

    @property
    def vue(self):
        raise NotImplementedError

    def set_api(self, api: 'Api'):
        raise NotImplementedError

    def add_callback(self, fun: Callable[[], None]):
        raise NotImplementedError

    @property
    def callbacks(self):
        raise NotImplementedError


class Model(Reactive):
    """
    Data is all the data that can change
    in both the GUI and on the backend
    (typically the value of an Input)
    """
    max_id = 1
    model_dic: Dict[int, 'Model'] = {}

    def __init__(self, value):
        self.id = Model.max_id
        Model.max_id += 1
        self.model_dic[self.id] = self
        self._value = value
        self.api = None
        self._callbacks: List[Callable[[], None]] = []

    def __del__(self):
        del self.model_dic[self.id]

    def set_api(self, api: 'Api'):
        if self.api != api:
            self.api = api
            api.set_data(self.id, self._value)

    @property
    def value(self) -> str:
        if self.api is not None:
            return self.api.get_data(self.id)
        else:
            return self._value

    @value.setter
    def value(self, value):
        self.set_value(value)

    def set_value(self, value, _jsapi=False):
        if self._value == value:
            return
        self._value = value
        if self.api is not None and not _jsapi:
            self.api.set_data(self.id, self._value)
        for callback in self._callbacks:
            callback()

    def render_as_data(self):
        return {'@': self.id, 'value': self.value}

    @property
    def vue(self) -> str:
        return "{{$root.data[" + str(self.id) + "]}}"

    def add_callback(self, fun: Callable[[], None]):
        self._callbacks.append(fun)

    @property
    def callbacks(self):
        return self._callbacks


class Computed(Reactive):
    def __init__(self, fun: Callable[[...], Any], *args: Reactive):
        self.fun = fun
        self.args = args
        self.model = Model(None)
        self.calculate()
        for arg in args:
            if isinstance(arg, Reactive):
                arg.add_callback(self.calculate)

    def calculate(self):
        values = [a.value for a in self.args]
        self.model.value = self.fun(*values)

    @property
    def value(self):
        return self.model.value

    def render_as_data(self):
        return self.model.render_as_data()

    @property
    def vue(self) -> str:
        return self.model.vue

    def set_api(self, api: 'Api'):
        self.model.set_api(api)

    def add_callback(self, fun: Callable[[], None]):
        self.model.add_callback(fun)

    @property
    def callbacks(self):
        return self.model.callbacks
