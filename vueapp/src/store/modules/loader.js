const state = {
	show: false,
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
	set({ commit }, value) {
		commit('SET_SHOW', value)
	},
}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations,
}