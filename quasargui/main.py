import json

import webview

from quasargui import QUASAR_GUI_INDEX_PATH
from .components import Component, EventCallbacks


class Api:
    def __init__(self, main_component: Component):
        self.main_component = main_component
        self.window = None

    def init(self, window):
        self.window = window
        json_str = json.dumps(self.main_component.vue)
        cmd = f'app.setMainComponent({json_str})'
        print(cmd)
        window.evaluate_js(cmd)
        self.main_component.set_api(self)

    # noinspection PyMethodMayBeStatic
    def call_cb(self, cb_id: int, params):
        try:
            EventCallbacks.get(cb_id)(params)
        except TypeError as e:
            try:
                EventCallbacks.get(cb_id)()
            except TypeError:
                print("ERROR:", e)
                raise e
        except Exception as e:
            print("ERROR:", e)
            raise e

    def get_data(self, data_id: str):
        return self.window.evaluate_js(f'app.getData({data_id})')

    def set_data(self, data_id: str, value):
        print('set_data', data_id, value)
        return self.window.evaluate_js(f'app.setData({data_id}, {json.dumps(value)})')

    def send_notification(self, message: str):
        message = json.dumps({'message': message})
        return self.window.evaluate_js(f'app.showNotification({message})')


def run(component: Component):
    api = Api(component)
    window = webview.create_window(
        'Program',
        QUASAR_GUI_INDEX_PATH,
        js_api=api,
        min_size=(600, 450))
    webview.start(api.init, window, debug=True)
