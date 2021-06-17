externalValue = 5

Vue.component('my-custom-component', {
    props: ['value'],
    data(){
        return {
            name: 'my custom component'
        }
    },
    template:`
        <div class="my-custom-component">
            This is {{ name }}, written in js.
            <br>
            It's model's value: {{ value }}
        </div>
        `
})
