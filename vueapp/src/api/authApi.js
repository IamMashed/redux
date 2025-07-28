import api from './index'

const resource = 'auth'

export default {

	/**
	 * Load User Auth data
	 */
	user(params) {
		return api.get(`${resource}`, {
			params,
		})
	},
	
}