import json
import traceback
from typing import List, Tuple

import webview
from webview import Window

from quasargui import QUASAR_GUI_INDEX_PATH
from quasargui.base import EventCallbacks
from quasargui.components import Component


def _print_error(e):
    print("\n\nERROR {}: {}".format(e.__class__.__name__, e))
    print(traceback.format_exc())


class Api:
    def __init__(self, main_component: Component, debug: bool = False):
        self.main_component = main_component
        self.window = None
        self.debug = debug

    def init(self, window):
        self.window = window
        window.evaluate_js('app.setDebug({debug})'.format(
            debug=json.dumps(self.debug)
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

    # noinspection PyMethodMayBeStatic
    def call_cb(self, cb_id: int, params=None):
        fun = EventCallbacks.get(cb_id)
        nargs = fun.__code__.co_argcount
        if nargs == 0:
            try:
                fun()
            except Exception as e:
                _print_error(e)
                raise e
        elif nargs == 1:
            try:
                fun(params)
            except Exception as e:
                _print_error(e)
                raise e
        else:
            raise AssertionError('Callback {name} has wrong number of parameters ({n})'.format(
                name=fun.__name__,
                n=nargs
            ))

    # noinspection PyMethodMayBeStatic
    def print_log(self, args):
        """
        callback for app for debug purposes
        """
        print(*args.values(), sep=' ', end='\n', flush=True)

    def get_data(self, data_id: int):
        return self.window.evaluate_js('app.getData({data_id})'.format(
            data_id=data_id
        ))

    def set_data(self, data_id: int, value):
        if self.debug:
            print('set_data', data_id, value)
        return self.window.evaluate_js(
            'app.setData({data_id}, {value})'.format(
                data_id=json.dumps(data_id),
                value=json.dumps(value)
            ))

    def set_component(self, component_vue):
        if self.debug:
            print('set_component', component_vue)
        return self.window.evaluate_js(
            'app.refreshComponent({component_vue})'.format(
                component_vue=json.dumps(component_vue)))

    def send_notification(self, params: dict):
        return self.window.evaluate_js('app.showNotification({params})'.format(
            params=json.dumps(params)))


WINDOW = 0
API = 1
window_api_list: List[Tuple[Window, Api]] = []


def run(component: Component, debug: bool = False):
    api = Api(component, debug=debug)
    window = webview.create_window(
        'Program',
        QUASAR_GUI_INDEX_PATH,
        js_api=api,
        min_size=(600, 450))
    window_api_list.append((window, api))
    webview.start(api.init, window, debug=debug)


def set_main_component(component: Component):
    if len(window_api_list) != 1:
        raise AssertionError(
            'This function only works for a single window. '
            'Otherwise use layout.api.set_main_component()')
    window_api_list[0][API].set_main_component(component)
