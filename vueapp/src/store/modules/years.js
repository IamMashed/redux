const state = {
	startYear: 2011,
	endYear: new Date().getFullYear() + 2,
}

const getters = {
	/**
	 * Get array of years
	 */
	years: ({ startYear, endYear }) =>{
		return Array(endYear - startYear + 1)
				.fill('')
				.map((y, i) => endYear - i)
	},
}

export default {
	namespaced: true,
	state,
	getters,
}