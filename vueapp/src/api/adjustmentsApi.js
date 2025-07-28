import api from './index'

const resource = 'adjustments'

export default {

	/**
	 * Get all adjustments
	 */
	getAll() {
		return api.get(`${resource}`)
	},

}