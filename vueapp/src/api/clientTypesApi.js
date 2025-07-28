import api from './index'

const resource = 'client-types'

export default {

	/**
	 * Get all client types
	 */
	getAll() {
		return api.get(`${resource}`)
	},

}