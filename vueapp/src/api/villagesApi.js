import api from './index'

const resource = 'counties'

export default {

	/**
	 * Get villages by county id
	 */
	getAll(countyid) {
		return api.get(`${resource}/${countyid}/villages`)
	},

}