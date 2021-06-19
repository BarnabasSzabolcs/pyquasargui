import json
from typing import Union

from quasargui.base import EventCallbacks
from quasargui.typing import ValueType, PropsType, EventsType
from quasargui.main import Plugins, Api


class QuasarPlugins(Plugins):
    script_sources = ['quasar_plugins.js']

    def notify(self, **params: ValueType):
        self.api.evaluate_js('quasarPlugins.notify(app, {params})'.format(params=json.dumps(params)))

    def dialog(self, props: PropsType, events: EventsType):
        self.api.evaluate_js('quasarPlugins.dialog(app, {params}, {events})'.format(
            params=json.dumps(props),
            events=EventCallbacks.render_events(events)
        ))

    def dark(self, value: Union[bool, None]):
        """
        :param value: None means "auto"
        :return:
        """
        if value is None:
            value = "auto"
        self.api.evaluate_js('app.$q.dark.set({})'.format(json.dumps(value)))

    def dark_toggle(self):
        self.api.evaluate_js('app.$q.dark.toggle()')

    def bottom_sheet(self, props: PropsType, events: EventsType):
        self.api.evaluate_js('quasarPlugins.bottomSheet(app, {params}, {events})'.format(
            params=json.dumps(props),
            events=EventCallbacks.render_events(events)
        ))

    def loading_show(self, params):
        self.api.evaluate_js('app.$q.loading.show({params})'.format(params=json.dumps(params)))

    def loading_hide(self):
        self.api.evaluate_js('app.$q.loading.hide()')

    def loading_bar_start(self):
        self.api.evaluate_js('app.$q.loadingBar.start()')

    def loading_bar_stop(self):
        self.api.evaluate_js('app.$q.loadingBar.stop()')

    def loading_bar_increment(self, value: float):
        assert (0.0 < value < 1.0)
        self.api.evaluate_js('app.$q.loadingBar.increment({})'.format(json.dumps(value)))


# register QuasarPlugins
Api.plugins_class = QuasarPlugins
