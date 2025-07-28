import api from './index'

const resource = 'applications'

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
	 * Load Application
	 * @param {Number} id Application id
	 */
	get(id = Number) {
		return api.get(`${resource}/${id}`)
	},

	/**
	 * Create Application
	 * @param {Object} payload Application model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update Application
	 * @param {Object} payload Application model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete Application
	 * @param {Object} payload Application model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

	/**
	 * Review Application
	 * @param {Object} payload Application model
	 */
	review(payload) {
		return api.put(`${resource}/${payload.id}/review`, payload)
	},

	/**
	 * Approve Application
	 * @param {Object} payload Application model
	 */
	approve(payload) {
		return api.put(`${resource}/${payload.id}/approve`, payload)
	},

	/**
	 * Reject Application
	 * @param {Object} payload Application model
	 */
	reject(payload) {
		return api.put(`${resource}/${payload.id}/reject`, payload)
	},

	/**
	 * Fully Reject Application
	 * @param {Object} payload Application model
	 */
	fullyReject(payload) {
		return api.put(`${resource}/${payload.id}/fully-reject`, payload)
	},

	/**
	 * Generate repair token
	 * @param {Number} id Application model id
	 */
	repair(id) {
		return api.get(`${resource}/${id}/repair`)
	},

	/**
	 * Send Sign Email to Client
	 * @param {Number} id Application model id
	 */
	sendSignEmail(id) {
		return api.get(`${resource}/${id}/sign-email`)
	},
}