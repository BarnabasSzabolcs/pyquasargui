# Quickstart

This page takes you through concepts of Quasargui.

If you haven't yet installed Quasargui, you can install Quasargui by
    
    pip install quasargui

Now, you're ready to run our first example.

## The simplest window

The simplest possible window only takes 3 lines of code.

=== "screenshot"
    <figure>
    ![Hello_world_window](assets/screenshots/hello_world.png#screenshot "Hello world window screenshot")
    </figure>

=== "source"
    ```python 
    {!examples/hello_world.py!}
    ```

The important parts of the code:

  1. `run` runs the GUI - and the program stays at this line until all the windows are closed.
  2. `run` always takes a `Component`, the main component to display. In this case the component is `Rows`. 
  3. `children` can be a list of `Component`'s and `str`'s and some other types that we'll discuss later. 
  4. The `children` strings accept html code, so simple formats such as `<i>` and `<b>` can be comfortably written directly. For more complex cases, use components such as `Link`, `Heading`, etc.

Let's move on to a more advanced code that also can be used as a boilerplate for your app.

## Starter code

To quickly get a nice window layout, you can use the code of the window below.

=== "screenshot"
    <figure>
    ![Quasargui menu header boilerplate](assets/screenshots/starter_header_footer_and_menu.png#screenshot)
    </figure>

=== "source"
    ```python
    {!examples/starter_header_footer_and_menu.py!}
    ```

The things you need to know about this window:

`QLayout`, `QDrawer`, etc. are all `Component`s that correspond to **Vue** components. In particular, we use [Quasar][quasardoc]'s professional-looking components - hence the name Quasargui. All the components you see on the Quasar documentation page, are imported into Quasargui, wrapped into `Component`'s.

The first parameter of a `Component` is `children`, so you don't have to type constantly `children=`.   
Note that `QButton`'s first parameter is *not* children but `label` since typically you want to add a label to a button and not children (which is also still possible of course...).

Quasargui uses Python's typing system, so if you use an IDE you can always check with typing system if you're using Quasargui correctly.

To make changes on the window, we use `Model`'s, like `loading` in this example. A `Model` provides "two-way binding" between your code and the GUI. This means that every change to a `Model`'s value is reflected in the GUI and every user input changes the `Model`'s value.

## Vue vs. Quasargui

If you have experience with Vue, this section shows you how concepts in Vue are transferred to Quasargui.  
The transfer from Vue is natural since under the hood Quasargui builds up a Vue/Quasar webpage and interacts with it through pywebview's api.

For example 
```python
ok_label = Model('ok')
Div(children=[
    'text', 
    QButton(props={'label': ok_label})
])
``` 
roughly results in 
```html
<div>
    text
    <q-button :label='data[1]' />
</div>
```

So, if you look into [quasar's documentation][quasardoc], all Vue components have their `Component` counterpart in Quasargui, with the same name. As an example, `<q-button/>` corresponds to `QButton`.

### Vue components to Component parameters

Among a `Component`'s constructor's parameters,

* `children` corresponds to html-style children.
* `props` corresponds to `props` (eg. `label="ok"`, `:label="data[1]"`),
* `events` corresponds to Vue events (eg. `@click`)
* `classes` corresponds to `class` attribute.
* `style` corresponds to `style` attribute.

Additionally, we have defined some shorthand parameters for frequently used props (such as `label` in case of QButton).

Directives are defined as functions. `v_show` and other `v_*` functions correspond to `v-*` directives. Only `v-model` gets special treatment, it is always accessible as the `model` parameter of a `ComponentWithModel`.

Any `Model` corresponds to Vue data that is defined on the Vue app. There is also `Computed` that works similar to 'computed'  in Vue.

### Vue slots in Quasargui

In components, Vue's slots can be accessed as `Slot('slot-name', [...children...])`. Since `Slot` is a `Component`, it also has props, events, styles and classes.

=== "screenshot"
    <figure>
    ![Slots example](assets/screenshots/slots_simple.png#screenshot)
    <figcaption>
    The map sign of the input field is defined in a slot.
    </figcaption>
    </figure>
=== "source"
    ```python
    {!examples/slots_simple.py!}
    ```

#### Scoped slots

Scoped slots can be accessed a little-bit differently. Since scoped slots are meant as a template, in python we express them as functions, `Slot('slot-name', lambda props: [... children...])`. In this formula `props` is a `PropVar` that behaves just like a `Model`.

=== "screenshot"
    <figure>
    ![Scoped slots example](assets/screenshots/slots_scoped_prop_vars.png#screenshot)
    <figcaption>
    This example is the Quasargui variant of Quasar's [tree example](https://quasar.dev/vue-components/tree#customize-content) where items in the tree view have customized *default-header* and *default-body*.
    </figcaption>
    </figure>
=== "source"
    ```python
    {!examples/slots_scoped_prop_vars.py!}
    ```

## Model and Computed

In Quasargui `Model` and `Computed` enable `Component`'s to change dynamically. They are the most convenient way to handle complex user interaction.    
To see the interactions with `Model` and `Computed`, consider the following example:

=== "screenshot"
    <figure>
    ![Even or odd](assets/screenshots/even_or_odd.png#screenshot)
    <figcaption>
    If you type a number into *a* or *b*,     
    the window displays "is even" or "is odd",     
    depending on the parity of *a+b*
    </figcaption>
    </figure>

=== "source"
    ```python
    {!examples/even_or_odd.py!}
    ```

In the example above `even` and `odd` are computed from the value of `a` and `b`. 
Although a `QInput`'s model value is usually `str`, in this example it is automatically converted to `int`, since `a` and `b` has initial value of type `int`.

In general, a `Model` accepts any combination of basic python types (including `list` and `dict`). If you want to use other python classes, you'll need to write your custom logic to convert a Model's value into json-compatible values.

To access the value of a `Model` or a `Computed`, use the `.value` property. It is a read/write property for `Model`'s and read-only for `Computed`. If you want to be more explicit, you can also use `.set_value()`.

### Watching changes

If you want to execute code when a `Model` gets a certain value, you just call `add_callback` on that `Model`. 

=== "screenshot"
    <figure>
    ![Accept_conditions](assets/screenshots/accept_conditions.png#screenshot)
    <figcaption>
    When the conditions are accepted, a notification pops up.
    </figcaption>
    </figure>

=== "source"
    ```python
    {!examples/accept_conditions.py!}
    ```

You can add a callback anytime of course, even after a component is added to the window. 

### Structured Models

Models can hold `int`, `str`, `bool` values, and also nested `list`'s and `dict`'s. 
If a model is a `dict`, it can be accessed just like a normal variable:
```python
deep_model = Model({'deep': {'data': 'deep value'}})
data_model = deep_model['deep']['data']  # is also a Model
data_model.value = 'new value'
assert deep_model.value['deep']['data'] == 'new value'  # True!
list_model = Model(['a', 'b', 'c'])
list_model[1].value == 'b'
list_model[1].value = 'new'
assert list_model.value == ['a', 'new', 'c']  # True!
```
Keep in mind that you can access any depth of items of a Model, with the item accessor,
and it is going to be a Model that refers to the same value as the original model.
Don't do `your_model.value['item'] == 'new value'` since it will not dynamically set the value in the GUI, and you'll have to manually run `your_model.update()`.

## Events

Events can be defined on `Components` using the `events` property at construction time. Events that can be defined are specific for a `Component`. If you want to check the state of the system at the event, access your `Model` and `Computed` values.

=== "screenshot"
    <figure>
    ![Click event](assets/screenshots/click_event.png#screenshot)
    <figcaption>
    When the user clicks the button, a notification pops up.
    </figcaption>
    </figure>

=== "source"
    ```python 
    {!examples/click_event.py!}
    ```

## Notifications, dialogs

Quasargui offers a range of notification and dialog options, wrapping [Quasar's plugins][quasardocplugins]. You can access most Quasar plugins via `your_component.api.plugins` or `your_model.api.plugins`. 

=== "📷 main screen"
    <figure>
    ![Click event](assets/screenshots/dialogs.png#screenshot)
    <figcaption>
    An extensive example. To check out all the dialogs and grid menus, you can run this example if you copy-paste it into your Python prompt.
    </figcaption>
    </figure>

=== "📷 dark mode"
    <figure>
    ![Click event](assets/screenshots/dialogs-dark.png#screenshot)
    <figcaption>
    Dark mode can be a breeze. The switch is in the top-right corner.
    </figcaption>
    </figure>

=== "📷 success notification"
    <figure>
    ![Click event](assets/screenshots/dialogs-alert.png#screenshot)
    <figcaption>
    Notifications can be easily configured (use `your_component.api.plugins.notify()`, with setting keyword arguments besides message). See [Quasar documentation of options][quasardocnotifyapi]; on QuasarConfOptions you can use any option as a keyword argument to `notify()`.  
    </figcaption>
    </figure>

=== "📷 options dialog"
    <figure>
    ![Click event](assets/screenshots/dialogs-options.png#screenshot)
    <figcaption>
    One type of dialog is options dialog. You can have a simple yes-no prompt, a string value input prompt and other custom options.
    </figcaption>
    </figure>

=== "📷 grid menu"
    <figure>
    ![Click event](assets/screenshots/dialogs-grid_menu.png#screenshot)
    <figcaption>
    A grid menu can nicely de-clog your app.
    </figcaption>
    </figure>

=== "⌨️ python source"
    ```python
    {!examples/dialogs.py!}
    ```

In general, in [Quasar's plugins][quasardocplugins] documentation, if you see `notify({options})` you can expect to write in Python `my_component.api.plugins.notify(**options)`.

Note that not all plugins are wrapped (because many plugins do not make sense in a desktop app) and some plugins work a little bit different. Look up `QuasarPlugins` in the `Quasargui` code to see all the implemented plugins.

## Custom styles, defaults

Once you start working with Quasargui, you will probably want to create your own styling. Luckily, Quasar is pretty flexible, offers a range of [styling classes][quasardocclasses] (eg. `'q-mt-xl'` means margin top should be extra large) and `Q*` components have lots of props (eg. `QButton(props={'glossy': True})`).

It can be a bit of a hustle though to set the same options again and again. So, defaults to the rescue!


=== "screenshot"
    <figure>
    ![Styling with defaults](assets/screenshots/defaults.png#screenshot)
    <figcaption>
    An alternative styling for form elements. Check out the code to see how styles can be set.
    </figcaption>
    </figure>
=== "source"
    ```python
    {!examples/defaults.py!}
    ```

## Window access

Quasargui's `run(layout)` command automatically produces a window for you. You can access this window through `layout.api` - in fact, `your_component.api` and `your_model.api` points to the same api *after* the component or the model is attached to a window. If you want to modify the window's properties, access system dialogs or create new windows, you can find these functionality as `api`'s (`quasargui.main.Api`'s) functions.

So, in the following sections we'll basically walk through `quasargui.main.Api`.

### Menu

Menu can be added using `run(menu=menu_definition)` where `menu_definition` can look like 
```python
[{
    'title': 'Edit', 
    'children': [
        {'title': 'Copy', 'key': 'c', 'action': copy_cb},
        {'title': 'Paste', 'key': 'p', 'action': paste_cb}
    ]
}]
``` 
There are other subtleties such as defining a menu that is specific to a certain operations system. These are covered in the documentation of `Api`.

=== "📷 menu on mac"
    <figure>
    ![Example native mac menu](assets/screenshots/menu-mac.png)
    <figcaption>
    An example menu on Mac - check out the other screenshots for other systems.
    </figcaption>
    </figure>
=== "📷 menu on other systems"
    <figure>
    ![Example menu under the titlebar](assets/screenshots/menu-other.png)
    <figcaption>
    The menu on other systems is implemented using Quasargui `Component`'s, mimicking a Windows menu.
    </figcaption>
    </figure>
=== "⌨️ python source"
    ```python
    {!examples/menu.py!}
    ```

If you want to dynamically change the menu, you can do that using `Api`'s `set_menu()` command.

### Window operations

To access window operations, we use `Api`'s methods. You can access the api instance pointing to the window by a `Component` that is already mounted to a window (`your_component.api`) or a `Model` that is mounted to a window (`your_model.api`). To minimize, fullscreen or close a window, call 
`.minimize_window()`, `.toggle_fullscreen()` or `.close_window()`. To change the title, call `.set_title('New title')`. 

The standard file/folder/save dialogs can be accessed the same way - see the code of this example below.

=== "screenshot"
    <figure>
    ![window_operations](assets/screenshots/window_operations.png#screenshot)
    <figcaption>
    Copy the code of this example into your Python prompt to see window properties in action.
    </figcaption>
    </figure>
=== "source"
    ```python
    {!examples/window_operations.py!}
    ```

Frameless windows are also possible.

=== "screenshot"
    <figure>
    ![window_operations](assets/screenshots/window_frameless.png#screenshot)
    <figcaption>
    This toolbar is a frameless window.
    </figcaption>
    </figure>
=== "source"
    ```python
    {!examples/window_frameless.py!}
    ```

### Multiple windows

You can manage multiple windows. In that case the main rule of thumb is that each `Component`, `Model` and `Computed` can belong to only *one* window.    
So, it is best to create your layout and models via a factory function.

=== "screenshot"
    <figure>
    ![window_handling](assets/screenshots/window_handling.png#screenshot)
    <figcaption>
    This example creates a new random-sized window when the user clicks 'create window'. Setting window title (that is a model) affects only its own window. 
    </figcaption>
    </figure>
=== "source"
    ```python
    {!examples/window_handling.py!}
    ```

## Most important components

In this part we'll go through the most important components.
If you're interested in seeing all components, go to the [components list](components.md).

### Layout components 

The window (or `run()` function) can take any component as `component`, still it is recommended to use `QLayout` with `QHeader`, `QPage` and `QFooter` as children, and optionally `QDrawer`'s. This leads to a standard layout where you can put your most important functions into `QHeader`, as `QButton` (*'stretch'* prop is recommended). QHeader's background and foreground can be set using 'q-*' classes, using `styles={'background': '#abc', 'color': '#fff'}` or adding your own stylesheet, pushing the path of your css file to `your_component.style_sources` or calling `your_component.api.import_styles()` after your component is mounted. 

Note that adding `QHeader` and `QFooter` to `QLayout` is entirely optional.

### Rows and Columns

If you want the classic vertical or horizontal layout, use `Rows` or `Columns`. These result in a html "flex" layout which means that Columns will wrap automatically if the window is not wide enough.

=== "screenshot"
    <figure>
    ![columns_and_rows](assets/screenshots/columns_and_rows.png#screenshot)
    <figcaption>
    Columns and rows can be assembled using `Columns` and `Rows` component.
    </figcaption>
    </figure>

=== "source"
    ```python
    {!examples/columns_and_rows.py!}
    ```
Note that columns don't grow naturally, for even spacing you need to set 'col-grow', also with `Rows` you need to set 'row-grow' for even alignment. 

### Form elements

You have access to a range of form elements. There are the Quasar form components (starting with Q, in `quasargui.quasar_form` module). 

=== "screenshot"
    <figure>
    ![Form_simple](assets/screenshots/form_simple.png#screenshot)
    <figcaption>
    Some basic list of quasar form-components in a window
    </figcaption>
    </figure>

=== "source"
    ```python
    {!examples/form_simple.py!}
    ```

Also, there are form elements *by input value type*. These elements are in `quasargui.quasar_form_improved` module and are named according to the input value type, eg. `InputStr`, `InputBool`, etc. The idea is to automatically get a combination of controls that is set up correctly. You can get an apropriate appearance for your input, and later you can refine it, choosing from one of its available `appearance`. Eg. an `InputChoice` can be a radio, a series of pushable buttons, or a select dropdown. Or, if you allow multiple choices, you can get checkbox, toggles, tags input or a multi-choice select. If you don't choose one, the control is determined based on the number of available choices.

=== "📷 single choice appearances"
    <figure>
    ![Form_input_choice-single](assets/screenshots/form_input_choice-single.png#screenshot)
    <figcaption>
    InputChoice with different single-choice appearance settings.
    If the appearance is not set, it will automatically choose an appearance based on the number of choices 
    </figcaption>
    </figure>

=== "📷 multiple choice appearances"
    <figure>
    ![Form_input_choice-multiple](assets/screenshots/form_input_choice-multiple.png#screenshot)
    <figcaption>
    InputChoice with different multi-choice appearance settings.
    If the appearance is not set, it will automatically choose an appearance based on the number of choices
    </figcaption>
    </figure>

=== "⌨️ source"
    ```python
    {!examples/form_input_choice.py!}
    ```

There's `InputTime`, `InputDate` and `InputDateTime` that are implementations of Quasar's recommendations on data-time input, with all the conversions between Python and the GUI taken care of (remember that `date`, `time` and `datetime` is a special class that is not a basic type.)

=== "screenshot"
    TODO: example - date-time with datetime open.

=== "source"
    ```python
    ```

#### Form validation

You can validate form components right when the user inputs a value - but for snappier action you need to add raw javascript to handle simple field validations, using `JSRaw`.

=== "📷 form with field error"
    <figure>
    ![Form_validation-field](assets/screenshots/form_validation-field.png#screenshot)
    <figcaption>
    When the user fails to fill username, it gets into error state.
    </figcaption>
    </figure>

=== "📷 form with error after submission"
    <figure>
    ![Form_validation-submit](assets/screenshots/form_validation-submit.png#screenshot)
    <figcaption>
    When the user clicks submit, and there's error with the form data, a notification pops up.
    </figcaption>
    </figure>

=== "⌨️ source"
    ```python
    {!examples/form_validation.py!}
    ```

You can also stick to validation on submit, in this case you need to set up a `Model` for errors.

=== "screenshot"
    TODO: example - submit-time validation

=== "source"
    ```python
    ```

## Creating your own components

=== "screenshot"
    TODO: example - custom component

=== "source"
    ```python
    ```

## Integration

### Matplotlib integration

=== "screenshot"
    TODO: example - matplotlib integration

=== "source"
    ```python
    ```

### Adding your own existing components

=== "screenshot"
    TODO: example - with external js like Tags input.

=== "source"
    ```python
    ```

=== "screenshot"
    TODO: example - from spa-style own js.

=== "source"
    ```python
    ```

[quasardoc]: https://quasar.dev
[quasardocplugins]: https://quasar.dev/quasar-plugins/
[quasardocnotifyapi]: https://quasar.dev/quasar-plugins/notify#notify-api
[quasardocclasses]: https://quasar.dev/style/spacing