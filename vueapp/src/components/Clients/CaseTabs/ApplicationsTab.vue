<template>
	<v-container class="pa-4">
		<v-data-table
			:items="applications"
			:headers="headers"
			:items-per-page="-1"
			hide-default-footer>

			<template #item.created_at="{ value }">
				{{ value | date }}
			</template>

			<template #item.updated_at="{ value }">
				{{ value | date }}
			</template>

			<template #item.action="{ item }">
				<v-btn
					:href="`${VUE_APP_API}applications/${item.id}/attachment`"
					target="_blank"
					color="info"
					outlined
					depressed
					small>
					Download
				</v-btn>
			</template>
		</v-data-table>
	</v-container>
</template>

<script>
import { apiFactory } from '../../../api/apiFactory'

const applicationsApi = apiFactory.get('applications')

export default {
	props: {
		case: {
			type: Object,
			required: true,
		},
	},
	data: () => ({
		VUE_APP_API: process.env.VUE_APP_API,
		applications: [],
		headers: [
			{
				text: 'Full Address',
				value: 'full_address',
			},
			{
				text: 'Tax Year',
				value: 'tax_year',
			},
			{
				text: 'Status',
				value: 'status.name',
			},
			{
				text: 'Created At',
				value: 'created_at',
			},
			{
				text: 'Updated At',
				value: 'updated_at',
			},
			{
				text: 'Action',
				value: 'action',
			},
		],
	}),
	methods: {
		async loadApplications() {
			try {
				const { property_id, tax_year } = this.case
				const status_id = 2
				const { data } = await applicationsApi.getAll({
					property_id,
					tax_year,
					status_id,
				})
				this.applications = data
			} catch(error) {
				this.notify({
					text: 'Can not load Applications',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.loadApplications()
	},
}
</script>