import json
import re
from typing import List, Tuple, Dict, Union, Callable

import webview
from webview import Window

from quasargui import QUASAR_GUI_INDEX_PATH
from quasargui.base import EventCallbacks
from quasargui.components import Component
from quasargui.model import Model, Computed
from quasargui.tools import print_error
from quasargui.typing import ValueType, PathType, MenuSpecType


class Api:
    """
    python -> js
    """

    def __init__(self,
                 main_component: Component,
                 menu: MenuSpecType = None,
                 debug: bool = False,
                 render_debug: bool = False
                 ):
        self.main_component = main_component
        self.menu = menu
        self.window = None
        self.debug = debug
        self.render_debug = render_debug
        self.model_data_queue = []
        self.scripts_imported = set()
        self.styles_imported = set()

    def init(self, window):
        self.window = window
        if self.menu is not None:
            self.set_menu(self.menu)
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

    def get_model_data(self, data_id: int):
        return self.window.evaluate_js('app.getData({data_id})'.format(
            data_id=data_id
        ))

    def set_model_data(self, model_id: int, path: PathType, value: ValueType):
        if self.debug:
            print('set_model_data', model_id, path, value)
        self.model_data_queue.append({'id': model_id, 'path': path, 'value': value})

    def flush_model_data(self, data_id=0):
        if (not self.model_data_queue) or (data_id and self.model_data_queue[0]['id'] != data_id):
            return
        self.window.evaluate_js(
            'app.setData({payload})'.format(
                payload=json.dumps(self.model_data_queue)
            ))
        self.model_data_queue = []

    def set_component(self, component_vue):
        if self.debug:
            print('set_component', component_vue)
        self.window.evaluate_js(
            'app.refreshComponent({component_vue})'.format(
                component_vue=json.dumps(component_vue)))

    def call_component_method(self, component_id: str, method: str):
        """
        eg. call_component_method(12, 'validate()')
        """
        return self.window.evaluate_js('app.callComponentMethod({params})'.format(
            params=json.dumps({'component_id': component_id, 'method': method})
        ))

    def import_scripts(self, scripts: List[str]):
        not_added = [script for script in scripts if script not in self.scripts_imported]
        if not not_added:
            return
        self.scripts_imported |= set(not_added)
        self.window.evaluate_js('app.addScripts({})'.format(json.dumps(not_added)))

    def import_styles(self, styles: List[str]):
        not_added = [styles for styles in styles if styles not in self.scripts_imported]
        if not not_added:
            return
        self.styles_imported |= set(not_added)
        self.window.evaluate_js('app.addStyles({})'.format(json.dumps(not_added)))

    def show_notification(self, **params: ValueType):
        self.window.evaluate_js('app.showNotification({params})'.format(
            params=json.dumps(params)))

    @property
    def is_cocoa(self):
        return self.window.gui.__name__ == 'webview.platforms.cocoa'

    def set_menu(self, menuspec: Union[MenuSpecType, Dict[str, MenuSpecType]]):
        """
        If menuspec is a list then the menu is the same for all platforms,
        if menuspec is a dict then menuspec is set platform-specific.
        (eg. {'cocoa': [{'title': 'Cocoa menu'}], 'default': []})  # no menu if not cocoa.
        :param menuspec: [menuSpecApp, menuSpec1, menuSpec2, ...]
            where menuSpec is {'title': str, 'children': [menuSpec], 'key': str, 'icon': ...}
            or {'cocoa': [... menu spec for cocoa...], 'default': [... menu spec fallback ...]}
        :return:
        """
        if isinstance(menuspec, dict):
            if 'default' not in menuspec:
                AssertionError('Please set "default" menuspec as a fallback option.')

            if self.is_cocoa and 'cocoa' in menuspec:
                menuspec = menuspec['cocoa']
            if self.is_cocoa and 'mac' in menuspec:
                menuspec = menuspec['mac']
            else:
                menuspec = menuspec['default']

        self.menu = menuspec
        if self.is_cocoa:
            from quasargui.platforms.cocoa import set_menu as set_menu_cocoa
            set_menu_cocoa(self.window, menuspec)
        else:
            from quasargui.platforms.fallback import set_menu as set_menu_fallback
            set_menu_fallback(self, menuspec)

    def set_key_shortcut(self, key: str, cb: Callable):
        cb_id = EventCallbacks.register(cb)
        self.window.evaluate_js('app.setKeyShortcut({key}, {cb_id})'.format(
            key=json.dumps(key), cb_id=json.dumps(cb_id)))

    def register_sfc(self, component_name: str, vue_file_path: str):
        with open(vue_file_path, 'r') as f:
            code = f.read()
            try:
                template = code.split('<template>')[1].split('</template>')[0]
            except IndexError:
                raise AssertionError('<template>...</template> is not found in {}'.format(vue_file_path))
            try:
                script = code.split('<script>')[1].split('</script>')[0]
            except IndexError:
                raise AssertionError('<script>...</script> is not found in {}'.format(vue_file_path))
            try:
                style = code.split('<style>')[1].split('</style>')[0]
            except IndexError:
                style = ''
        script = re.sub(
            'export +default *{',
            'var {component_name} = {{template: `{template}`,'.format(
                component_name=component_name,
                template=template.replace('`', '\\`')
            ),
            script)
        self.window.evaluate_js('registerSfc({component_name}, {script}, {style})'.format(
            component_name=json.dumps(component_name),
            script=json.dumps(script),
            style=json.dumps(style)
        ))


# noinspection PyMethodMayBeStatic
class JsApi:
    """
    js -> python
    """

    def __init__(self, debug):
        self.debug = debug

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
            if self.debug:
                print('set_model_value', model_id, value)
            Model.model_dic[int(model_id)].set_value(value, _jsapi=True)
        except Exception as e:
            print_error(e)
            raise e

    def calculate_computed(self, computed_id: int, props: any):
        # noinspection PyProtectedMember
        return Computed._calculate_for_props_value(computed_id, props)


WINDOW, API = 0, 1
window_api_list: List[Tuple[Window, Api]] = []


def run(
        component: Component,
        title: str = None,
        menu: MenuSpecType = None,
        debug: bool = False,
        _render_debug: bool = False,
):
    """
    :param component:
    :param menu: [menuSpec1, menuSpec2, ...]
            where menuSpec is {'title': str, 'children': [menuSpec], 'key': str, 'icon': ...}
            if menuSpec is None or {}, a separator is displayed
            (See quasargui.main.Api.set_menu's menuspec)
    :param title: The title of the window.
    :param debug: Enables right-click inspection in the GUI window.
    :param _render_debug: this option is for quasargui development.
    It displays all the rendering in python's standard output.
    """
    api = Api(main_component=component, menu=menu, debug=debug, render_debug=_render_debug)
    window = webview.create_window(
        title or 'Program',
        QUASAR_GUI_INDEX_PATH,
        js_api=JsApi(debug=debug),
        min_size=(600, 450))
    window_api_list.append((window, api))
    webview.start(api.init, window, debug=debug)


def set_main_component(component: Component):
    if len(window_api_list) != 1:
        raise AssertionError(
            'This function only works for a single window. '
            'Otherwise use layout.api.set_main_component()')
    window_api_list[0][API].set_main_component(component)
