import api from './index'

const resource = 'marketing-codes'

export default {

	/**
	 * Load Marketing Codes
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},
	
}