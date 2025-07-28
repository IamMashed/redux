<template>
	<v-menu
		ref="dateMenu"
		v-model="dateMenu"
		:close-on-content-click="false"
		transition="scale-transition"
		offset-y
		min-width="290px">
		<template
			v-slot:activator="{ on }">
			<v-text-field
				v-on="on"
				v-bind="$attrs"
				:value="formattedDate"
				:label="label"
				:disabled="disabled"
				:class="classes"
				:style="styles"
				prepend-icon="mdi-calendar"
				@input="handleManualInput">
			</v-text-field>
		</template>
		<v-date-picker
			ref="datePicker"
			:value="value"
			:type="type"
			:min="min"
			:max="max"
			@input="handleInput"
			scrollable>
		</v-date-picker>
	</v-menu>
</template>

<script>
import { format, parse, parseISO, isValid } from 'date-fns'

export default {
	props: {
		value: {
			type: String,
		},
		label: {
			type: String,
		},
		type: {
			type: String,
		},
		min: {
			type: String,
		},
		max: {
			type: String,
		},
		disabled: {
			type: Boolean,
		},
		classes: {
			type: String,
		},
		styles: {
			type: String,
		},
	},
	data: () => ({
		dateMenu: false,
	}),
	computed: {
		formattedDate() {
			if(this.value) {
				return format(parseISO(this.value), 'MM/dd/yyyy')
			}
			return this.value
		},
	},
	methods: {
		handleManualInput(value) {
			const date = parse(value, 'MM/dd/yyyy', new Date())
			const formattedDate = format(date, 'yyyy-MM-dd')
			if(value && isValid(date) && value.length === 10) {
				this.$emit('input', formattedDate ? formattedDate : '')
			}
		},
		handleInput(value) {
			this.$emit('input', value)
		},
	},
}
</script>