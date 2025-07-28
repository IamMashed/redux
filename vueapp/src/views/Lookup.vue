<template>
	<div>
		<v-toolbar
			dense
			elevation="0">
			<v-app-bar-nav-icon
				@click="toggleSidebar">
			</v-app-bar-nav-icon>
			<h1 class="title font-weight-bold mr-12 pr-12">
				Advanced Search
			</h1>

			<v-tabs
				v-model="tab"
				class="ml-12"
				style="width: auto;">
				<v-tab to="#filters" class="mx-4">
					Filters
				</v-tab>
				<v-tab to="#results" class="mx-4">
					Results
				</v-tab>
			</v-tabs>
			<v-spacer></v-spacer>

			<v-card-actions
				class="v-card__actions--wide">
				<lookup-actions
					v-if="tab === 'results'"
					@export:cases="exportCasesReport">
					<v-list-item
						v-if="resultsTab === 1"
						@click="exportCasesReport">
						Export results
					</v-list-item>
					<v-list-item
						v-if="resultsTab === 1"
						@click="exportCasesFolioTXT">
						Export as Folio TXT
					</v-list-item>
					<v-list-item
						v-if="resultsTab === 1"
						@click="exportCasesExtendedTXT">
						Export as Extended TXT
					</v-list-item>
					<v-list-item
						v-if="resultsTab === 1"
						@click="exportPetitionsReport">
						Excel Petitions Report
					</v-list-item>
					<v-list-item
						v-if="resultsTab === 1"
						@click="exportLookupResults">
						Export as CSV
					</v-list-item>
				</lookup-actions>
				<v-btn
					v-if="tab === 'filters'"
					color="secondary"
					outlined
					@click="search">
					Search
				</v-btn>
				<v-btn
					v-if="tab === 'filters'"
					color="primary"
					outlined
					@click="clearFilters">
					Clear Filters
				</v-btn>
				<v-btn
					v-if="tab === 'filters'"
					color="grey"
					outlined>
					Save Filters
				</v-btn>
			</v-card-actions>
		</v-toolbar>
		<v-divider></v-divider>

		<v-container>
			<v-tabs-items v-model="tab"
				class="transparent">
				<v-tab-item value="filters">
					<v-card
						outlined>
						<v-card-title>
							Selected Filters
						</v-card-title>
						<v-divider></v-divider>
						<v-container>
							<v-form ref="form"
								@submit.prevent="search">
								<v-row align="center">
									<template v-for="(item, key) in filters">
										<v-col v-if="item.selected"
											:key="key"
											cols="3"
											class="px-6">
											<v-row align="center">
												<v-col cols="4">
													{{ item.name }}
												</v-col>
												<v-col cols="2"
													v-if="item.prefix"
													class="px-0">
													<v-select
														v-model="item[item.prefix.model]"
														:items="item.prefix.items"
														dense
														outlined
														hide-details>
													</v-select>
												</v-col>
												<v-col :cols="item.prefix ? '5' : ''"
													class="pr-1">
													<v-checkbox
														v-if="item.field_type === 'boolean'"
														v-model="item.value"
														class="mt-0"
														dense
														outlined
														hide-details>
													</v-checkbox>

													<v-autonumeric
														v-else-if="item.field_type === 'numeric'"
														v-model.number="item.value"
														:suffix="item.suffix"
														dense
														outlined
														hide-details>
													</v-autonumeric>
													
													<a-date
														v-else-if="item.field_type === 'date'"
														v-model="item.value"
														dense
														outlined
														hide-details>
													</a-date>

													<v-select
														v-else-if="item.field_type === 'select'"
														v-model="item.value"
														:items="resolve(item.items, this)"
														:item-value="item.item_value"
														:item-text="item.item_text"
														dense
														outlined
														:multiple="item.multiple"
														hide-details>
													</v-select>

													<v-autocomplete
														v-else-if="item.field_type === 'autocomplete'"
														v-model="item.value"
														:items="resolve(item.items, this)"
														:item-value="item.item_value"
														:item-text="item.item_text"
														dense
														outlined
														:multiple="item.multiple"
														hide-details>
													</v-autocomplete>

													<v-mask-input
														v-else-if="item.field_type === 'phone_number'"
														v-model="item.value"
														:mask="'(999) 999-9999'"
														dense
														outlined
														hide-details>
													</v-mask-input>

													<v-text-field
														v-else
														v-model="item.value"
														:suffix="item.suffix"
														dense
														outlined
														hide-details>
													</v-text-field>
												</v-col>
												<v-col cols="1"
													class="pl-1">
													<v-btn
														icon
														small
														@click="item.selected = false">
														<v-icon small>mdi-close</v-icon>
													</v-btn>
												</v-col>
											</v-row>
										</v-col>
									</template>
								</v-row>
							</v-form>
						</v-container>
					</v-card>
					
					<v-row>
						<v-col cols="10">
							<v-card
								outlined>
								<v-card-title>
									Choose Filters:
								</v-card-title>
								<v-divider></v-divider>
								<v-container>
									<v-row>
										<v-col cols="2"
											v-for="(item, key) in filters"
											:key="key">
											<v-checkbox
												v-model="item.selected"
												:label="item.name"
												class="mt-0"
												hide-details>
												<template #label>
													{{ item.name }}
													<v-btn
														small
														text
														icon
														@click.stop="item.favorite = !item.favorite">
														<v-icon small
															:color="item.favorite ? 'amber' : ''">
															mdi-star-outline
														</v-icon>
													</v-btn>
												</template>
											</v-checkbox>
										</v-col>
									</v-row>
								</v-container>
							</v-card>
						</v-col>

						<v-col cols="2">
							<v-card
								outlined>
								<v-card-title>
									Searches:
								</v-card-title>
								<v-divider></v-divider>
							</v-card>
						</v-col>
					</v-row>
				</v-tab-item>

				<v-tab-item value="results">
					<v-tabs
						v-model="resultsTab"
						grow>
						<v-tab>
							Clients
						</v-tab>
						<v-tab>
							Cases
						</v-tab>
					</v-tabs>
					<v-divider></v-divider>

					<v-tabs-items
						v-model="resultsTab"
						class="transparent">
						<v-tab-item>
							<clients-table
								:clients="clients">
							</clients-table>
						</v-tab-item>

						<v-tab-item>
							<cases-table
								:cases="cases">
							</cases-table>
						</v-tab-item>
					</v-tabs-items>

				</v-tab-item>
			</v-tabs-items>
		</v-container>
	</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import { resolve } from '../utils'
