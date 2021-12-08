function registerSfc(component_name, script, style) {
  let node
  node = document.createElement('script')
  node.innerHTML = script
  document.body.appendChild(node)

  node = document.createElement('style')
  node.innerHTML = style
  document.head.appendChild(node)

  Vue.component(component_name, window[component_name])
}

function toCallback(cb) {
  if(_.isNumber(cb)){ // callback id
    return params => window.pywebview.api.call_cb(cb, params)
  } else { // JSRaw
    return eval(cb['$'])
  }
}

function sendLog() {
  if (app._data.debug)
    window.pywebview.api.print_log(arguments)
}

function getPathJs(prop, drop_last_segment) {
  if (!('path' in prop && prop.path.length)) return ''
  path = drop_last_segment ? _.dropRight(prop.path, 1) : prop.path
  return path.map(v => _.isString(v) ? `['${v}']` : `[${v}]`).join('')
}

function getBase(prop) {
  if ('@' in prop) {
    // Model
    return `$root.data[${prop['@']}]`
  } else if ('@p' in prop) {
    // PropVar
    return prop['@p']
  } else {
    throw Error("Not implemented")
  }
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
    if (!this.id) {
      return this.renderTemplate('<div></div>')
    }
    const template = this.assembleTemplate(this.id, false)
    sendLog('rendering:')
    sendLog(template)
    return this.renderTemplate(template)
  },
  methods: {
    ref(ref) {
      return this.$refs[ref]
    },
    calculateWithProp(computedId, props) {
      // calculates a Computed within a scoped slot for props
      if (computedId in this.$root.computed === false) {
        this.$set(this.$root.computed, computedId, {})
      }
      const s = JSON.stringify(props)
      if (s in this.$root.computed[computedId]) {
        return this.$root.computed[computedId][s]
      } else {
        this.$set(this.$root.computed[computedId], s, {
          value: undefined
        })
        window.pywebview.api.calculate_computed(computedId, [props])
          .then(response => {
            if (this.$root.computed[computedId][s].value !== response) {
              this.$set(this.$root.computed[computedId], s, {
                value: response
              })
            }
          })
        return this.$root.computed[computedId][s]
      }
    },
    assembleTemplate(id, recursive) {
      if (id === undefined || id === null) {
        return ''
      }
      const d = this.$root.componentStore[id]
      sendLog('descriptor:', d)
      if (_.isString(d)) {
        sendLog('rendering:', d)
        return this.renderTemplate(d)
      }
      if (!d.component) {
        sendLog('rendering:', '(empty)')
        return ''
      }
      d.props['data-component-id'] = id.toString()
      // sendLog(JSON.stringify(d))
      // if (('value' in d.props) && !('input' in d.events)) {
      //   const prop = d.props.value
      //   const path = getPathJs(prop, true)
      //   // The trickery with $set below is necessary 
      //   // since array-valued things are not updated properly
      //   // if normal 'variable=$event' is used.
      //   const base = getBase(prop)
      //   if ('path' in prop && prop.path.length) {
      //     let last = prop.path[prop.path.length - 1]
      //     if (_.isString(last)) {
      //       last = `'${last}'`
      //     }
      //     inputEvent = `@input="$set(${base}${path}, ${last}, $event)"`
      //   } else {
      //     inputEvent = `@input="${base}=$event"`
      //   }
      // } else {
      //   inputEvent = ''
      // }
      if ('load' in d.events && !this.loadEventFired) {
        window.pywebview.api.call_cb(d.events.load)
        this.loadEventFired = true
      }
      const classes = this.renderClasses(d.classes)
      const props = this.renderProps(d.props)
      const events = this.renderEvents(d.events)
      const children = this.renderChildren(d.children, recursive || d.recursive)
      const slots = this.renderSlots(d.slots)

      const attrs = [classes, props, events/*, inputEvent*/].join(' ')
      return `<${d.component} ${attrs}>${children}${slots}</${d.component}>`
    },
    renderClasses(classes) {
      return classes.length ? `class="${classes}"` : ''
    },
    renderProps(props) {
      return _.map(props, (prop, propName) => {
        if (prop === null) {
          return propName
        } else if (_.isObject(prop) && '@' in prop) {
          // Model
          const modelId = prop['@']
          if (('value' in prop) && !(modelId in this.$root.data)) {
            this.$root.$set(this.$root.data, modelId, prop.value)
          }
          const colon = propName.startsWith('v-') ? '' : ':'
          const modifiers = 'modifiers' in prop ? '.' + prop.modifiers.join('.') : ''
          const path = getPathJs(prop)
          return `${colon}${propName}${modifiers}="$root.data[${modelId}]${path}"`
        } else if (_.isObject(prop) && '@p' in prop) {
          // PropVar
          const propVar = prop['@p']
          const colon = propName.startsWith('v-') ? '' : ':'
          const modifiers = 'modifiers' in prop ? '.' + prop.modifiers.join('.') : ''
          const path = getPathJs(prop)
          return `${colon}${propName}${modifiers}="${propVar}${path}"`
        } else if (_.isObject(prop) && '$' in prop) {
          // JSFunction
          const colon = propName.startsWith('v-') ? '' : ':'
          return `${colon}${propName}="${prop['$']}"`
        } else if (_.isString(prop)) {
          quotedProp = prop.replace(/"/g, '&quot;')
          return `${propName}="${quotedProp}"`
        } else {
          const sProp = JSON.stringify(prop)
          return `:${propName}='${sProp}'`
        }
      }).join(' ')
    },
    renderEvents(events) {
      return _.map(events, (cb, eventName) => {
        if (_.isNumber(cb)) {
          const cb_id = cb
          return `@${eventName}="params=>window.pywebview.api.call_cb(${cb_id}, params)"`
        } else if ('$' in cb) {
          return `@${eventName}="${cb['$']}"`
        }
      }).join(' ')
    },
    renderChildren(children, recursive) {
      return _.map(children, child => {
        if (_.isString(child)) {
          return child
        } else if (recursive) {
          return this.assembleTemplate(child, recursive)
        } else {
          const childComponent = 'dynamic-component'
          child = JSON.stringify(child).replace(/'/g, "&#39;")
          return `<${childComponent} :id="${child}"></${childComponent}>`
        }
      }).join('')
    },
    renderSlots(slots) {
      return _.map(slots, (d, name) => {
        if (name == '' || name == 'default') {
          name = ''
        } else {
          name = ':' + name
        }
        const classes = this.renderClasses(d.classes)
        const props = this.renderProps(d.props)
        const events = this.renderEvents(d.events)
        const arg = 'arg' in d ? `="${d.arg}"` : ''
        // if there's no arg, normal render, if there's arg, recursive static render.
        // otherwise the PropVar's cause rendering errors.
        const children = this.renderChildren(d.children, arg !== '')
        const slots = this.renderSlots(d.slots)
        const attrs = [classes, props, events].join(' ')
        return `<template v-slot${name}${arg} ${attrs}>${children}${slots}</template>`
      }).join('')
    },
    renderTemplate(template) {
      // This works even if the template does not have any reactive variables.
      // ref. https://github.com/vuejs/vue/issues/9911
      const compiled = Vue.compile(template)
      this.$options.staticRenderFns = []
      this._staticTrees = []
      compiled.staticRenderFns.map(fn => (this.$options.staticRenderFns.push(fn)))
      return compiled.render.call(this)
    }
  }
})

