import api from './index'

const resource = 'upload'

export default {

	/**
	 * Process Petition File
	 * @param {FormData} payload FormData with valid file
	 */
	petition(payload) {
		return api.post(`${resource}/petition`, payload, {
			headers: {
				'Content-Type': 'multipart/form-data',
			},
		})
	},
}