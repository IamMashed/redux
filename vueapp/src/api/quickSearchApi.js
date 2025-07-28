import api from './index'

const resource = 'quick-search'

export default {

	/**
	 * Search in properties, clients and cases
	 * @param {String} params
	 */
	search(params) {
		return api.get(`${resource}`, {
			params,
		})
	},

}