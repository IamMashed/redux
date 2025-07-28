<template>
	<ul>
		<li v-for="(error, key) in errors"
			:key="key">
			{{ error }}
		</li>
	</ul>
</template>

<script>
export default {
	props: {
		errors: {
			type: Array,
			required: true,
		},
	},
}
</script>