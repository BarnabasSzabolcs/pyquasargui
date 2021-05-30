import json
from typing import List, Tuple

import webview
from webview import Window

from quasargui import QUASAR_GUI_INDEX_PATH
from quasargui.base import EventCallbacks
from quasargui.components import Component
from quasargui.model import Model
from quasargui.tools import print_error


class Api:
    """
    python -> js
    """
    def __init__(self, main_component: Component, debug: bool = False, render_debug: bool = False):
        self.main_component = main_component
        self.window = None
        self.debug = debug
        self.render_debug = render_debug
        self.set_data_queue = []

    def init(self, window):
        self.window = window
        window.evaluate_js('app.setDebug({render_debug})'.format(
            render_debug=json.dumps(self.render_debug)
        ))
        self.set_main_component(self.main_component)

    def set_main_component(self, component: Component):
        component.set_api(self)
        cmd = 'app.setMainComponent({component})'.format(
            component=json.dumps(component.vue)
        )
        if self.debug:
            print(cmd)
        self.window.evaluate_js(cmd)

    def get_data(self, data_id: int):
        return self.window.evaluate_js('app.getData({data_id})'.format(
            data_id=data_id
        ))

    def set_data(self, data_id: int, value):
        if self.debug:
            print('set_data', data_id, value)
        self.set_data_queue.append([data_id, value])

    def flush_data(self, data_id=0):
        if (not self.set_data_queue) or (data_id and self.set_data_queue[0][0] != data_id):
            return
        result = self.window.evaluate_js(
            'app.setData({payload})'.format(
                payload=json.dumps(self.set_data_queue)
            ))
        self.set_data_queue = []
        return result

    def set_component(self, component_vue):
        if self.debug:
            print('set_component', component_vue)
        return self.window.evaluate_js(
            'app.refreshComponent({component_vue})'.format(
                component_vue=json.dumps(component_vue)))

    def call_component_method(self, component_id: str, method: str):
        """
        eg. call_component_method(12, 'validate()')
        """
        return self.window.evaluate_js('app.callComponentMethod({params})'.format(
            params=json.dumps({'component_id': component_id, 'method': method})
        ))

    def send_notification(self, params: dict):
        return self.window.evaluate_js('app.showNotification({params})'.format(
            params=json.dumps(params)))


# noinspection PyMethodMayBeStatic
class JsApi:
    """
    js -> python
    """
    def call_cb(self, cb_id: int, params=None):
        fun = EventCallbacks.get(cb_id)
        nargs = fun.__code__.co_argcount
        if nargs == 0:
            try:
                fun()
            except Exception as e:
                print_error(e)
                raise e
        elif nargs == 1:
            try:
                fun(params)
            except Exception as e:
                print_error(e)
                raise e
        else:
            raise AssertionError('Callback {name} has wrong number of parameters ({n})'.format(
                name=fun.__name__,
                n=nargs
            ))

    def print_log(self, args):
        """
        callback for app for debug purposes
        """
        print(*args.values(), sep=' ', end='\n', flush=True)

    def set_model_value(self, model_id, value):
        try:
            Model.model_dic[int(model_id)].set_value(value, _jsapi=True)
        except Exception as e:
            print_error(e)
            raise e


WINDOW = 0
API = 1
window_api_list: List[Tuple[Window, Api]] = []


def run(component: Component, debug: bool = False, _render_debug: bool = False):
    api = Api(component, debug=debug, render_debug=_render_debug)
    window = webview.create_window(
        'Program',
        QUASAR_GUI_INDEX_PATH,
        js_api=JsApi(),
        min_size=(600, 450))
    window_api_list.append((window, api))
    webview.start(api.init, window, debug=debug)


def set_main_component(component: Component):
    if len(window_api_list) != 1:
        raise AssertionError(
            'This function only works for a single window. '
            'Otherwise use layout.api.set_main_component()')
    window_api_list[0][API].set_main_component(component)
