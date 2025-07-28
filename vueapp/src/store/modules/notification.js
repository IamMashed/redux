const state = {
	show: false,
	color: '',
	text: '',
}

const getters = {
	show: ({ show }) => show,
	color: ({ color }) => color,
	text: ({ text }) => text,
}

const mutations = {
	SET_SHOW(state, payload) {
		state.show = payload
	},
	SET_TEXT(state, payload) {
		state.text = payload
	},
	SET_COLOR(state, payload) {
		state.color = payload
	},
}

const actions = {
	notify: {
		root: true,
		handler({ commit }, { text, color }) {
			commit('SET_TEXT', text)
			commit('SET_COLOR', color)
			commit('SET_SHOW', true)
		},
	},
}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations,
}