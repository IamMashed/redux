import Vue from 'vue'
import App from './App.vue'
// import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import VueScrollTo from 'vue-scrollto'
import panZoom from 'vue-panzoom'
import './filters'
import Confirm from '@/components/Confirm.vue'
import ADate from '@/components/ADate.vue'
import VAutonumeric from '@/components/VAutonumeric.vue'
import VMaskInput from '@/components/VMaskInput'

Vue.use(panZoom)
Vue.use(VueScrollTo)

Vue.component('confirm', Confirm)
Vue.component('a-date', ADate)
Vue.component('v-autonumeric', VAutonumeric)
Vue.component('v-mask-input', VMaskInput)

Vue.config.productionTip = false

new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
}).$mount('#app')