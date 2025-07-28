<template>
	<div>
		<p>{{ properties.obs_name }}</p>
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
		properties() {
			return this.feature.properties || {}
		},
	},
}
</script>