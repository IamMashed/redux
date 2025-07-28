import api from './index'

const resource = 'lookup'

export default {

	/**
	 * Lookup clients
	 */
	clients(payload) {
		return api.post(`${resource}/case_client`, payload)
	},

	/**
	 * Lookup cases
	 */
	cases(payload) {
		return api.post(`${resource}/case_property`, payload)
	},

	/**
	 * Get Cases Report
	 * @param {Object} payload Filters
	 */
	casesReport(payload) {
		return api.post(`${resource}/case_property/report`, payload)
	},

	/**
	 * Export Cases Folio TXT
	 * @param {Object} payload Filters
	 */
	casesFolioTXT(payload) {
		// TODO: update url
		return api.post(`${resource}/case_property/case_list`, payload)
	},

	/**
	 * Export Cases Extended TXT
	 * @param {Object} payload Filters
	 */
	casesExtendedTXT(payload) {
		// TODO: update url
		return api.post(`${resource}/case_property/case_extended_list`, payload)
	},

	/**
	 * Export Petition Report Excel
	 * @param {Object} payload Filters
	 */
	petitionsReport(payload) {
		return api.post(`${resource}/case_property/petitions-report`, payload, {
			responseType: 'blob',
		})
	},

	/**
	 * Export Lookup Results CSV
	 * @param {Object} payload Filters
	 */
	exportLookupResults(payload) {
		return api.post(`${resource}/case_property/lookup-results`, payload, {
			responseType: 'blob',
		})
	},

}