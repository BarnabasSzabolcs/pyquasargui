const quasarPlugins = {
    notify(app, params){
      const longTimeOut = 7000
      defaults = {
        type: '',
        timeout: longTimeOut,
        position: 'top',
        message: '',
        multiline: true
      }
      params = _.defaults(params, defaults)
      app.$q.notify(params)
    },
    dialog(app, params, events){
      const dialog = app.$q.dialog(params)
      _.each(events, (cb, name)=>{
        const eventName = `on${name[0].toUpperCase()}${name.slice(1)}`
        dialog[eventName](toCallback(cb))
      })
    },
    bottomSheet(app, params, events){
      const dialog = app.$q.bottomSheet(params)
      _.each(events, (cb, name)=>{
        const eventName = `on${name[0].toUpperCase()}${name.slice(1)}`
        dialog[eventName](toCallback(cb))
      })
    }
}
