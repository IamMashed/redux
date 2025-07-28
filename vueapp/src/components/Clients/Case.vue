<template>
	<v-card
		height="100%"
		outlined>
		<v-card-title>
			<v-btn
				class="mr-2"
				icon
				small
				:to="{
					name: 'client',
					params: {
						id: caseProperty.client_id,
					},
				}">
				<v-icon>mdi-chevron-left</v-icon>
			</v-btn>
			Case ID: {{ caseProperty.case_id }}
			<v-spacer></v-spacer>
			Tax Year: {{ caseProperty.tax_year }}
		</v-card-title>
		<v-divider></v-divider>

		<case-list-item
			:value="caseProperty"
			:clickable="false">
		</case-list-item>
		
		<v-divider></v-divider>
		<v-tabs
			v-model="detailsTab"
			grow>
			<v-tab to="#general">General</v-tab>
			<v-tab to="#info">Info</v-tab>
			<v-tab to="#town">Town</v-tab>
			<v-tab to="#village">Village</v-tab>
			<v-tab to="#saved-cma">Saved CMA's</v-tab>
			<v-tab to="#applications">Applications</v-tab>
			<v-tab to="#documents">Documents</v-tab>
			<v-tab to="#billing-history">Billing History</v-tab>
		</v-tabs>

		<v-tabs-items
			v-model="detailsTab"
			class="transparent">
			<v-tab-item value="general">
				<general-tab
					v-model="caseProperty"
					@input="updateCase">
				</general-tab>
			</v-tab-item>
			<v-tab-item value="info"></v-tab-item>
			<v-tab-item value="town"></v-tab-item>
			<v-tab-item value="village"></v-tab-item>
			<v-tab-item value="saved-cma" eager>
				<workups-tab
					:case="caseProperty">
				</workups-tab>
			</v-tab-item>
			<v-tab-item value="applications">
				<applications-tab
					:case="caseProperty">
				</applications-tab>
			</v-tab-item>
		</v-tabs-items>

		<confirm ref="confirm"></confirm>
	</v-card>
</template>

<script>
import { mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'

import CaseListItem from './CaseListItem'
import GeneralTab from './CaseTabs/GeneralTab'
import ApplicationsTab from './CaseTabs/ApplicationsTab'
import WorkupsTab from './CaseTabs/WorkupsTab'

const casesApi = apiFactory.get('cases')

export default {
	components: {
		CaseListItem,
		GeneralTab,
		ApplicationsTab,
		WorkupsTab,
	},
	props: {
		caseid: {
			type: Number,
			required: true,
		},
		items: {
			type: Array,
			required: true,
		},
	},
	data: () => ({
		caseProperty: {},
		detailsTab: 0,
	}),
	computed: {
		property() {
			return this.caseProperty?.property || {}
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		...mapActions('constants', [
			'loadConstants',
		]),
		
		async loadCase(id) {
			try {
				const { data } = await casesApi.get(id)
				this.caseProperty = data
			} catch(error) {
				this.notify({
					text: 'Can not load Case',
					color: 'error'
				}, { root: true })
			}
		},

		async updateCase(caseProperty) {
			try {
				const { data } = await casesApi.update(caseProperty)
				this.caseProperty = data
				this.notify({
					text: 'Case updated',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not update Case',
					color: 'error'
				}, { root: true })
			}
		},

		async deleteCase() {
			try {
				const confirm = await this.$refs.confirm.open(
					'Delete Case',
					`Are you certain you want to permanently delete the Case? To continue, type 'delete me' in the dialog box and click Delete`,
					{
						color: 'error',
						width: 400,
						promptText: 'delete me',
					})
				if(confirm) {
					await casesApi.delete(this.caseProperty)
					this.$router.push({
						name: 'client',
						params: {
							...this.$route.params,
						},
					})
					this.notify({
						text: 'Case deleted',
						color: 'success'
					}, { root: true })
				}
			} catch (error) {
				this.notify({
					text: 'Can not delete Case',
					color: 'error'
				}, { root: true })
			}
		},
	},
	watch: {
		'caseid': {
			immediate: true,
			deep: true,
			handler: async function(newVal) {
				await this.loadCase(newVal)
				this.loadConstants({ county: this.property?.county })
			},
		},
	},
}
</script>