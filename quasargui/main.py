import json
import re
import weakref
from typing import List, Tuple, Dict, Union, Optional

import webview
from webview import Window

from quasargui import QUASAR_GUI_INDEX_PATH
from quasargui.base import EventCallbacks
from quasargui.components import Component
from quasargui.model import Model, Computed
from quasargui.tools import print_error
from quasargui.typing import ValueType, PathType, MenuSpecType, EventCBType


class Plugins:
    """
    Extend this class to hook up your plugins, then set
    ::

        Api.plugins_class = YourPlugins

    """
    script_sources: List[str] = []
    style_sources: List[str] = []

    def __init__(self, api: 'Api'):
        self.api = weakref.proxy(api)

    def init(self):
        if self.script_sources:
            self.api.import_scripts(self.script_sources)
        if self.style_sources:
            self.api.import_styles(self.style_sources)


class Api:
    """
    python -> js
    """
    plugins_class: type = Plugins

    def __init__(self,
                 main_component: Component,
                 menu: MenuSpecType = None,
                 debug: bool = False,
                 render_debug: bool = False,
                 ):
        if main_component.api is not None:
            raise AssertionError('A component can be only attached to a single window at a time.')
        self.main_component = main_component
        self.menu = menu
        self._window = None
        self.debug = debug
        self.render_debug = render_debug
        self.model_data_queue = []
        self.scripts_imported = set()
        self.styles_imported = set()
        self.plugins = self.plugins_class(self)

    def init(self, window):
        self._window = window
        if self.menu is not None:
            self.set_menu(self.menu)
        window.evaluate_js('app.setDebug({render_debug})'.format(
            render_debug=json.dumps(self.render_debug)
        ))
        self.set_main_component(self.main_component)
        self.plugins.init()

    def close_window(self, exit_if_last: bool = True):
        """
        :param exit_if_last: exists app if this was the last window
        """
        global window_api_list
        self.main_component.remove_api()
        window_api_list = [
            (window, api) for window, api in window_api_list
            if self._window != window]
        window = self._window
        self._window = None
        window.destroy()
        if exit_if_last and not window_api_list:
            exit(0)

    def set_window_title(self, title=str):
        self._window.set_title(title)

    def toggle_fullscreen(self):
        self._window.toggle_fullscreen()

    def minimize_window(self):
        self._window.minimize()

    def restore_window(self):
        self._window.restore()

    def hide_window(self):
        self._window.hide()

    def show_window(self):
        self._window.show()

    def move_window(self, position: Tuple[int, int]):
        self._window.move(*position)

    def resize_window(self, size: Tuple[Optional[int], Optional[int]]):
        if size[0] is None:
            size = (self._window.width, size[1])
        if size[1] is None:
            size = (size[0], self._window.height)
        self._window.resize(*size)

    def show_save_dialog(self, directory: str = '', save_filename: str = ''):
        """
        :param directory: Initial directory
        :param save_filename: Default filename.
        :return: A tuple of selected files, None if cancelled.
        """
        return self._window.create_file_dialog(
            webview.SAVE_DIALOG, directory=directory, save_filename=save_filename)

    def show_open_file_dialog(self, directory: str = '', file_types=(), allow_multiple: bool = False):
        """
        :param directory: Initial directory
        :param file_types: Allowed file types in open file dialog. Should be a tuple of strings in the format:
            filetypes = ('Description (*.extension[;*.extension[;...]])', ...)
        :param allow_multiple: Allow multiple selection.
        :return: A tuple of selected files, None if cancelled.
        """
        return self._window.create_file_dialog(
            webview.OPEN_DIALOG, directory=directory, file_types=file_types, allow_multiple=allow_multiple)

    def show_folder_dialog(self, directory: str = ''):
        """
        :param directory: Initial directory
        :return: A tuple of selected folders, None if cancelled.
        """
        return self._window.create_file_dialog(
            webview.FOLDER_DIALOG, directory=directory)

    def evaluate_js(self, code):
        if self._window is not None:
            self._window.evaluate_js(code)

    def get_html_elements(self, selector: str) -> dict:
        """
        Use it only as a last resource.
        ref. https://pywebview.flowrl.com/examples/get_elements.html
        :param selector: css selector
        """
        return self._window.get_elements(selector)

    def set_main_component(self, component: Component):
        component.set_api(self)
        cmd = 'app.setMainComponent({component})'.format(
            component=json.dumps(component.vue)
        )
        if self.debug:
            print(cmd)
        self._window.evaluate_js(cmd)

    def get_model_data(self, data_id: int):
        return self._window.evaluate_js('app.getData({data_id})'.format(
            data_id=data_id
        ))

    def set_model_data(self, model_id: int, path: PathType, value: ValueType):
        if self.debug:
            print('set_model_data', model_id, path, value)
        self.model_data_queue.append({'id': model_id, 'path': path, 'value': value})

    def flush_model_data(self, data_id=0):
        if (not self.model_data_queue) or (data_id and self.model_data_queue[0]['id'] != data_id):
            return
        self._window.evaluate_js(
            'app.setData({payload})'.format(
                payload=json.dumps(self.model_data_queue)
            ))
        self.model_data_queue = []

    def set_component(self, component_vue):
        if self.debug:
            print('set_component', component_vue)
        self._window.evaluate_js(
            'app.refreshComponent({component_vue})'.format(
                component_vue=json.dumps(component_vue)))

    def call_component_method(self, component_id: str, method: str):
        """
        eg. ``call_component_method(12, 'validate()')``
        """
        return self._window.evaluate_js('app.callComponentMethod({params})'.format(
            params=json.dumps({'component_id': component_id, 'method': method})
        ))

    def import_scripts(self, scripts: List[str]):
        not_added = [script for script in scripts if script not in self.scripts_imported]
        if not not_added:
            return
        self.scripts_imported |= set(not_added)
        self._window.evaluate_js('app.addScripts({})'.format(json.dumps(not_added)))

    def import_styles(self, styles: List[str]):
        not_added = [styles for styles in styles if styles not in self.scripts_imported]
        if not not_added:
            return
        self.styles_imported |= set(not_added)
        self._window.evaluate_js('app.addStyles({})'.format(json.dumps(not_added)))

    @property
    def is_cocoa(self):
        return self._window.gui.__name__ == 'webview.platforms.cocoa'

    @property
    def is_windows(self):
        return self._window.gui.__name__ == 'webview.platforms.winforms'

    @property
    def is_linux(self):
        return self._window.gui.__name__ == 'webview.platforms.gtk'

    def set_menu(self, menuspec: Union[MenuSpecType, Dict[str, MenuSpecType]]):
        """
        If ``menuspec`` is a *list* then the menu is the same for all platforms,
        if ``menuspec`` is a *dict* then ``menuspec`` is set platform-specific.
        (eg. ``{'cocoa': [{'title': 'Cocoa menu'}], 'default': []})``  means no menu if not cocoa.)
        :param menuspec: ``[menuSpecApp, menuSpec1, menuSpec2, ...]``
        where menuSpec is ``{'title': str, 'children': [menuSpec], 'key': str, 'icon': ...}``
        or ``{'cocoa': [... menu spec for cocoa...], 'default': [... menu spec fallback ...]}``
        :return:
        """
        if isinstance(menuspec, dict):
            if 'default' not in menuspec:
                AssertionError('Please set "default" menuspec as a fallback option.')

            if self.is_cocoa and 'cocoa' in menuspec:
                menuspec = menuspec['cocoa']
            elif self.is_cocoa and 'mac' in menuspec:
                menuspec = menuspec['mac']
            elif self.is_windows and 'windows' in menuspec:
                menuspec = menuspec['windows']
            elif self.is_linux and 'linux' in menuspec:
                menuspec = menuspec['linux']
            else:
                menuspec = menuspec['default']

        self.menu = menuspec
        if self.is_cocoa:
            from quasargui.platforms.cocoa import set_menu as set_menu_cocoa
            set_menu_cocoa(self._window, menuspec)
        else:
            from quasargui.platforms.fallback import set_menu as set_menu_fallback
            set_menu_fallback(self, menuspec)

    def set_key_shortcut(self, key: str, cb: EventCBType):
        self._window.evaluate_js('app.setKeyShortcut({key}, {cb})'.format(
            key=json.dumps(key),
            cb=json.dumps(EventCallbacks.render_cb(cb))
        ))

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
                template=template.replace('``', '\\``')
            ),
            script)
        self._window.evaluate_js('registerSfc({component_name}, {script}, {style})'.format(
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
window_api_list = []  # : List[Tuple[Window, Api]]
STARTED = False


def run(
        component: Component,
        title: str = None,
        menu: MenuSpecType = None,
        min_size: Tuple[int, int] = None,
        size: Tuple[Optional[int], Optional[int]] = (None, None),
        position: Tuple[Optional[int], Optional[int]] = (None, None),
        frameless: bool = False,
        resizable: bool = True,
        fullscreen: bool = False,
        localization: dict = None,
        debug: bool = False,
        _render_debug: bool = False,
):
    """
    :param localization: i18n strings for the main menu items.
        See: https://pywebview.flowrl.com/examples/localization.html
    :param component: the component to load as main component.
    :param menu: ``[menuSpec1, menuSpec2, ...]``
        where ``menuSpec`` is ``{'title': str, 'children': [menuSpec], 'key': str, 'icon': ...}``
        if ``menuSpec`` is ``None`` or ``{}``, a separator is displayed
        (See quasargui.main.Api.set_menu's menuspec)
    :param title: The title of the window.
    :param min_size:
    :param size:
    :param position:
    :param frameless:
    :param fullscreen:
    :param debug: Enables right-click inspection in the GUI window.
    :param _render_debug: this option is for quasargui development.
        It displays all the rendering in python's standard output.
    """
    api, window = create_window(component,
                                title=title,
                                menu=menu,
                                min_size=min_size,
                                size=size,
                                position=position,
                                frameless=frameless,
                                resizable=resizable,
                                fullscreen=fullscreen,
                                debug=debug,
                                _render_debug=_render_debug)
    webview.start(lambda window_: start_app(api, window_), window, debug=debug, localization=localization or {}, gui='cef')


def start_app(api, window):
    global STARTED
    api.init(window)
    STARTED = True


def create_window(
        component: Component,
        title: str = None,
        menu: MenuSpecType = None,
        min_size: Tuple[int, int] = None,
        size: Tuple[Optional[int], Optional[int]] = (None, None),
        position: Tuple[Optional[int], Optional[int]] = (None, None),
        frameless: bool = False,
        resizable: bool = True,
        fullscreen: bool = False,
        debug: bool = None,
        _render_debug: bool = None,
) -> Tuple[Api, Window]:
    """
    Creates a new window.
    :param component: a component that is not attached to any window yet.
    :param title:
    :param menu:
    :param min_size:
    :param size:
    :param position:
    :param frameless:
    :param fullscreen:
    :param debug: Enables right-click inspection in the GUI window.
    :param _render_debug: this option is for quasargui development.
    It displays all the rendering in python's standard output.
    :return:
    """
    api = Api(main_component=component, menu=menu, debug=debug, render_debug=_render_debug)
    window = webview.create_window(
        title or 'Program',
        QUASAR_GUI_INDEX_PATH,
        js_api=JsApi(debug=debug),
        min_size=min_size or (200, 100),
        x=position[0],
        y=position[1],
        width=size[0] or 800,
        height=size[1] or 600,
        frameless=frameless,
        resizable=resizable,
        fullscreen=fullscreen
    )
    window_api_list.append((window, api))
    if STARTED:
        api.init(window)
    return api, window


def set_main_component(component: Component, window_index: int = 0):
    try:
        api = window_api_list[window_index][API]
    except IndexError:
        raise AssertionError('No such window: {}'.format(window_index))
    api.set_main_component(component)
