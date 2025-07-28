import api from './index'

const resource = 'payment-types'

export default {

	/**
	 * Load Payment Types
	 */
	getAll() {
		return api.get(`${resource}`)
	},
	
}