<template>
	<v-dialog
		v-model="dialog"
		max-width="1235">
		<v-card
			outlined>
			<v-card-title>
				<slot name="title">Settings</slot>
				<v-spacer></v-spacer>
				<v-btn
					icon
					color="black"
					@click="dialog = false">
					<v-icon>mdi-close</v-icon>
				</v-btn>
			</v-card-title>
			<v-divider></v-divider>

			<v-container
				class="px-5">
				<v-row>
					<v-col
						cols="12"
						sm="6"
						md="4"
						class="pt-0">
						<h2>General</h2>
						<v-row>
							<v-col
								cols="4">
								Rule Set
							</v-col>
							<v-col
								cols="8">
								<router-link
									v-if="ruleSet.id"
									:to="{
										name: 'rule-set',
										params: {
											id: ruleSet.id,
										}
									}">
									<b>{{ ruleSet.rule_name }}</b>
								</router-link>
							</v-col>
						</v-row>

						<v-row>
							<v-col
								cols="4">
								Ratio
							</v-col>
							<v-col
								cols="8">
								{{ assessmentRatio }} ({{ assessmentDate.tax_year }})
							</v-col>
						</v-row>

						<v-row>
							<v-col
								cols="4">
								Assessment
							</v-col>
							<v-col
								cols="8">
								<v-select
									:value="assessmentDateId"
									:items="assessmentDates"
									item-text="assessment_name"
									item-value="id"
									outlined
									dense
									hide-details
									@input="(v) => $emit('update:assessment-date-id', v)">
								</v-select>
							</v-col>
						</v-row>

						<v-row>
							<v-col>
								ALL Adjustments
							</v-col>
						</v-row>

						<v-select
							v-model="ruleSet.adjustments_all"
							:items="adjustments"
							multiple
							chips
							item-text="key"
							item-value="key"
							dense>
						</v-select>

						<v-select
							v-model="ruleSet.adjustments_required"
							:items="adjustments"
							multiple
							chips
							label="Required for Mass CMA Adjustments"
							item-text="key"
							item-value="key"
							dense>
						</v-select>

						<v-autonumeric
							v-model.number="ruleSet.cost_of_sale"
							suffix="%"
							label="Cost of Sale">
						</v-autonumeric>
					</v-col>

					<template
						v-if="ruleSet.selection_rules">
						<v-col
							v-for="(col, key) in selectionRulesFields"
							:key="key"
							cols="12"
							sm="6"
							md="4">
							<template
								v-for="(field, key) in col"
								class="align-center">
								<v-checkbox
									v-if="field.type === 'boolean'"
									v-model="ruleSet.selection_rules[field.model]"
									:label="field.label"
									:key="key"
									dense>
								</v-checkbox>

								<v-autonumeric
									v-else-if="field.type === 'numeric'"
									v-model.number="ruleSet.selection_rules[field.model]"
									:suffix="field.suffix"
									:label="field.label"
									:key="key"
									dense>
								</v-autonumeric>

								<a-date
									v-else-if="field.type === 'date'"
									v-model="ruleSet.selection_rules[field.model]"
									:label="field.label"
									:key="key"
									dense>
								</a-date>

								<v-text-field
									v-else
									v-model.number="ruleSet.selection_rules[field.model]"
									:suffix="field.suffix"
									:label="field.label"
									:key="key"
									dense>
								</v-text-field>
							</template>
						</v-col>
					</template>
				</v-row>

				<v-row>
					<v-col
						cols="12"
						sm="6"
						md="4"
						class="pt-0">
						<v-checkbox
							v-if="settings.settings"
							v-model="settings.settings.show_formatted_rule_value"
							label="Show formatted rule value in Printed CMA Report"
							@change="updateSettings">>
						</v-checkbox>
					</v-col>
				</v-row>
			</v-container>
		</v-card>
	</v-dialog>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
	props: {
		ruleSet: {
			type: Object,
			required: true,
		},
		assessmentDateId: {
			type: Number,
		},
		assessmentDates: {
			type: Array,
			required: true,
		},
		assessmentRatio: {
			type: Number,
		},
		settings: {
			type: Object,
		},
	},
	data: () => ({
		dialog: false,
		selectionRule: {},
		selectionRulesFields: [
			[
				{
					label: 'Proximity range',
					type: 'numeric',
					model: 'proximity_range',
					suffix: 'Miles',
				},
				{
					label: 'Sale date from',
					type: 'date',
					model: 'sale_date_from',
				},
				{
					label: 'Sale date to',
					type: 'date',
					model: 'sale_date_to',
				},
				{
					label: 'Percent GLA Lower',
					model: 'percent_gla_lower',
					suffix: '%',
				},
				{
					label: 'Percent GLA Higher',
					model: 'percent_gla_higher',
					suffix: '%',
				},
				{
					label: 'Percent Sale Lower',
					model: 'percent_sale_lower',
					suffix: '%',
				},
				{
					label: 'Percent Sale Higher',
					model: 'percent_sale_higher',
					suffix: '%',
				},
				{
					label: 'Percent Lot Size Lower',
					model: 'percent_lot_size_lower',
					suffix: '%',
				},
				{
					label: 'Percent Lot Size Higher',
					model: 'percent_lot_size_higher',
					suffix: '%',
				},
			], [
				{
					label: 'Same property class',
					type: 'boolean',
					model: 'same_property_class',
				},
				{
					label: 'Same Family Types',
					type: 'boolean',
					model: 'same_one_family_types',
				},
				{
					label: 'Same school district',
					type: 'boolean',
					model: 'same_school_district',
				},
				{
					label: 'Same town',
					type: 'boolean',
					model: 'same_town'
				},
				{
					label: 'Same street',
					type: 'boolean',
					model: 'same_street',
				},
				{
					label: 'Same property style',
					type: 'boolean',
					model: 'same_property_style',
				},
				{
					label: 'Same building',
					type: 'boolean',
					model: 'same_building',
				},
				{
					label: 'Prioritize same water categories',
					type: 'boolean',
					model: 'prioritize_same_water_categories',
				},
			],
		],
	}),
	computed: {
		...mapGetters('adjustments', [
			'adjustments',
		]), 
		assessmentDate() {
			return this.assessmentDates.find(d => d.id === this.assessmentDateId) || {}
		},
	},
	methods: {
		...mapActions('adjustments', [
			'loadAdjustments',
		]),
		show() {
			this.dialog = true
		},
		updateSettings() {
			return this.$emit('update:settings', this.settings)
		},
	},
	watch: {
		dialog(newVal) {
			if(!newVal) {
				this.$emit('close')
			}
		},
	},
	mounted() {
		this.loadAdjustments()
	},
}
</script>