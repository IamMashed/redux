import api from './index'

const resource = 'payment-statuses'

export default {

	/**
	 * Load Payment Statuses
	 */
	getAll() {
		return api.get(`${resource}`)
	},
	
}