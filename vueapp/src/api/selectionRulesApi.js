import api from './index'

const resource = 'selection-rules'

export default {

	/**
	 * Load Selection Rules
	 */
	getAll() {
		return api.get(`${resource}`)
	},

	/**
	 * Load Selection Rule
	 * @param {Number} id Selection Rule id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create Selection Rule
	 * @param {Object} payload Selection Rule model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update Selection Rule
	 * @param {Object} payload Selection Rule model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Selection Rule
	 * @param {Object} payload Selection Rule model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}