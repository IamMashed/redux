<template>
	<v-alert
		text
		dense
		outlined
		type="warning"
		class="ma-0">
		This email address is used by 
		<router-link
			:to="{
				name: 'client',
				params: {
					id: this.clientid,
				},
			}">
			the existing Client
		</router-link>
	</v-alert>
</template>

<script>
export default {
	props: {
		clientid: {
			type: Number,
			required: true,
		},
	},
}
</script>