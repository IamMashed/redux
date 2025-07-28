import api from './index'

const resource = 'constants'

export default {

	/**
	 * Get all constants
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

}