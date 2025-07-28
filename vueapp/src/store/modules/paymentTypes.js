import { apiFactory } from '@/api/apiFactory'

const paymentTypesApi = apiFactory.get('payment-types')

const state = {
	paymentTypes: [],
}

const getters = {
	paymentTypes: ({ paymentTypes }) => paymentTypes,
}

const mutations = {
	SET_PAYMENT_TYPES(state, payload) {
		state.paymentTypes = payload
	},
}

const actions = {
	async loadPaymentTypes({ commit, dispatch }) {
		try {
			const { data } = await paymentTypesApi.getAll()
			commit('SET_PAYMENT_TYPES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load payment types',
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