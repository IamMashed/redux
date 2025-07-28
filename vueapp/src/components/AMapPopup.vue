<template>
	<div>
		<p>{{ property.address }}</p>
		<p>ADJ Market: {{ property.adjusted_market_value | currency }}</p>
		<v-switch
			v-model="property.selected"
			label="Selected"
			dense
			@change="emitChange">
		</v-switch>
		<v-btn
			color="secondary"
			small
			@click="emitShow">Show</v-btn>
	</div>
</template>

<script>
export default {
	props: {
		feature: {
			type: Object,
			required: true,
		},
	},
	computed: {
		property() {
			return this.feature.properties || {}
		},
	},
	methods: {
		emitChange(e) {
			return this.$emit('selection', this.property?.id, e)
		},
		emitShow() {
			return this.$emit('show', this.property?.id)
		},
	},
}
</script>