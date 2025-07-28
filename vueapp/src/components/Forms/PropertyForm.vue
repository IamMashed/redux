<template>
	<v-container>
		<v-row>
			<v-col cols="4"
				class="py-2">
				<v-text-field
					v-model="item.section"
					label="Sec"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="4"
				class="py-2">
				<v-text-field
					v-model="item.block"
					label="Block"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="4"
				class="py-2">
				<v-text-field
					v-model="item.lot"
					label="Lot"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="12"
				class="py-2">
				<v-text-field
					v-model="item.address"
					label="Address"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="12"
				class="py-2">
				<v-text-field
					v-model="item.school_district"
					label="School Dist"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="12"
				class="py-2">
				<v-text-field
					v-model="item.property_class"
					label="Class"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="12"
				class="py-2">
				<v-text-field
					v-model="item.age"
					label="Age"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col
				cols="6"
				class="py-2">
				<v-text-field
					v-model="item.last_sale_price"
					label="Sale Price"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col
				cols="6"
				class="py-2">
				<v-text-field
					v-model="item.last_sale_date"
					label="Sale Date"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="12"
				class="py-2">
				<h4 class="primary--text">Adjustments</h4>
			</v-col>
			<v-col cols="6"
				class="py-2">
				<v-select
					v-model="item.property_style"
					:items="transConstants.property_style_map"
					label="Style"
					item-value="key"
					item-text="value"
					dense
					hide-details>
				</v-select>
			</v-col>
			<v-col
				v-for="(field, key) in propField"
				:key="key"
				cols="6"
				class="py-2">

				<v-select
					v-if="constants[`${field.key.toLowerCase()}_type_map`]"
					v-model="item[field.value]"
					:items="transConstants[`${field.key.toLowerCase()}_type_map`]"
					:label="field.key"
					item-value="key"
					item-text="value"
					dense
					hide-details>
				</v-select>

				<v-text-field
					v-else
					v-model="item[field.value]"
					:label="field.key"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="6"
				class="py-2">
				<v-select
					v-model="item.location"
					:items="transObsolescences"
					label="Location"
					item-value="code"
					item-text="rule_name"
					dense
					hide-details>
				</v-select>
			</v-col>
		</v-row>
		<v-row>
			<v-col cols="6"
				class="py-2">
				<v-text-field
					v-model="item.other_adjustment_description"
					label="Other Adjustment Description"
					dense
					hide-details>
				</v-text-field>
			</v-col>
			<v-col cols="6"
				class="py-2">
				<v-text-field
					v-model="item.other_adjustment"
					label="Other Adjustment"
					dense
					hide-details>
				</v-text-field>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
	props: {
		item: {
			type: Object,
			required: true,
		},
		fields: {
			type: Array,
			default: () => ([]),
		},
	},
	computed: {
		...mapGetters('constants', [
			'constants',
			'transConstants'
		]),
		...mapGetters('adjustments', [
			'adjustments',
		]),
		...mapGetters('obsolescences', [
			'transObsolescences',
		]),
		propField() {
			return this.adjustments.map(item => {
				return this.fields.indexOf(item.key) >= 0
				? {
					key: item.key,
					value: item.property_field,
				}
				: false
			}).filter(item => !!item.value)
		},
	},
}
</script>