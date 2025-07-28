import api from './index'

const resource = 'settings/assessment-dates'

export default {

	/**
	 * Load assessment dates
	 */
	getAll() {
		return api.get(`${resource}`)
	},

	/**
	 * Get rule sets for this assessment date
	 * @param {Number} id assessment date id
	 */
	getRuleSets(id) {
		return api.get(`${resource}/${id}/rule-sets`)
	},

	/**
	 * Get assessment for this assessment date
	 * @param {Number} id assessment date id
	 * @param {Object} params assessmnet filter params
	 */
	getAssessments(id, params) {
		return api.get(`${resource}/${id}/assessments`, {
			params,
		})
	},

	/**
	 * Create assessment date
	 * @param {Object} payload assessment date model
	 */
	create(payload) {
		return api.post(`${resource}`, payload)
	},

	/**
	 * Update assessment date
	 * @param {Object} payload assessment date model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

	/**
	 * Delete assessment date
	 * @param {Object} payload assessment date model
	 */
	delete(payload) {
		return api.delete(`${resource}/${payload.id}`)
	},

}