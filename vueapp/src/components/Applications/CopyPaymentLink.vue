<template>
	<v-btn
		color="primary"
		outlined
		small
		@click.prevent.stop="copyPaymentLink">
		Copy Payment Link
	</v-btn>
</template>

<script>
import { mapActions } from 'vuex'

export default {
	props: {
		applicationId: {
			type: Number,
			required: true,
		},
	},
	data: () => ({
		SHOPIFY_URL: 'https://redux-web.myshopify.com/cart/31763617906752:1?attributes[application_id]=',
	}),
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		async copyPaymentLink() {
			const url = `${this.SHOPIFY_URL}${this.applicationId}`

			// Create dummy input and copy text to clipboard
			var dummy = document.createElement('textarea')
			document.body.appendChild(dummy)
			dummy.value = url
			dummy.select()
			document.execCommand('copy')
			document.body.removeChild(dummy)

			this.notify({
				text: 'Payment Link Copied',
				color: 'black'
			}, { root: true })
		},
	},
}
</script>