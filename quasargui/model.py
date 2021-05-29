from typing import TYPE_CHECKING, Any, Callable, Union, List, Dict

if TYPE_CHECKING:
    from quasargui.main import Api


class Renderable:

    def render(self):
        raise NotImplementedError

    @property
    def vue(self):
        raise NotImplementedError

    def set_api(self, api: 'Api'):
        raise NotImplementedError


class Model(Renderable):
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
        self.update_callbacks: List[Callable[[], None]] = []

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
        for callback in self.update_callbacks:
            callback()

    def render(self):
        return {'@': self.id, 'value': self.value}

    @property
    def vue(self) -> str:
        return "{{$root.data[" + str(self.id) + "]}}"


class Computed(Renderable):
    def __init__(self, fun: Callable[[...], Any], *args: Union[Model, 'Computed']):
        self.fun = fun
        self.args = args
        self.model = Model(None)
        self.calculate()
        self.model.update_callbacks = [computed.calculate for computed in args if isinstance(computed, Computed)]
        self.update_callbacks = self.model.update_callbacks
        for arg in args:
            if isinstance(arg, Model) or isinstance(arg, Computed):
                arg.update_callbacks.append(self.calculate)

    def calculate(self):
        values = [a.value for a in self.args]
        self.model.value = self.fun(*values)

    @property
    def value(self):
        return self.model.value

    def render(self):
        return self.model.render()

    @property
    def vue(self) -> str:
        return self.model.vue

    def set_api(self, api: 'Api'):
        self.model.set_api(api)
