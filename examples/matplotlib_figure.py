"""
Coin-flip stock market price simulator

this example requires matplotlib and mpld3
"""
import math
import random
import time

# noinspection PyPackageRequirements, PyUnresolvedReferences
import matplotlib.pyplot as plt

import quasargui
from quasargui.components import *

loading = Model(False)
calculation_time = Model(0.0)
n = Model(100)
n_processes = Model(10)
start = Model(10.0)
drift = Model(0.002)
variance = Model(0.04)
interactive = Model(False)


def calculate_plot():
    loading.value = True
    t1 = time.time()

    def create_random_process():
        coinflips = random.choices([-1, 1], k=int(n.value))
        random_process = [float(start.value)]
        for flip in coinflips:
            s_0 = random_process[-1]
            mu = float(drift.value)
            var = float(variance.value)
            s_1 = s_0 * math.e ** (mu - 0.5 * var**2 + var * flip)
            random_process.append(s_1)
        return random_process

    fig, ax = plt.subplots(1, 1)
    for _ in range(int(n_processes.value)):
        ax.plot(create_random_process())

    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # update the gui
    plot.set_figure(fig)
    t2 = time.time()
    calculation_time.value = round(t2 - t1, 2)
    loading.value = False


# This example loads the plot on load.
plot = Plot(interactive=interactive)
layout = Layout(events={'load': calculate_plot}, children=[
    Header([
        Toolbar([ToolbarTitle([
            Icon('insights', 'lg', classes='q-mx-md'),
            'Interactive plot demo <small>- stock simulation by coin flip</small>'
        ])])
    ]),
    Page([
        plot
    ]),
    Drawer([Rows([
        Input(label='number of coinflips', model=n),
        Input(label='number of screnarios', model=n_processes),
        Input(label='start value (S_0)', model=start),
        Input(label='drift (μ)', model=drift),
        Input(label='variance (σ)', model=variance),
        Toggle(label='interactive', model=interactive),
        Button(label='calculate', events={'click': calculate_plot}, props={'loading': loading}),
    ])]),
    Footer(props={'v-if': calculation_time}, children=[
        'Plotting took ',
        calculation_time,
        ' seconds.'
    ])
])

quasargui.run(layout, debug=True)