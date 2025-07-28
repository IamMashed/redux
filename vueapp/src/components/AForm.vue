<template>
	<v-card>
		<v-form ref="form">

			<v-card-title>
				Edit
			</v-card-title>

			<v-card-text style="max-height: 70vh; overflow: scroll;">
				<v-container grid-list-md px-0>
					<slot></slot>
				</v-container>
			</v-card-text>

			<v-card-actions>
				<slot
					name="actions"
					:cancel="cancel"
					:submit="submit">
					<v-spacer></v-spacer>

					<v-btn
						text
						color="grey"
						class="text-none"
						@click="cancel">
						Cancel
					</v-btn>

					<v-btn
						text
						class="text-none v-btn--filled"
						color="success"
						@click="submit">
						Submit
					</v-btn>
				</slot>
			</v-card-actions>

		</v-form>
		<v-overlay
            v-if="loading"
            absolute
			class="text-center">
            <v-progress-circular indeterminate size="64"></v-progress-circular>
			<div>Loading</div>
        </v-overlay>
	</v-card>
</template>

<script>
export default {
	props: {
		loading: {
			type: Boolean,
			default: false,
		},
	},
	methods: {
		cancel() {
			this.$emit('cancel')
		},
		submit() {
			// const result = await this.$validator.validate()
			// if(result) {
			// 	this.$emit('submit')
			// }
			this.$emit('submit')
		},
		reset() {
			this.$refs.form.reset()
		},
	},
}
</script>