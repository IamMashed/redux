import api from './index'

const resource = 'settings/time-adjustments'

export default {

	/**
	 * Load time adjustments
	 */
	getAll() {
		return api.get(`${resource}`)
	},

	/**
	 * Create time adjustment
	 * @param {Object} payload time adjustment model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update time adjustment
	 * @param {Object} payload time adjustment model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete time adjustment
	 * @param {Object} payload time adjustment model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}