# Components list


## Quasar components

All the components starting with *Q* are wrapped Quasar Vue components that are documented on the [Quasar components documentation page][quasardoccomponents]. 
The components are all wrapped (almost) uniformly into Quarasgui `Component`'s.

If a component has a model, then it is usually wrapped into a `ComponentWithModel`. If a component is a form component (or makes sense for it to have a label), then it is wrapped into a `LabeledComponent`. `LabeledComponent` is a `ComponentWithModel` which is a `Component`.  

=== "diagram"
    ```mermaid
    classDiagram
        LabeledComponent <|-- ComponentWithModel
        ComponentWithModel <|-- Component
        class LabeledComponent{
        -label
        }
        class ComponentWithModel{
        +model
        }
    ```

Components are configured at initialization and if you want dynamic behavior, initialize them with `Model` values. Eg. 
```python
size = Model('sm')
q_button = QButton(props={'size': size})
```
A different method is to change `q_button.props` and then run `q_button.update()` but this is not the recommended approach.

### Reading Quasar's component documentation

When you read any Quasar component documentation, *props* correspond to *props* dictionary keys, *events* to *events* dictionary keys, *class* html attributes can be set at *classes* parameter, *style* attributes can be set at *styles* parameter. Any component that has html children in the documentation (also called as *default slot*), can be set children via *children* parameter.

Named slots and scoped slots can be passed as a special child among the list of *children*: a `Slot` component. If the slot is a scoped-slot, you'll set its *children* as a function.

[quasardoccomponents]: https://quasar.dev/vue-components/