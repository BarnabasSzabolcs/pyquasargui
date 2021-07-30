import json
from typing import Union

from quasargui.base import EventCallbacks
from quasargui.typing import ValueType, PropsType, EventsType
from quasargui.main import Plugins, Api


class QuasarPlugins(Plugins):
    script_sources = ['quasar_plugins.js']

    def notify(self, message: str, **params: ValueType) -> None:
        """
        reference: https://quasar.dev/quasar-plugins/notify#usage

        Line breaks cause message to render in 'html' mode. To disable this, add `html=False` to params.
        """
        params['message'] = message
        if 'html' not in params and '\n' in message:
            params['message'] = message.replace('\n', '<br>')
            params['html'] = True
        self.api.evaluate_js('quasarPlugins.notify(app, {params})'.format(params=json.dumps(params)))

    def dialog(self, props: PropsType, events: EventsType) -> None:
        """
        reference: https://quasar.dev/quasar-plugins/dialog#predefined
        """
        self.api.evaluate_js('quasarPlugins.dialog(app, {params}, {events})'.format(
            params=json.dumps(props),
            events=EventCallbacks.render_events(events)
        ))

    def dark(self, value: Union[bool, None]) -> None:
        """
        Sets dark mode.
        reference:  https://quasar.dev/quasar-plugins/dark#dark-api
        :param value: None means "auto"
        """
        if value is None:
            value = "auto"
        self.api.evaluate_js('app.$q.dark.set({})'.format(json.dumps(value)))

    def dark_toggle(self) -> None:
        """
        toggles dark mode
        """
        self.api.evaluate_js('app.$q.dark.toggle()')

    def bottom_sheet(self, props: PropsType, events: EventsType) -> None:
        """
        reference: https://quasar.dev/quasar-plugins/bottom-sheet#usage
        """
        self.api.evaluate_js('quasarPlugins.bottomSheet(app, {params}, {events})'.format(
            params=json.dumps(props),
            events=EventCallbacks.render_events(events)
        ))

    def loading_show(self, params):
        """
        Fades the content and shows a spinner, with an optional text to explain the reason the app is loading.
        reference: https://quasar.dev/quasar-plugins/loading#usage
        """
        self.api.evaluate_js('app.$q.loading.show({params})'.format(params=json.dumps(params)))

    def loading_hide(self):
        self.api.evaluate_js('app.$q.loading.hide()')

    def loading_bar_start(self):
        """
        Puts a loading bar on the bottom of the window.
        Use `loading_bar_increment()` and `loading_bar_stop()` to set progress.
        reference: https://quasar.dev/quasar-plugins/loading-bar
        """
        self.api.evaluate_js('app.$q.loadingBar.start()')

    def loading_bar_stop(self):
        self.api.evaluate_js('app.$q.loadingBar.stop()')

    def loading_bar_increment(self, value: float):
        assert (0.0 < value < 1.0)
        self.api.evaluate_js('app.$q.loadingBar.increment({})'.format(json.dumps(value)))


# register QuasarPlugins
Api.plugins_class = QuasarPlugins
