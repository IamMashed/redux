import api from './index'

const resource = 'application-sources'

export default {

	/**
	 * Load Application Sources
	 */
	getAll() {
		return api.get(`${resource}`)
	},
	
}