const app = new Vue({
  el: '#q-app',
  data: function() {
    return {
      mainComponentId: null,
      menuId: null,
      debug: false,
      data: {}, // holds the Model values {id: value}
      computed: {}, // holds computed values
      componentStore: {}, // holds the Component specifications {id: descriptor}
      keyShortcuts: {}
    }
  },
  created() {
    document.addEventListener('keydown', (event) => {
      if (
        event.metaKey == true &&
        event.key in this.keyShortcuts
      ) {
        const cbId = this.keyShortcuts[event.key]
        window.pywebview.api.call_cb(cbId, {})
        event.preventDefault()
      }
    })
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
    setMenu(component) {
      if (component === false) {
        this.menuId = null
      } else {
        const id = this.registerComponent(component)
        this.menuId = id
      }
    },
    setKeyShortcut(key, cbId) {
      this.keyShortcuts[key] = cbId
    },
    registerComponent(component, refresh = false) {
      if (refresh || (component.id in this.componentStore === false)) {
        this.$set(this.componentStore, component.id, component)
      }
      const _childrenToIds = (component) => {
        const children = component.children || []
        component.children = children.map(child => {
          return _.isObject(child) ? this.registerComponent(child, refresh) : child
        })
      }
      _childrenToIds(component)
      _.each(component.slots, slot => {
        _childrenToIds(slot)
      })
      return component.id
    },
    refreshComponent(component) {
      this.registerComponent(component, refresh = true)
    },
    getData(id) {
      return this.data[id]
    },
    setData(payload) {
      payload.forEach(({
        id,
        path,
        value
      }) => this._setData(id, path, value))
    },
    _setData(id, path, value) {
      if (path.length) {
        let target = this.data[id]
        for (let i = 0; i < path.length - 1; i++) {
          target = target[path[i]]
        }
        this.$set(target, path[path.length - 1], value)
        return
      }
      const idIsNew = id in this.data === false
      this.$set(this.data, id, value)
      if (idIsNew) {
        this.$watch(`data.${id}`, {
          handler: v => {
            window.pywebview.api.set_model_value(id, v)
          },
          deep: _.isObject(value)
        })
      }
    },
    setComputedValue({
      id,
      propsJson,
      value
    }) {
      this.$set(this.computed[id], propsJson, value)
    },
    addScripts(sources) {
      sources.forEach(src => {
        const node = document.createElement('script')
        node.setAttribute('src', src)
        document.body.appendChild(node)
      })
    },
    addStyles(sources) {
      sources.forEach(src => {
        const node = document.createElement('link')
        node.setAttribute('rel', 'stylesheet')
        node.setAttribute('href', src)
        document.head.appendChild(node)
      })
    },
    callComponentMethod({
      component_id,
      method
    }) {
      // We shoot into the structure wherever we find data-component-id 
      // then the vue component must be somewhere among the parents.
      // This is clearly madness but it seems to work for now, for q-input validation. 
      var el = document.querySelector(`[data-component-id="${component_id}"]`)
      sendLog(JSON.stringify(el.tagName))
      if (el === undefined) {
        return
      }
      for (;; el = el.parentNode) {
        sendLog(JSON.stringify(el.tagName))
        if ('__vue__' in el)
          break
        if (el === null) {
          return
        }
      }
      that = el.__vue__
      if (method in that) {
        return that[method].bind(that)()
      } else {
        that = that.$children[0]
        return that[method].bind(that)()
      }
    }
  }
})