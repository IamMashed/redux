<template>
	<v-overlay :value="show"
		absolute>
		<v-progress-circular
			:size="70"
			:width="7"
			color="primary"
			indeterminate>
		</v-progress-circular>
	</v-overlay>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
	computed: {
		...mapGetters('loader', [
			'show',
		]),
	},
}
</script>

<style>

</style>