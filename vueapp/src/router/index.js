import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './routes'
import store from '../store'

Vue.use(VueRouter)

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
})

router.beforeEach(async (to, from, next) => {
	if(to.matched.some(record => !!record.meta.auth)) {
		let isLoggedIn = store.getters['auth/isLoggedIn']
		if(!isLoggedIn) {
			await store.dispatch('auth/loadUser')
			store.dispatch('applications/loadCaseInfo')
			store.dispatch('counties/loadCounties')
			isLoggedIn = store.getters['auth/isLoggedIn']
		}
		
		const allowedRoles = to.meta.allowedRoles
		const userRole = store.getters['auth/userRole']
		const isAllowed = allowedRoles?.some(role => role === userRole)

		if(isLoggedIn && isAllowed) {
			next()
			return
		}
		next('/login') 
	} else {
		next() 
	}
})

export default router