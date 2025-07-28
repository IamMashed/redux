import api from './index'

const resource = 'reject-reasons'

export default {

	/**
	 * Load Application Reject Reasons
	 */
	getAll() {
		return api.get(`${resource}`)
	},
	
}