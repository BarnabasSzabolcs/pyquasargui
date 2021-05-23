"""
Coin-flip stock market price simulator

this example requires matplotlib and mpld3
"""
import random
import time

import matplotlib.pyplot as plt
# noinspection PyPackageRequirements
from mpld3 import plugins

import quasargui
from quasargui import Model
from quasargui.components import *

loading = Model(False)
calculation_time = Model(0.0)
n = Model(100)
n_processes = Model(10)
start = Model(0.0)
drift = Model(0.0)
variance = Model(1.0)
interactive = Model(False)
plot = Plot(interactive=bool(interactive.value))


def calculate_plot():
    loading.value = True
    t1 = time.time()

    def create_random_process():
        coinflips = random.choices([-1, 1], k=int(n.value))
        random_process = [float(start.value)]
        for flip in coinflips:
            prev = random_process[-1]
            random_process.append(prev + float(variance.value) * flip + float(drift.value))
        return random_process

    fig, ax = plt.subplots(1, 1)
    plt.close()
    ax.grid(True, alpha=0.3)
    for _ in range(int(n_processes.value)):
        ax.plot(create_random_process())
    handles, labels = ax.get_legend_handles_labels()  # return lines and labels
    interactive_legend = plugins.InteractiveLegendPlugin(zip(handles,
                                                             ax.collections),
                                                         labels,
                                                         alpha_unsel=0.5,
                                                         alpha_over=1.5,
                                                         start_visible=True)
    plugins.connect(fig, interactive_legend)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    if bool(interactive.value):
        ax.set_title('Interactive legend', size=20)
    plot.set_figure(fig, ax)
    t2 = time.time()
    calculation_time.value = round(t2 - t1, 2)
    loading.value = False


layout = Layout(events={'load': calculate_plot}, children=[
    Header([
        Toolbar([ToolbarTitle(['Interactive plot demo'])])
    ]),
    Page([
        plot
    ]),
    Drawer([
        Input(label='n', model=n),
        Input(label='drift', model=drift),
        Input(label='variance', model=variance),
        Button(label='calculate', events={'click': calculate_plot}, props={'loading': loading})
    ]),
    Footer([
        'Plotting took ',
        calculation_time,
        ' seconds.'
    ]),
])

quasargui.run(layout, debug=True)
