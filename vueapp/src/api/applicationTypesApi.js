import api from './index'

const resource = 'application-types'

export default {

	/**
	 * Load Owner Types
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},
	
}