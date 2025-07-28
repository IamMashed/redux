const state = {
	county: null,
}

const getters = {
	county: ({ county }) => county,
}

const mutations = {
	SET_COUNTY(state, payload) {
		state.county = payload
	},
}

const actions = {
	
}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations,
}