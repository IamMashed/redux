import api from './index'

const resource = 'obsolescence-rules'

export default {

	/**
	 * Load Obsolescences Rules
	 */
	getAll(params) {
		return api.get(`${resource}`, {
			params,
		})
	},
	
}