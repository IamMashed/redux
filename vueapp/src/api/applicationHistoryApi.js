import api from './index'

const resource = 'history'

export default {

	/**
	 * Get all history for Application
	 * @param {Number} applicationId Application id
	 */
	getByApplication(applicationId = Number) {
		return api.get(`applications/${applicationId}/${resource}`)
	},

}