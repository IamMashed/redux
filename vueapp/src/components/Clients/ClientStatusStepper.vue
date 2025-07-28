<template>
	<v-stepper v-model="step"
		class="elevation-0 transparent"
		alt-labels>
		<v-stepper-header>
			<template v-for="item in steps">
				<v-stepper-step
					:complete="step >= item"
					:color="step >= item ? 'success' : ''"
					:key="item"
					:step="item"
					:complete-icon="`${item}`"
					class="v-stepper__step--outlined">
				</v-stepper-step>
				<v-divider v-if="item !== steps"
					:key="`${item}-d`">
				</v-divider>
			</template>
		</v-stepper-header>
	</v-stepper>
</template>

<script>
export default {
	props: {
		step: {
			type: Number,
			default: 1,
		},
	},
	data: () => ({
		steps: 6,
	}),
}
</script>