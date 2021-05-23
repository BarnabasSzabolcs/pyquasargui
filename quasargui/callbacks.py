from typing import TYPE_CHECKING, Callable, Any

if TYPE_CHECKING:
    from ._base import Model


def toggle(model: 'Model'):
    def f():
        model.value = not model.value
    return f


def bind(fun: Callable[['Model'], Any], *args):
    def f():
        fun(*args)
    return f
