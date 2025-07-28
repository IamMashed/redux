import api from './index'

const resource = 'assessments'

export default {

	/**
	 * Update assessment
	 * @param {Object} payload assessment model
	 */
	update(payload) {
		return api.put(`${resource}/${payload.id}`, payload)
	},

}