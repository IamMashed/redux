const state = {
	
}

const getters = {
	entities: (state, getters, rootState, { 'applications/statuses': statuses}) => {
		return [
			{
				name: 'case_client',
				icon: 'mdi-account-outline',
				route: 'client',
				groupName: 'Clients',
			},
			{
				name: 'property',
				icon: 'mdi-home-outline',
				route: 'cma-compare',
				groupName: 'Properties',
			},
			{
				name: 'case_property',
				icon: 'mdi-home-lightbulb-outline',
				route: 'client-case',
				params: (item) => {
					const { id, client_id } = item?.item
					return {
						id: client_id,
						caseid: id,
					}
				},
				groupName: 'Cases',
			},
			{
				name: 'case_application',
				icon: 'mdi-file-document-outline',
				route: 'application',
				params: (item) => {
					const { status_id } = item?.item
					const status = statuses.find(item => item.id === status_id)
					return {
						status: status?.key,
					}
				},
				groupName: 'Applications',
			},
		]
	},
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