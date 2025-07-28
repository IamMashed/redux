import api from './index'

const resource = 'notes'

export default {

	/**
	 * Load Notes
	 * @param {Object} params get params
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

	/**
	 * Load Note
	 * @param {Number} id Note id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create Note
	 * @param {Object} payload Note model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update Note
	 * @param {Object} payload Note model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Note
	 * @param {Object} payload Note model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}