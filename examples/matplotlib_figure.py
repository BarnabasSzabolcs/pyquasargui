"""
Coin-flip stock market price simulator

This example requires matplotlib and mpld3
"""
import math
import random
import time

# noinspection PyPackageRequirements, PyUnresolvedReferences
import matplotlib.pyplot as plt

from quasargui import *
from quasargui.plot import Plot

loading = Model[bool](True)
calculation_time = Model(0.0)
n = Model(1000)
n_processes = Model(10)
start = Model(10.0)
drift = Model(0.001)
variance = Model(0.02)
interactive = Model(False)
animated = Model(False)
fig, ax = plt.subplots(1, 1)
plot = Plot(renderer=Computed(lambda i: 'mpld3' if bool(i) else 'png', interactive))


def add_scenario(update_plot=True):
    global ax, plot, animated

    def create_random_process():
        coinflips = random.choices([-1, 1], k=int(n.value))
        random_process: list = [0]*(len(coinflips)+1)
        random_process[0] = float(start.value)
        mu = float(drift.value)
        var = float(variance.value)
        for i, flip in enumerate(coinflips, start=1):
            s_0 = random_process[i-1]
            s_1 = s_0 * math.e ** (mu - 0.5 * var**2 + var * flip)
            random_process[i] = s_1
        return random_process

    ax.plot(create_random_process())
    if update_plot:
        plot.update()


def redraw_plot():
    global fig, ax, plot, animated
    loading.value = True
    t1 = time.time()

    fig, ax = plt.subplots(1, 1)
    plot.set_figure(fig)
    for _ in range(int(n_processes.value)):
        add_scenario(update_plot=bool(animated.value))

    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    if not animated.value:
        plot.update()
    t2 = time.time()
    calculation_time.value = round(t2 - t1, 2)
    loading.value = False


# This example loads the plot on load.
QToggle.defaults['props'] = {
    'color': 'white',
    'keep-color': True,
    'left-label': True
}
layout = QLayout(events={'load': redraw_plot}, children=[
    QHeader([
        QToolbar([
            QToolbarTitle([
                QIcon('insights', 'lg', classes='q-mx-md'),
                'Plot demo <small>- Stock simulation by coin flip</small>'
            ]),
            QToggle(label='Interactive', model=interactive),
            QToggle(label='Animated', model=animated)
        ])
    ]),
    QPage([
        plot,
        v_if(
            interactive,
            Div(classes='text-center', children=[
                "Interactive plot is rendered by ",
                Link('mpld3', 'https://mpld3.github.io/')
            ])
        ),
        v_if(
            Not(Or(interactive, loading)),
            Div(classes='text-center', children=[
                'Non-interactive plot is rendered by matplotlib as png.'
            ])
        )
    ]),
    QDrawer([Rows([
        QInput(label='Number of coinflips', model=n),
        QInput(label='Number of screnarios', model=n_processes),
        QInput(label='Start value (S_0)', model=start),
        QInput(label='Drift (μ)', model=drift),
        QInput(label='Variance (σ)', model=variance),
        QButton(label='Redraw', events={'click': redraw_plot}, props={'loading': loading}),
        QButton(label='Add scenario', events={'click': add_scenario}, props={'disable': loading}),
    ])]),
    v_if(
        calculation_time,
        QFooter(['Plotting took ', calculation_time, ' seconds.'])
    )
])

run(layout)
