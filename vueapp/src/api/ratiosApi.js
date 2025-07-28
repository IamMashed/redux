import api from './index'

const resource = 'ratiossets/ratios'

export default {

	/**
	 * Load ratios
	 */
	getAll() {
		return api.get(`${resource}`)
	},

	/**
	 * Create ratio
	 * @param {Object} ratio ratio model
	 */
	create(ratio) {
		return api.post(`${resource}`, ratio)
	},

	/**
	 * Update ratio
	 * @param {Object} ratio ratio model
	 */
	update(ratio) {
		return api.put(`${resource}/${ratio.id}`, ratio)
	},

	/**
	 * Delete ratio
	 * @param {Object} ratio ratio model
	 */
	delete(ratio) {
		return api.delete(`${resource}/${ratio.id}`)
	},

}