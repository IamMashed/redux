import api from './index'

const resource = 'notes'

export default {

	/**
	 * Load Application Notes
	 * @param {Number} applicationId Application id
	 * @param {Object} params get params
	 */
	getAll(applicationId = Number, params) {
		return api.get(`applications/${applicationId}/${resource}`, {
			params,
		})
	},

	/**
	 * Load Application Note
	 * @param {Number} applicationId Application id
	 * @param {Number} id Application Note id
	 */
	get(applicationId = Number, id = Number) {
		return api.get(`applications/${applicationId}/${resource}/${id}`)
	},

	/**
	 * Create Application Note
	 * * @param {Number} applicationId Application id
	 * @param {Object} payload Application Note model
	 */
	create(applicationId = Number, payload) {
		return api.post(`applications/${applicationId}/${resource}`, payload)
	},

	/**
	 * Update Application Note
	 * @param {Object} payload Application Note model
	 */
	update(payload) {
		return api.put(`applications/${payload.application_id}/${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Application Note
	 * @param {Object} payload Application Note model
	 */
	delete(payload) {
		return api.delete(`applications/${payload.application_id}/${resource}/${payload.id}`)
	},

}