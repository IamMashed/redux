<template>
	<v-dialog
		v-model="dialog"
		max-width="500px"
		@keydown.esc="cancel">
		<v-card
			outlined>
			<v-card-title>
				Select PDF filename
			</v-card-title>
			<v-divider></v-divider>

			<v-container>
				<v-select
					:value="value"
					:items="items"
					label="PDF filename"
					outlined
					dense
					@input="updateValue">
				</v-select>
			</v-container>

			<v-card-actions class="pt-0">
				<v-spacer></v-spacer>
				<v-btn
					color="error"
					outlined
					@click.native="cancel">
					Cancel
				</v-btn>
				<v-btn
					color="primary"
					outlined
					@click.native="submit">
					Submit
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
export default {
	props: {
		value: {
			type: String,
			required: true,
		},
	},
	data: () => ({
		dialog: false,
		resolve: null,
		reject: null,
		items: [
			'address',
			'apn',
		],
	}),
	methods: {
		updateValue(e) {
			this.$emit('input', e)
		},
		open() {
			this.dialog = true
			return new Promise((resolve, reject) => {
				this.resolve = resolve
				this.reject = reject
			})
		},
		submit() {
			this.resolve(true)
			this.dialog = false
		},
		cancel() {
			this.resolve(false)
			this.dialog = false
		},
	},
}
</script>
