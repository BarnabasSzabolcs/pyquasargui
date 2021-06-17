<template>
    <div class="sfc">
        <h5 class="q-my-sm">MySingleFileComponent</h5>
        <p>
        Model value: {{ value }}
        <p>
        The `single file component` support is partial,
        <ul>
            <li><code>import</code> is not supported,</li>
            <li>only html template is supported</li>
            <li>only css style is supported</li>
        </ul>
    </div>
</template>

<script>
    export default {
        props: ['value']
    }
</script>

<style>
.sfc{
    padding: 20px;
    margin: 40px;
    border: 1px dashed #0b0;
}
</style>