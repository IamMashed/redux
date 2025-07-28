<template>
	<v-container>

		<h1 class="primary--text">Assessment Dates</h1>

		<a-table
			:items="items"
			:headers="headers"
			:schema="schema"
			:uiSchema="uiSchema"
			@update="updateItem"
			@delete="deleteItem">

			<template #item.county="{ item }">
				{{ countyFilter(item.county) }}
			</template>

			<template #item.files="{ item }">
				{{ item.files.map(({ file_name }) => file_name).join(', ') }}
			</template>

			<template #item.assessment_type="{ item }">
				{{ types.find(type => type.value === item.assessment_type).text }}
			</template>

			<template #item.valuation_date="{ item }">
				{{ item.valuation_date | date }}
			</template>
		</a-table>

	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import countyFilter from '../mixins/countyFilter'

import ATable from '../components/ATable'

const assessmentDatesApi = apiFactory.get('assessment-dates')

export default {
	components: {
		ATable,
	},
	mixins: [
		countyFilter,
	],
	data: () => ({
		items: [],
		schema: {
			type: 'object',
			properties: {
				assessment_name: {
					type: 'string',
				},
				assessment_type: {
					type: 'string',
				},
				valuation_date: {
					type: 'string',
				},
				release_date: {
					type: 'string',
				},
				tax_year: {
					type: 'string',
				},
			},
		},
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
		]),
		...mapGetters('counties', [
			'counties',
		]),
		...mapGetters('assessments', [
			'types',
		]),
		headers() {
			return [
				{
					text: 'County',
					value: 'county',
				},
				{
					text: 'Name',
					value: 'assessment_name',
				},
				{
					text: 'File',
					value: 'files',
				},
				{
					text: 'Type',
					value: 'assessment_type',
				},
				{
					text: 'Valuation Date',
					value: 'valuation_date',
				},
				{
					text: 'Release Date',
					value: 'release_date',
				},
				{
					text: 'Tax Year',
					value: 'tax_year',
				},
				...(
					this.isAdmin ?
					[{
						text: 'Actions',
						value: 'actions',
					}] : []
				),
			]
		},
		uiSchema() {
			return [
				{
					component: 'v-text-field',
					model: 'assessment_name',
					fieldOptions: {
						class: ['flex xs12'],
						on: ['input'],
						attrs: {
							label: 'Name',
							type: 'text',
						},
					},
				},
				{
					component: 'v-select',
					model: 'assessment_type',
					fieldOptions: {
						class: ['flex xs12'],
						on: ['input'],
						attrs: {
							label: 'Type',
							items: this.types,
						},
					},
				},
				{
					component: 'a-date',
					model: 'valuation_date',
					fieldOptions: {
						class: ['flex xs6'],
						on: ['input'],
						attrs: {
							label: 'Valuation Date',
						},
					},
				},
				{
					component: 'a-date',
					model: 'release_date',
					fieldOptions: {
						class: ['flex xs6'],
						on: ['input'],
						attrs: {
							label: 'Release Date',
						},
					},
				},
				{
					component: 'v-text-field',
					model: 'tax_year',
					fieldOptions: {
						class: ['flex xs6 mt-3'],
						on: ['input'],
						attrs: {
							label: 'Tax Year',
							type: 'text'
						},
					},
				},
			]
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		async loadItems() {
			try {
				const { data } = await assessmentDatesApi.getAll()
				this.items = data
			} catch(error) {
				this.notify({
					text: 'Can not load Assessment Dates',
					color: 'error'
				}, { root: true })
			}
		},
		async updateItem(item, index) {
			try {
				await assessmentDatesApi.update(item)
				this.$set(this.items, index, item)
				this.notify({
					text: 'Assessment Date updated',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not update Assessment Date',
					color: 'error'
				}, { root: true })
			}
		},
		async deleteItem(item, index) {
			try {
				await assessmentDatesApi.delete(item)
				this.$delete(this.items, index)
				this.notify({
					text: 'Assessment Date deleted',
					color: 'error'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not delete Assessment Date',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.loadItems()
	},
}
</script>