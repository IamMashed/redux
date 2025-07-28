<template>
	<v-menu
		offset-y>

		<template #activator="{ on, attrs }">
			<v-btn
				color="primary"
				class="mr-10"
				outlined
				v-bind="attrs"
				v-on="on">
				Actions
			</v-btn>
		</template>

		<v-list>
			<v-list-item
				v-if="isCaseShown">
				<v-btn
					color="primary"
					outlined
					:href="`${VUE_APP_API}case-properties/${caseId}/dr486`"
					target="_blank">
					Download DR486
				</v-btn>
			</v-list-item>

			<v-list-item
				v-if="isCaseShown">
				<v-btn
					color="primary"
					outlined
					:href="`${VUE_APP_API}case-properties/${caseId}/evidence-package`"
					target="_blank">
					Evidence Package
				</v-btn>
			</v-list-item>
			
			<v-list-item>
				<v-btn
					color="error"
					outlined
					@click="$emit('delete:client')">
					Permanently Delete Client
				</v-btn>
			</v-list-item>

			<v-list-item
				v-if="isCaseShown">
				<v-btn
					color="error"
					outlined
					@click="$emit('delete:case')">
					Permanently Delete Case
				</v-btn>
			</v-list-item>
      </v-list>

	</v-menu>
</template>

<script>
export default {
	data: () => ({
		VUE_APP_API: process.env.VUE_APP_API,
	}),
	computed: {
		isCaseShown() {
			return this.$route.name === 'client-case'
		},
		caseId() {
			return this.$route.params.caseid
		},
	},
}
</script>