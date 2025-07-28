import api from './index'

const resource = 'case-properties'

export default {

	/**
	 * Get all cases
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

	/**
	 * Load case
	 * @param {Number} id case id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create case
	 * @param {Object} payload case model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update case
	 * @param {Object} payload case model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete case
	 * @param {Object} payload case model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

	/**
	 * Load Case's Workups
	 * @param {Number} id Case id
	 */
	singleCmaWorkups(id = Number) {
		return api.get(`${resource}/${id}/single-cma-workups`)
	},

}