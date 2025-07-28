<template>
	<v-snackbar
		v-model="show"
		:color="color"
		:timeout="timeout">
		{{ text }}
		<template v-slot:action="{ attrs }">
			<v-btn
				dark
				text
				icon
				v-bind="attrs"
				@click="show = false">
				<v-icon>mdi-close</v-icon>
			</v-btn>
		</template>
	</v-snackbar>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
	data: () => ({
		timeout: 10000,
	}),
	computed: {
		...mapGetters('notification', [
			'text',
			'color'
		]),
		show: {
			get() {
				return this.$store.state.notification.show;
			},
			set(value) {
				this.$store.commit('notification/SET_SHOW', value);
			},
		},
	},
}
</script>