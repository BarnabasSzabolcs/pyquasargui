externalValue = 5

Vue.component('my-custom-component', {
    props: ['value'],
    data(){
        return {
            name: 'MyCustomComponent'
        }
    },
    template:`
        <div class="my-custom-component">
            <h5 class="q-my-sm">{{name}}</h5>
            Written in js, using 'template' parameter of Vue.component.
            <br>
            It's model's value: {{ value }}
        </div>
        `
})
