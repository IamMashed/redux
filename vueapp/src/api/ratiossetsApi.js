import api from './index'

const resource = 'ratiossets'

export default {

	/**
	 * Load ratiossets
	 */
	getAll() {
		return api.get(`${resource}`)
	},
	
}