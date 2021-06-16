import threading
from time import sleep
from typing import Callable

# noinspection PyUnresolvedReferences,PyPackageRequirements
from AppKit import NSMenu, NSMenuItem
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Foundation import NSObject
from webview import Window
from webview.platforms.cocoa import BrowserView

from quasargui.typing import MenuSpecType


def set_menu_cocoa(window: Window, menuspec: MenuSpecType):
    sleep(0.3)  # MAC bug: if the sleep is less, the menu does not render properly
    if window.gui.__name__ != 'webview.platforms.cocoa':
        raise AssertionError('set_menu_cocoa can be only called when using Mac/cocoa. '
                             'Current gui is: {}'.format(window.gui.__name__))
    bv = BrowserView.instances[window.uid]

    # noinspection PyProtectedMember
    bv._add_app_menu()

    main_menu = bv.app.mainMenu()
    for menu_spec in menuspec:
        assemble_menu(main_menu, menu_spec, top_menu=True)


def set_action(menu_item, callback):
    if isinstance(callback, Callable):
        menu_item.setTarget_(mfc)
        MyFuncCaller.callbacks[menu_item] = callback
        menu_item.setAction_("callback:")
    elif isinstance(callback, str):
        menu_item.setAction_(callback)
    else:
        raise NotImplementedError


def assemble_menu(parent_menu, menu_spec: dict, top_menu: bool = False):
    if not menu_spec:
        if not top_menu:
            parent_menu.addItem_(NSMenuItem.separatorItem())
        else:
            raise AssertionError('Cannot put separator into top menu')
    elif 'children' in menu_spec:
        menu_item = NSMenuItem.alloc().init()
        if not top_menu:
            menu_item.setTitle_(menu_spec['title'])
        parent_menu.addItem_(menu_item)
        menu = NSMenu.alloc().init()
        if top_menu:
            menu.setTitle_(menu_spec['title'])
        for child in menu_spec['children']:
            assemble_menu(menu, child)
        menu_item.setSubmenu_(menu)
    else:
        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            menu_spec['title'], None, menu_spec.get('key', '') if not top_menu else '')
        parent_menu.addItem_(menu_item)
        if top_menu:
            # workaround:
            # I cannot get Mac to play the action on a top menu if it is a menu item
            # Mac does not display top menu item without submenu...
            menu = NSMenu.alloc().init()
            menu.setTitle_(menu_spec['title'])
            assemble_menu(menu, menu_spec)
            menu_item.setSubmenu_(menu)
        if 'action' in menu_spec:
            set_action(menu_item, menu_spec['action'])


class MyFuncCaller(NSObject):
    callbacks = {}

    def callback_(self, arg0):
        # evaluate_js cannot start in the same thread, the cocoa app would hang.
        x = threading.Thread(target=self.callbacks[arg0])
        x.start()


mfc = MyFuncCaller.alloc().init()
