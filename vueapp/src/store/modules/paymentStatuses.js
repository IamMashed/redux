import { apiFactory } from '@/api/apiFactory'

const paymentStatusesApi = apiFactory.get('payment-statuses')

const state = {
	paymentStatuses: [],
}

const getters = {
	paymentStatuses: ({ paymentStatuses }) => paymentStatuses,
}

const mutations = {
	SET_PAYMENT_STATUSES(state, payload) {
		state.paymentStatuses = payload
	},
}

const actions = {
	async loadPaymentStatuses({ commit, dispatch }) {
		try {
			const { data } = await paymentStatusesApi.getAll()
			commit('SET_PAYMENT_STATUSES', data)
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load payment statuses',
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