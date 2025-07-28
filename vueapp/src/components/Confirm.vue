<template>
	<v-dialog
		v-model="dialog"
		:max-width="options.width"
		:style="{ zIndex: options.zIndex }"
		@keydown.esc="cancel">
		<v-form
			ref="form"
			v-model="valid">
			<v-card>
				<v-toolbar
					dark
					dense
					flat
					color="white">
					<v-toolbar-title
						:class="`${options.color}--text`">
						{{ title }}
					</v-toolbar-title>
				</v-toolbar>

				<v-card-text
					v-show="!!message">
					{{ message }}
					<v-text-field
						v-if="!!options.promptText"
						v-model="inputText"
						:rules="inputRules"
						outlined
						dense>
					</v-text-field>
					<slot></slot>
				</v-card-text>

				<v-card-actions class="pt-0">
					<v-spacer></v-spacer>
					<v-btn
						color="grey"
						text
						class="text-none"
						@click.native="cancel">Cancel</v-btn>
					<v-btn
						:color="options.color"
						text
						class="text-none"
						:disabled="!valid"
						@click.native="agree">Submit</v-btn>
				</v-card-actions>
			</v-card>
		</v-form>
	</v-dialog>
</template>

<script>
/**
 * Vuetify Confirm Dialog component
 *
 * Insert component where you want to use it:
 * <confirm ref="confirm"></confirm>
 *
 * Call it:
 * this.$refs.confirm.open('Delete', 'Are you sure?', { color: 'red' }).then((confirm) => {})
 * Or use await:
 * if (await this.$refs.confirm.open('Delete', 'Are you sure?', { color: 'red' })) {
 *   // yes
 * }
 * else {
 *   // cancel
 * }
 *
 * Alternatively you can place it in main App component and access it globally via this.$root.$confirm
 * <template>
 *   <v-app>
 *     ...
 *     <confirm ref="confirm"></confirm>
 *   </v-app>
 * </template>
 *
 * mounted() {
 *   this.$root.$confirm = this.$refs.confirm.open
 * }
 */
export default {

	data: () => ({
		dialog: false,
		resolve: null,
		reject: null,
		message: null,
		title: null,
		options: {
			color: "primary",
			width: 300,
			zIndex: 200,
			promptText: null,
		},
		valid: true,
		inputText: '',
	}),
	computed: {
		inputRules() {
			return [
				v => !!v || 'Please fill the field',
				v => (v === this.options.promptText) || 'Text should match',
			]
		},
	},
	methods: {
		open(title, message, options) {
			this.dialog = true;
			this.title = title;
			this.message = message;
			this.options = Object.assign(this.options, options);
			return new Promise((resolve, reject) => {
				this.resolve = resolve;
				this.reject = reject;
			});
		},
		agree() {
			this.resolve(true);
			this.dialog = false;
		},
		cancel() {
			this.resolve(false);
			this.dialog = false;
		}
	},
};
</script>