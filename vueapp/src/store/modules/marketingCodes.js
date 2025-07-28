import { apiFactory } from '@/api/apiFactory'

const marketingCodesApi = apiFactory.get('marketing-codes')

const state = {
	marketingCodes: [],
}

const getters = {
	marketingCodes: ({ marketingCodes }) => marketingCodes,
}

const mutations = {
	SET_MARKETING_CODES(state, payload) {
		state.marketingCodes = payload
	},
}

const actions = {
	async loadMarketingCodes({ commit, dispatch }) {
		try {
			const { data } = await marketingCodesApi.getAll()
			commit('SET_MARKETING_CODES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load marketing codes',
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