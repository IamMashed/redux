<template>
	<v-dialog
		v-model="innerValue"
		max-width="1125">
		<v-card outlined>
			<v-card-title>
				<v-btn
					class="mr-2"
					icon
					small
					@click="innerValue = false">
					<v-icon>mdi-chevron-left</v-icon>
				</v-btn>
				Timeline
			</v-card-title>
			<v-divider></v-divider>
			<v-container>
				<v-stepper v-model="step"
					class="elevation-0 transparent v-stepper--great"
					alt-labels>
					<v-stepper-header>
						<template v-for="item in steps">
							<v-stepper-step
								:complete="step >= item"
								:color="step >= item ? 'success' : ''"
								:key="item"
								:step="item"
								:complete-icon="item"
								class="v-stepper__step--outlined">
								<v-row
									class="flex-nowrap"
									no-gutters
									style="margin-left: -2em;">
									<v-col cols="4">
										<svg xmlns="http://www.w3.org/2000/svg" width="61" height="126" viewBox="0 0 61 383"
											style="margin-top: -2em;">
											<polyline fill="none" stroke="#49484D" stroke-linecap="round" stroke-width="6" points="45.494 3 3 44.893 3 379.288 57.704 379.288"/>
										</svg>
									</v-col>

									<v-col cols="9"
										class="pt-5">
										<p>Received and Validated Application</p>
										<p class="mb-2 font-weight-bold">DATE</p>
										<p class="font-weight-bold">March 12, 2020</p>
									</v-col>
								</v-row>
							</v-stepper-step>
							<v-divider v-if="item !== steps"
								:key="`${item}-d`">
							</v-divider>
						</template>
					</v-stepper-header>
				</v-stepper>
			</v-container>
		</v-card>
	</v-dialog>
</template>

<script>
export default {
	props: {
		value: {
			type: Boolean,
			default: false,
		},
		step: {
			type: Number,
			default: 1,
		},
	},
	data: () => ({
		steps: 6,
	}),
	computed: {
		innerValue: {
			get() {
				return this.value
			},
			set(val) {
				this.$emit('input', val)
			},
		},
	},
}
</script>