import api from './index'

const resource = 'global-settings'

export default {

	/**
	 * Get all settings
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

	/**
	 * Update county settings
	 * @param {Object} payload settings model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

}