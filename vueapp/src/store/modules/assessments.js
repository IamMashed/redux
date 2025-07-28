const state = {
	types: [
		{
			value: 1,
			text: 'Final',
		},
		{
			value: 2,
			text: 'Tentative',
		},
		{
			value: 3,
			text: 'School',
		},
	],
}

const getters = {
	types: ({ types }) => types,
}

export default {
	namespaced: true,
	state,
	getters,
}