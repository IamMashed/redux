const state = {
	show: true,
}

const getters = {
	show: ({ show }) => show,
}

const mutations = {
	SET_SHOW(state, payload) {
		state.show = payload
	},
}

const actions = {
	toggle({ commit, getters }) {
		commit('SET_SHOW', !getters.show)
	},
}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations,
}