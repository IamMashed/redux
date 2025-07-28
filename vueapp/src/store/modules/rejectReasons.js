import { apiFactory } from '@/api/apiFactory'

const rejectReasonsApi = apiFactory.get('reject-reasons')

const state = {
	rejectReasons: [],
}

const getters = {
	rejectReasons: ({ rejectReasons }) => rejectReasons,
}

const mutations = {
	SET_REJECT_REASONS(state, payload) {
		state.rejectReasons = payload
	},
}

const actions = {
	async loadRejectReasons({ commit, dispatch }) {
		try {
			const { data } = await rejectReasonsApi.getAll()
			commit('SET_REJECT_REASONS', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load reject reasons',
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