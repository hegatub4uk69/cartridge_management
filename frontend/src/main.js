/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import router from '@/router'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import { store } from './store';

// Styles
import 'unfonts.css'

const app = createApp(App)

registerPlugins(app)
app.use(router)
app.use(store)
app.mount('#app')
