from typing import TYPE_CHECKING, Callable, Any

if TYPE_CHECKING:
    from .base import Model


def toggle(model: 'Model'):
    """
    This is an event callback.
    Usage:
    my_model = Model(False)
    MyComponent(events={'click': toggle(my_model)})
    """
    def f():
        model.value = not model.value
    return f


def bind(fun: Callable[['Model'], Any], *args) -> Callable:
    def f():
        fun(*args)
    return f