import { saveAs } from 'file-saver'
import Blob from 'blob'

import ClientsTable from '../components/Lookup/ClientsTable'
import CasesTable from '../components/Lookup/CasesTable'
import LookupActions from '../components/Lookup/LookupActions'

const lookupApi = apiFactory.get('lookup')

const propertyTypes = [
	{
		text: 'Vacant',
		value: 'vacant',
	},
	{
		text: 'Condo',
		value: 'condo',
	},
	{
		text: 'Residential',
		value: 'residential',
	},
]

const workupStatuses = [
	{
		text: 'Completed',
		value: true,
	},
	{
		text: 'Not Completed',
		value: null,
	},
]

export default {
	components: {
		ClientsTable,
		CasesTable,
		LookupActions,
	},
	data: () => ({
		tab: 'filters',
		resultsTab: 1,
		propertyTypes,
		workupStatuses,
	}),
	computed: {
		...mapGetters('users', [
			'users',
		]),
		...mapGetters('lookup', [
			'clients',
			'cases',
		]),
		...mapGetters('counties', [
			'counties',
		]),
		...mapGetters('clientTypes', [
			'clientTypes',
		]),
		...mapGetters('tags', [
			'tags',
		]),
		...mapGetters('marketingCodes', [
			'marketingCodes',
		]),
		...mapGetters('applicationTypes', [
			'applicationTypes',
		]),
		...mapGetters('applicationSources', [
			'applicationSources',
		]),
		...mapGetters('paymentTypes', [
			'paymentTypes',
		]),
		...mapGetters('paymentStatuses', [
			'paymentStatuses',
		]),
		...mapGetters('years', [
			'years',
		]),
		filters: {
			get() {
				return this.$store.state.lookup.filters;
			},
			set(value) {
				this.$store.commit('filters/SET_FILTERS', value);
			},
		},
		selectedFilters() {
			return this.filters.filter(item => item.selected)
		},
		defaultFilters() {
			return this.filters.filter(item => item.default && !item.selected)
		},
		favoriteFilters() {
			return this.filters.filter(item => item.favorite)
		},
		isResult() {
			return this.clients.length > 0
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		...mapActions('sidebar', {
			toggleSidebar: 'toggle',
		}),
		...mapActions('lookup', [
			'lookup',
		]),
		...mapActions('loader', {
			setLoader: 'set',
		}),
		...mapActions('users', [
			'loadUsers',
		]),
		...mapActions('counties', [
			'loadCounties',
		]),
		...mapActions('clientTypes', [
			'loadClientTypes',
		]),
		...mapActions('tags', [
			'loadTags',
		]),
		...mapActions('marketingCodes', [
			'loadMarketingCodes',
		]),
		...mapActions('applicationTypes', [
			'loadApplicationTypes',
		]),
		...mapActions('applicationSources', [
			'loadApplicationSources',
		]),
		...mapActions('paymentTypes', [
			'loadPaymentTypes',
		]),
		...mapActions('paymentStatuses', [
			'loadPaymentStatuses',
		]),
		resolve,
		async search() {
			try {
				this.setLoader(true)
				const filters = [
					...this.defaultFilters,
					...this.selectedFilters,
				]
				await this.lookup({ filters })
				this.$router.push('#results')
			} finally {
				this.setLoader(false)
			}
		},
		clearFilters() {
			this.$refs.form.reset()
			this.filters.forEach(filter => filter.selected = false)
		},

		/**
		 * Export Cases report
		 */
		async exportCasesReport() {
			try {
				this.setLoader(true)
				const filters = [
					...this.defaultFilters,
					...this.selectedFilters,
				]
				const { data } = await lookupApi.casesReport({ filters })
				const blob = new Blob([ data ])
				saveAs(blob, 'report.csv')
			} catch (error) {
				this.notify({
					text: 'Can not load Case Report',
					color: 'error'
				}, { root: true })
			} finally {
				this.setLoader(false)
			}
		},

		/**
		 * Export Cases Folio TXT report
		 */
		async exportCasesFolioTXT() {
			try {
				this.setLoader(true)
				const filters = [
					...this.defaultFilters,
					...this.selectedFilters,
				]
				const { data } = await lookupApi.casesFolioTXT({ filters })
				const blob = new Blob([ data ])
				saveAs(blob, 'cases_list.txt')
			} catch (error) {
				this.notify({
					text: 'Can not load Folio TXT',
					color: 'error'
				}, { root: true })
			} finally {
				this.setLoader(false)
			}
		},

		/**
		 * Export Cases Extended TXT report
		 */
		async exportCasesExtendedTXT() {
			try {
				this.setLoader(true)
				const filters = [
					...this.defaultFilters,
					...this.selectedFilters,
				]
				const { data } = await lookupApi.casesExtendedTXT({ filters })
				const blob = new Blob([ data ])
				saveAs(blob, 'extended_cases_list.txt')
			} catch (error) {
				this.notify({
					text: 'Can not load Extended TXT',
					color: 'error'
				}, { root: true })
			} finally {
				this.setLoader(false)
			}
		},

		/**
		 * Export Petiton Reports Excel
		 */
		async exportPetitionsReport() {
			try {
				this.setLoader(true)
				const filters = [
					...this.defaultFilters,
					...this.selectedFilters,
				]
				const { data } = await lookupApi.petitionsReport({ filters })
				const blob = new Blob([ data ])
				saveAs(blob, 'petitions_report.xlsx')
			} catch (error) {
				this.notify({
					text: 'Can not load Petitions Report',
					color: 'error'
				}, { root: true })
			} finally {
				this.setLoader(false)
			}
		},

		/**
		 * Export Lookup Results CSV
		 */
		async exportLookupResults() {
			try {
				this.setLoader(true)
				const filters = [
					...this.defaultFilters,
					...this.selectedFilters,
				]
				const { data } = await lookupApi.exportLookupResults({ filters })
				const blob = new Blob([ data ])
				saveAs(blob, 'lookup_results.csv')
			} catch (error) {
				this.notify({
					text: 'Can not load Lookup Results',
					color: 'error'
				}, { root: true })
			} finally {
				this.setLoader(false)
			}
		},
	},
	mounted() {
		if(this.isResult) {
			this.$router.push('#results')
			this.search()
		}
		this.loadUsers()
		this.loadCounties()
		this.loadClientTypes()
		this.loadTags()
		this.loadMarketingCodes()
		this.loadApplicationTypes()
		this.loadApplicationSources()
		this.loadPaymentTypes()
		this.loadPaymentStatuses()
	},
}
</script>