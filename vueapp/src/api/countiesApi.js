import api from './index'

const resource = 'counties'

export default {

	/**
	 * Get all counties
	 */
	getAll() {
		return api.get(`${resource}`)
	},

}