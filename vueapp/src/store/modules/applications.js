import { apiFactory } from '@/api/apiFactory'

const infoApi = apiFactory.get('info')

const state = {
	caseInfo: {},
	statuses: [
		{
			id: 1,
			text: 'Incoming',
			key: 'incoming',
			show: true,
			countable: true,
		},
		{
			id: 3,
			text: 'Rejected',
			key: 'rejected',
			show: true,
			countable: true,
		},
		{
			id: 5,
			text: 'Approved For Review',
			key: 'reviewed',
			show: true,
			countable: true,
		},
		{
			id: 2,
			text: 'Approved',
			key: 'approved',
			show: false,
			countable: false,
		},
		{
			id: 4,
			text: 'Fully Rejected',
			key: 'fully_rejected',
			show: true,
			countable: false,
		},
	],
}

const getters = {
	total: (state, { countableStatuses }) => {
		return Object.values(countableStatuses).reduce((sum, val) => sum + val?.count, 0)
	},
	statuses: ({ caseInfo, statuses }) => {
		return statuses.map(item => {
			const status = caseInfo[item.key]
			return {
				...item,
				...status,
			}
		})
	},
	countableStatuses: (state, { statuses }) => {
		return statuses.filter(item => item.countable)
	},
	activeStatuses: (state, { statuses }) => {
		return statuses.filter(item => item.show)
	},
	defaultStatus: (state, { statuses }) => {
		const status = {
			key: 'incoming',
			applications: [ '0' ],
		}
		return statuses.filter(item => item.count)?.[0] || status
	},
}

const mutations = {
	SET_CASE_INFO(state, payload) {
		state.caseInfo = payload
	},
}

const actions = {
	async loadCaseInfo({ commit, dispatch, rootGetters }) {
		const isPTRC = rootGetters['auth/isPTRC']
		const isAdmin = rootGetters['auth/isAdmin']
		const isMember = rootGetters['auth/isMember']
		const isViewer = rootGetters['auth/isViewer']

		try {
			if(!isPTRC && (isAdmin || isMember || isViewer)) {
				const { data } = await infoApi.caseInfo()
				commit('SET_CASE_INFO', data)
			}
		} catch (error) {
			dispatch('notify', {
				text: 'Can not load case info',
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