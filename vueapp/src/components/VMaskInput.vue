<script>
import { VTextField } from 'vuetify/lib'
import Inputmask from 'inputmask'

export default {
	extends: VTextField,
	name: 'v-mask-input',
	props: {
		mask: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			im: null,
		}
	},
	mounted() {
		// Create the Inputmask instance on the VTextField input element
		this.im = new Inputmask({
			mask: this.mask,
			autoUnmask: true,
		}).mask(this.$refs.input)
		this.im = this.$refs.input.inputmask
		this.setIMValue(this.value)
	},
	methods: {
		onInput() {
			// emit v-model
			this.updateVModel()
		},
		updateVModel() {
			if (this.im !== null) {
				// emit raw value
				this.$emit('input', this.im.unmaskedvalue().replace(/\D+/gi, ''))
			}
		},
		genInput() {
			const listeners = Object.assign({}, this.listeners$)
			delete listeners['change']
			let element = this.$createElement('input', {
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
					paste: this.onPaste,
				},
				ref: 'input',
			})
			return element
		},
		onPaste (e) {
			const value = e.clipboardData.getData('Text')
			const alias = this.mask
			var unformattedValue = Inputmask.unmask(value, { alias, })
			this.$emit('input', unformattedValue)
		},
		setIMValue(value) {
			if(value) {
				this.im.setValue(value)
			} else {
				this.im.setValue('')
			}
		},
	},
	watch: {
		value(newVal) {
			this.setIMValue(newVal)
		},
	},
}
</script>