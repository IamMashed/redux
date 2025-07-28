import { apiFactory } from '@/api/apiFactory'

const countiesApi = apiFactory.get('counties')

const state = {
	counties: [],
}

const getters = {
	counties: ({ counties }) => counties,
}

const mutations = {
	SET_COUNTIES(state, payload) {
		state.counties = payload
	},
}

const actions = {
	async loadCounties({ commit, dispatch }) {
		try {
			const { data } = await countiesApi.getAll()
			commit('SET_COUNTIES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load counties',
				color: 'error'
			}, { root: true })
		}
	},
}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations,
}