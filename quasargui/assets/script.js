function createEventCB(id) {
  return (params) => {
    window.pywebview.api.call_cb(id, params)
  }
}

function sendLog() {
  if (app.debug)
    window.pywebview.api.print_log(arguments)
}

// ref. https://symfonycasts.com/screencast/vue/vue-instance
// problem: this solution keeps rerendering unnecessarily when used with q-input
// alternative solution is to send html code and add it within script tags
// ref. https://jsfiddle.net/Justineo/y239e76m/
// ref. https://github.com/vuejs/vue/issues/9911
Vue.component('dynamic-component', {
  props: ['id'],
  data: {
    loadEventFired: false,
  },
  render: function(h) {
    if (this.id === undefined || this.id === null) {
      return ''
    }
    const d = this.$root.componentStore[this.id]
    sendLog('descriptor:', d)
    if (_.isString(d)) {
      sendLog('rendering:', d)
      return this.renderTemplate(d)
    }
    if (!d.component) {
      sendLog('rendering:', '(empty)')
      return ''
    }
    // sendLog(JSON.stringify(d))
    if (('value' in d.props) && !('input' in d.events)) {
      inputEvent = `@input="$root.data['${d.props.value['@']}']=$event"`
    } else {
      inputEvent = ''
    }
    if ('load' in d.events && !this.loadEventFired) {
      window.pywebview.api.call_cb(d.events.load)
      this.loadEventFired = true
    }
    const events = _.map(_.toPairs(d.events),
      pair => {
        [eventName, cb_id] = pair
        return `@${eventName}="params=>window.pywebview.api.call_cb(${cb_id}, params)"`
      }
    ).join(' ')

    const props = _.map(_.toPairs(d.props),
      pair => {
        const [propName, prop] = pair
        if (_.isObject(prop) && '@' in prop) {
          const ref = prop['@']
          if (ref in this.$root.data === false) {
            this.$root.$set(this.$root.data, ref, prop.value)
          }
          colon = propName.startsWith('v-') ? '' : ':'
          return `${colon}${propName}="$root.data[${ref}]"`
        } else if (_.isString(prop)) {
          quotedProp = prop.replace(/"/g, '&quot;')
          return `${propName}="${quotedProp}"`
        } else {
          return `:${propName}="${prop}"`
        }
      }
    ).join(' ')

    const children = _.map(d.children,
      child => {
        if (_.isString(child)) {
          return child
        } else {
          const childComponent = 'dynamic-component'
          child = JSON.stringify(child).replace(/'/g, "&#39;")
          return `<${childComponent} :id='${child}'></${childComponent}>`
        }
      }
    ).join('')

    const template = `<${d.component} ${props} ${events} ${inputEvent}>${children}</${d.component}>`
    // sendLog(Vue.compile(template).render)
    sendLog('rendering:')
    sendLog(template)
    return this.renderTemplate(template)
  },
  methods: {
    renderTemplate(template) {
      // This works even if the template does not have any reactive variables.
      // ref. https://github.com/vuejs/vue/issues/9911
      const compiled = Vue.compile(template)
      this.$options.staticRenderFns = [];
      this._staticTrees = [];
      compiled.staticRenderFns.map(fn => (this.$options.staticRenderFns.push(fn)))
      return compiled.render.call(this)
    }
  }
})

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

const app = new Vue({
  el: '#q-app',
  data: function() {
    return {
      mainComponentId: null,
      data: {}, // holds the Model values {id: value}
      componentStore: {}, // holds the Component specifications {id: descriptor}
      debug: false,
    }
  },
  methods: {
    setDebug(debug) {
      this.debug = debug
      if (debug) {
        setTimeout(() => {
          document.getElementById('debug').style.display = 'block'
        }, 50)
      }
    },
    setMainComponent(component) {
      const id = this.registerComponent(component)
      this.mainComponentId = id
    },
    registerComponent(component, refresh = false) {
      if (refresh || (component.id in this.componentStore === false)) {
        this.$set(this.componentStore, component.id, component)
      }
      const children = component.children || []
      component.children = children.map(child => {
        return _.isObject(child) ? this.registerComponent(child, refresh) : child
      })
      return component.id
    },
    refreshComponent(component) {
      this.registerComponent(component, refresh = true)
    },
    getData(id) {
      return this.data[id]
    },
    setData(id, value) {
      if(id in this.data===false){
        this.$watch(`data.${id}`, v=>{
          window.pywebview.api.set_model_value(id, v)
        })
      }
      this.$set(this.data, id, value)
    },
    showNotification(params) {
      const longTimeOut = 7000
      defaults = {
        type: '',
        timeout: longTimeOut,
        position: 'top',
        message: '',
        multiline: true
      }
      params = _.defaults(params, defaults)
      this.$q.notify(params)
    }
  }
})