import api from './index'

const resource = 'notes'

export default {

	/**
	 * Load Client Notes
	 * @param {Number} clientId Client id
	 * @param {Object} params get params
	 */
	getAll(clientId = Number, params) {
		return api.get(`clients/${clientId}/${resource}`, {
			params,
		})
	},

	/**
	 * Load Client Note
	 * @param {Number} clientId Client id
	 * @param {Number} id Client Note id
	 */
	get(clientId = Number, id = Number) {
		return api.get(`clients/${clientId}/${resource}/${id}`)
	},

	/**
	 * Create Client Note
	 * * @param {Number} clientId Client id
	 * @param {Object} payload Client Note model
	 */
	create(clientId = Number, payload) {
		return api.post(`clients/${clientId}/${resource}`, payload)
	},

	/**
	 * Update Client Note
	 * @param {Object} payload Client Note model
	 */
	update(payload) {
		return api.put(`clients/${payload.client_id}/${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Client Note
	 * @param {Object} payload Client Note model
	 */
	delete(payload) {
		return api.delete(`clients/${payload.client_id}/${resource}/${payload.id}`)
	},

}