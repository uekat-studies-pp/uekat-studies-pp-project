import { createApp } from 'vue'
import { Quasar } from 'quasar'
import { createPinia } from 'pinia'

import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'


import App from './App.vue'

const pinia = createPinia()
const myApp = createApp(App)

myApp.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
})
myApp.use(pinia)

// Assumes you have a <div id="app"></div> in your index.html
myApp.mount('#app')