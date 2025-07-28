<template>
	<v-container>

		<h1 class="primary--text">Single CMA Search</h1>

		<v-card>
			<v-card-title>Subject Information</v-card-title>
			<v-card-text>
				<v-form
					ref="form"
					id="cma-search-form"
					v-model="valid"
					@submit.prevent="searchProperties">
					<v-row>
						<v-col cols="4">
							<v-select
								v-model="county"
								:items="counties"
								label="County"
								:disabled="!counties[0]"
								:rules="[v => !!v || 'County is required']"
								item-value="id"
								item-text="name"
								hide-details
								outlined
								required>
							</v-select>
						</v-col>
						<v-col cols="4">
							<v-select
								v-model="assessmentDateId"
								label="Assessment"
								:items="countyAssessmentDates"
								item-text="assessment_name"
								item-value="id"
								:disabled="!county"
								outlined
								hide-details>
							</v-select>
						</v-col>
					</v-row>

					<v-row>
						<v-col cols="3">
							<v-text-field
								v-model="params.district"
								label="District"
								:disabled="!county"
								hide-details
								outlined>
							</v-text-field>
						</v-col>
						<v-col cols="3">
							<v-text-field
								v-model="params.section"
								label="Section"
								:disabled="!county"
								hide-details
								outlined>
							</v-text-field>
						</v-col>
						<v-col cols="3">
							<v-text-field
								v-model="params.block"
								label="Block"
								:disabled="!county"
								hide-details
								outlined>
							</v-text-field>
						</v-col>
						<v-col cols="3">
							<v-text-field
								v-model="params.lot"
								label="Lot"
								:disabled="!county"
								hide-details
								outlined>
							</v-text-field>
						</v-col>
					</v-row>

					<v-row>
						<v-col cols="4">
							<v-text-field
								v-model="params.address"
								label="Address"
								:disabled="!county"
								hide-details
								outlined>
							</v-text-field>
						</v-col>
						<v-col cols="4">
							<v-text-field
								v-model="params.unit"
								label="Unit"
								:disabled="!county"
								hide-details
								outlined>
							</v-text-field>
						</v-col>
					</v-row>

					<v-row>
						<v-col cols="4">
							<v-text-field
								v-model="params.apn"
								label="ParID (APN)"
								:disabled="!county"
								hide-details
								outlined>
							</v-text-field>
						</v-col>
					</v-row>

					<v-card-actions>
						<v-btn
							type="submit"
							color="secondary"
							depressed
							:disabled="!valid">
							Search
						</v-btn>
						<v-btn
							@click="clearForm">
							Clear
						</v-btn>
					</v-card-actions>
				</v-form>
			</v-card-text>

			<v-overlay
				absolute
				:value="loading">
				<v-progress-circular
					:size="70"
					:width="7"
					color="primary"
					indeterminate>
				</v-progress-circular>
			</v-overlay>
		</v-card>
		<h2 class="primary--text mt-10">Results:</h2>
		<v-row v-if="loading">
			<v-col
				v-for="i in 6"
				:key="i"
				cols="6"
				md="4">
				<v-skeleton-loader
					type="card-heading, list-item-three-line, list-item-three-line, actions"
					elevation="2">
				</v-skeleton-loader>
			</v-col>
		</v-row>
		<v-row v-else>
			<v-col
				v-for="property in properties"
				:key="property.id"
				cols="6"
				md="4">
				<v-card>
					<v-card-title>
						{{ property.address }}
					</v-card-title>
					<v-card-text>
						<v-row>
							<v-col>
								<ul>
									<li>County: {{ countyFilter(property.county) }}</li>
									<li>Town: {{ property.town }}</li>
									<li>Village: {{ property.village }}</li>
									<li>APN: {{ property.apn }}</li>
									<li>Owner: {{ property.owners | lastOwners }}</li>
									<li>Age: {{ property.age }}</li>
									<li>Acres: {{ property.lot_size }}</li>
									<li>GLA: {{ property.gla_sqft | bignum }}</li>
									<li>Class: {{ property.property_class | classFilter(property.county) }}</li>
								</ul>
							</v-col>
							<v-col>
								<v-img
									:src="findByKey(property.photos, (item) => item.is_best === true).url || require('@/assets/images/no_photo.png')"
									lazy-src="@/assets/images/no_photo.png"
									height="130"
									max-width="200">
								</v-img>
							</v-col>
						</v-row>
					</v-card-text>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn
							:to="{
								name: 'cma-compare',
								params: {
									id: property.id,
								},
								query: {
									'assessment-date': assessmentDateId,
								},
							}"
							class="secondary"
							depressed>
							Next
						</v-btn>
					</v-card-actions>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import { removeEmpty, findByKey } from '../utils'
import countyFilter from '../mixins/countyFilter'

const assessmentDatesApi = apiFactory.get('assessment-dates')
const propertiesApi = apiFactory.get('properties')

export default {
	mixins: [
		countyFilter,
	],
	data: () => ({
		assessmentDates: [],
		assessmentDateId: null,
		params: {
			district: '',
			section: '',
			block: '',
			lot: '',
			address: '',
			apn: '',
		},
		properties: [],
		loading: false,
		valid: true,
	}),
	computed: {
		...mapGetters('counties', [
			'counties',
		]),
		county: {
			get() {
				return this.$store.state.cma.county
			},
			set(value) {
				this.$store.commit('cma/SET_COUNTY', value)
			},
		},
		countyAssessmentDates() {
			return this.assessmentDates.filter(item => item.county === this.county)
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		...mapActions('counties', [
			'loadCounties',
		]),
		findByKey,
		async loadAssessmentDates() {
			try {
				const { data } = await assessmentDatesApi.getAll()
				this.assessmentDates = data
			} catch (error) {
				this.notify({
					text: 'Can not load Assessment Dates',
					color: 'error',
				}, { root: true })
			}
		},
		setDefaultAssessmentDate() {
			const assessmentDates = this.countyAssessmentDates
			const latestAssessmentDate = assessmentDates[assessmentDates.length - 1]
			this.assessmentDateId = latestAssessmentDate.id || null
		},
		async loadProperties(params) {
			try {
				this.loading = true
				const { data } = await propertiesApi.getAll(params)
				this.properties = data
				this.loading = false
			} catch (error) {
				this.notify({
					text: 'Can not load properties',
					color: 'error',
				}, { root: true })
			}
		},
		searchProperties() {
			return this.loadProperties(removeEmpty({
				...this.params,
				county: this.county,
			}))
		},
		clearForm() {
			this.$refs.form.reset()
		},
	},
	mounted() {
		this.loadCounties()
		this.loadAssessmentDates()
	},
	watch: {
		county: 'setDefaultAssessmentDate',
	},
}
</script>

<style scoped>
#cma-search-form >>> .v-label {
	font-size: 16px;
}

#cma-search-form >>> .v-label:not(.v-label--active) {
	transform: unset !important;
}
</style>