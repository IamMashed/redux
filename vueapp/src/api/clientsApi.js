import api from './index'

const resource = 'clients'

export default {

	/**
	 * Get all applications
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

	/**
	 * Load Client
	 * @param {Number} id Client id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create Client
	 * @param {Object} payload Client model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update Client
	 * @param {Object} payload Client model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Client
	 * @param {Object} payload Client model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}