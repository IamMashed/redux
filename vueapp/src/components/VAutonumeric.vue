<script>
import { VTextField } from 'vuetify/lib'
import AutoNumeric from 'autonumeric'

export default {
	extends: VTextField,
	props: {
		anOptions: {
			// autonumeric options (see doc)
			type: Object,
			required: false,
			default() {
				return {}
			},
		},
	},
	data() {
		return {
			anElement: null, // autonumeric instance
			changedByInput: false, // Flag to know if the value is changed by user input
		}
	},
	mounted() {
		this.createAnElement()
	},
	methods: {
		createAnElement() {
			// Create the AutoNumeric instance on the VTextField input element
			this.anElement = new AutoNumeric(this.$refs.input, this.anOptions)
			// Set the AutoNumeric  default value
			this.anElement.set(this.value)
		},
		onInput() {
			// User has changed the input
			this.changedByInput = true // set the flag to true
			this.updateVModel() // emit v-model
		},
		updateVModel() {
			// emit raw value
			if (this.anElement !== null) {
				this.$emit("input", this.anElement.getNumber())
			}
		},
		genInput() {
			const listeners = Object.assign({}, this.listeners$)
			delete listeners["change"]
			let element = this.$createElement("input", {
				style: {},
				attrs: {
					...this.attrs$,
					autofocus: this.autofocus,
					disabled: this.disabled,
					id: this.computedId,
					placeholder: this.placeholder,
					readonly: this.readonly,
					type: this.type
				},
				on: {
					blur: this.onBlur,
					input: this.onInput,
					focus: this.onFocus,
					keydown: this.onKeyDown,
					"autoNumeric:formatted": () => {
						this.changedByInput = false // Remove the flag when autonumeric finish formatting
					}
				},
				ref: "input"
			})
			return element
		},
	},
	watch: {
		value() {
			// Check if the last v-model update is fired by the input
			if (!this.changedByInput) {
				this.anElement.set(this.value) // Set the AutoNumeric raw value
			}
		},

		/**
		 * Watch options and reinit autonumeric on change
		 */
		'anOptions': {
			handler: function() {
				this.anElement.remove()
				this.createAnElement()
			},
		},
	},
}
</script>