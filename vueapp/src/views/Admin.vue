<template>
	<v-container>
		<h1>Admin</h1>
		<users></users>
	</v-container>
</template>

<script>
import Users from '../components/Users/Users'

export default {
	components: {
		Users,
	},
}
</script>