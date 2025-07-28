import Vue from 'vue'
import Vuex from 'vuex'
import sidebar from './modules/sidebar'
import notification from './modules/notification'
import loader from './modules/loader'
import auth from './modules/auth'
import search from './modules/search'
import applications from './modules/applications'
import years from './modules/years'
import constants from './modules/constants'
import counties from './modules/counties'
import adjustments from './modules/adjustments'
import obsolescences from './modules/obsolescences'
import assessments from './modules/assessments'
import tags from './modules/tags'
import users from './modules/users'
import roles from './modules/roles'
import applicationTypes from './modules/applicationTypes'
import applicationSources from './modules/applicationSources'
import marketingCodes from './modules/marketingCodes'
import rejectReasons from './modules/rejectReasons'
import clientTypes from './modules/clientTypes'
import paymentTypes from './modules/paymentTypes'
import paymentStatuses from './modules/paymentStatuses'
import lookup from './modules/lookup'
import cma from './modules/cma'

import VuexORM from './plugins/vuex-orm'

Vue.use(Vuex)

export default new Vuex.Store({
	modules: {
		sidebar,
		notification,
		loader,
		auth,
		search,
		applications,
		years,
		constants,
		counties,
		adjustments,
		obsolescences,
		assessments,
		tags,
		users,
		roles,
		applicationTypes,
		applicationSources,
		marketingCodes,
		rejectReasons,
		clientTypes,
		paymentTypes,
		paymentStatuses,
		lookup,
		cma,
	},
	state: {
	},
	mutations: {
	},
	actions: {
	},
	plugins: [
		VuexORM,
	],
})