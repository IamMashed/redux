/**
 * Mixin to translate county key/id into name
 * using counties vuex state
 */
export default {
	methods: {
		/**
		 * Translate county id into county name
		 * @param {String} value county id
		 * 
		 * @returns {String} county name
		 */
		countyFilter(countyId) {
			const county = this.counties?.find(item => item.id === countyId)
			return county?.name
		},
	},
}