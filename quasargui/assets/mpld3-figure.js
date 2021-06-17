Vue.component('mpld3-figure', {
  props: ['id', 'script', 'style', 'figId'],
  render: function(h) {
    const script = document.createElement('script')
    script.id = this.id + '_script'
    script.innerHTML = this.script
    const style = document.createElement('style')
    style.innerHTML = this.style
    style.id = this.id + '_style'
    if (this.$el) {
      this.$el.innerHTML = ''
    }
    setTimeout(() => {
      var styleObj = document.getElementById(style.id)
      if (styleObj) {
        styleObj.remove()
      }
      var scriptObj = document.getElementById(script.id)
      if (scriptObj) {
        scriptObj.remove()
      }
      document.head.appendChild(style)
      document.body.appendChild(script)
    })
    return h('div', {
      attrs: {
        id: this.figId
      }
    })
  }
})