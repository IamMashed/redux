<template>
	<v-alert
		dense
		outlined
		:type="notification.status"
		class="ma-0">
		{{ notification.message }}
	</v-alert>
</template>

<script>
export default {
	props: {
		notification: {
			type: Object,
			required: true,
		},
	},
}
</script>