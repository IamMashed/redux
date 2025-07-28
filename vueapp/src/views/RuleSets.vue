<template>
	<v-container>

		<h1 class="primary--text">Rule Sets</h1>

		<v-row>
			<v-col cols="12" md="3">
				<h2 class="title success--text">Filters</h2>
				<v-select
					v-model="county"
					:items="counties"
					label="County"
					:disabled="!counties[0]"
					placeholder="Select county"
					class="mt-12 pt-9"
					item-value="id"
					item-text="name">
				</v-select>
				<v-select
					v-model="town"
					:items="towns"
					label="Town/Village"
					item-text="name"
					item-value="name"
					placeholder="Select town/village"
					clearable>
				</v-select>
				<v-select
					v-model="year"
					:items="years"
					label="Year"
					placeholder="Select year">
				</v-select>
				<v-btn
					width="100%"
					class="ma-1"
					@click="loadRuleSets({
						county,
						town,
						year,
					})">Apply</v-btn>
				<v-btn
					width="100%"
					class="ma-1"
					@click="clearFilters">
					Clear
				</v-btn>
			</v-col>
			<v-col cols="12" md="9">
				<h2 class="title">Existing Rule Sets</h2>
				<a-table
					ref="table"
					:items="ruleSets"
					:headers="headers"
					:schema="schema"
					:uiSchema="uiSchema"
					:item-class="() => 'cursor-pointer'"
					@click:row="navigateToRuleSet"
					@create="createRuleSet"
					@delete="deleteRuleSet">

					<template #top
						v-if="isAdmin">
						<div class="d-flex justify-end my-4">
							<v-btn
								depressed
								color="secondary"
								class="mx-1"
								:to="{ name: 'create-rule-set' }">
								<v-icon left>mdi-pencil</v-icon>
								Create
							</v-btn>
						</div>
					</template>

					<template #item.county="{ item }">
						{{ countyFilter(item.county) }}
					</template>

					<template #item.copy="{ item }">
						<v-icon
							small
							color="secondary"
							@click.stop.prevent="copyRuleSet(item)">
							mdi-content-duplicate
						</v-icon>
					</template>

					<template #item.actions="{ item }">
						<router-link :to="{
								name: 'rule-set',
								params: {
									id: item.id,
								}
							}">
							<v-icon
								small
								class="mr-2"
								color="amber">
								mdi-pencil
							</v-icon>
						</router-link>
								
						<v-icon
							v-if="isAdmin"
							small
							color="red"
							@click.stop.prevent="$refs.table.deleteItem(item)">
							mdi-delete
						</v-icon>
					</template>
					
					<template #item.last_updated="{ item }">
						{{ item.last_updated | date }}
					</template>
					
				</a-table>
			</v-col>
		</v-row>

	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import countyFilter from '../mixins/countyFilter'

import ATable from '../components/ATable'

const townsApi = apiFactory.get('towns')
const ruleSetsApi = apiFactory.get('rule-sets')

export default {
	components: {
		ATable,
	},
	mixins: [
		countyFilter,
	],
	data: () => ({
		county: null,
		towns: [],
		town: null,
		year: null,
		ruleSets: [],
		headers: [
			{
				text: 'County',
				value: 'county',
			},
			{
				text: 'Township/Village',
				value: 'town',
			},
			{
				text: 'Year',
				value: 'year',
			},
			{
				text: 'Copy Rule Set',
				value: 'copy',
			},
			{
				text: 'Actions',
				value: 'actions',
			},
			{
				text: 'Last Updated',
				value: 'last_updated',
			},
		],
		schema: {
			type: 'object',
			properties: {
				county: {
					type: 'string',
				},
				town: {
					type: 'string',
				},
				year: {
					type: 'number',
				},
			},
		},
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
		]),
		...mapGetters('years', [
			'years',
		]),
		...mapGetters('counties', [
			'counties',
		]),
		uiSchema() {
			return [
				{
					component: 'v-select',
					model: 'county',
					fieldOptions: {
						class: ['flex xs12'],
						on: ['input'],
						attrs: {
							label: 'County',
							items: this.counties,
							'item-text': 'name',
							'item-value': 'id',
						},
					},
				},
				{
					component: 'v-select',
					model: 'town',
					fieldOptions: {
						class: ['flex xs12'],
						on: ['input'],
						attrs: {
							label: 'Township/Village',
							items: this.towns,
							'item-text': 'name',
							'item-value': 'name',
						},
					},
				},
				{
					component: 'v-text-field',
					model: 'year',
					fieldOptions: {
						class: ['flex xs12'],
						on: ['input'],
						attrs: {
							label: 'Year',
							type: 'text',
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
		...mapActions('counties', [
			'loadCounties',
		]),
		async loadTowns(countyid) {
			try {
				const { data } = await townsApi.getAll(countyid)
				this.towns = Object.entries(data).map(([key, val]) => ({
						id: key,
						name: val,
					}))
			} catch(error) {
				this.notify({
					text: 'Can not load towns',
					color: 'error'
				}, { root: true })
			}
		},
		async loadRuleSets(params) {
			try {
				const { data } = await ruleSetsApi.getAll(params)
				this.ruleSets = data
			} catch(error) {
				this.notify({
					text: 'Can not load Rule Sets',
					color: 'error'
				}, { root: true })
			}
		},
		copyRuleSet(item) {
			this.$delete(item, 'id')
			this.$delete(item, 'rule_name')
			this.loadTowns(item.county)
			this.$refs.table.addItem(item)
		},
		async createRuleSet(item) {
			try {
				await ruleSetsApi.create(item)
				this.notify({
					text: 'Rule Set create',
					color: 'success'
				}, { root: true })
				this.loadRuleSets()
			} catch (error) {
				this.notify({
					text: 'Can not create Rule Set',
					color: 'error'
				}, { root: true })
			}
		},
		async deleteRuleSet(item, index) {
			try {
				await ruleSetsApi.delete(item)
				this.$delete(this.ruleSets, index)
				this.notify({
					text: 'Rule Set deleted',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not delete Rule Set',
					color: 'error'
				}, { root: true })
			}
		},
		clearFilters() {
			this.county = null
			this.town = null
			this.year = null
			this.loadRuleSets()
		},
		navigateToRuleSet(item) {
			this.$router.push({
				name: 'rule-set',
				params: {
					id: item.id,
				}
			})
		},
	},
	mounted() {
		this.loadCounties()
		this.loadRuleSets()
	},
	watch: {
		county(val) {
			return val && this.loadTowns(val), this.town = null
		},
	},
}
</script>