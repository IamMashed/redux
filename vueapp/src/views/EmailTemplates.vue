<template>
	<div>
		<v-toolbar
			dense
			elevation="0">
			<v-app-bar-nav-icon
				@click="toggleSidebar">
			</v-app-bar-nav-icon>
			<h1 class="title font-weight-bold mr-12 pr-12">
				Email Templates Editor (Demo)
			</h1>
		</v-toolbar>
		<v-divider></v-divider>

		<v-container>
			<v-form
				ref="form"
				lazy-validation
				@submit.prevent="sendEmail">
				<v-row class="mt-2">
					<v-col cols="6" class="d-flex">
						<v-text-field
							v-model="email"
							label="Email Address"
							:rules="[v => !!v || 'Email is required']"
							dense>
						</v-text-field>

						<v-btn
							type="submit"
							color="primary"
							class="ml-2"
							:loading="loading"
							depressed>
							Send Email
						</v-btn>

						<v-btn
							type="submit"
							color="secondary"
							class="ml-4"
							depressed
							@click="saveDesign">
							Save Design
						</v-btn>
					</v-col>
				</v-row>
			</v-form>

			<EmailEditor
				ref="emailEditor"
				min-height="500px"
				@load="editorLoaded">
			</EmailEditor>
		</v-container>
	</div>
</template>

<script>
import { mapActions } from 'vuex'
import emailApi from '../api/emailApi'

import { EmailEditor } from 'vue-email-editor'

import template from '../assets/templates/email/template-1.json'

export default {
	components: {
		EmailEditor,
	},
	data: () => ({
		email: '',
		loading: false,
	}),
	methods: {
		...mapActions('sidebar', {
			toggleSidebar: 'toggle',
		}),
		...mapActions('notification', [
			'notify',
		]),
		editorLoaded() {
			// Pass the template JSON here
			this.$refs.emailEditor.editor.loadDesign(template);
		},
		saveDesign() {
			this.$refs.emailEditor.editor.saveDesign((design) => {
				console.log('saveDesign', design)

				const a = document.createElement('a')
				const file = new Blob([JSON.stringify(design)], {type: 'text/plain'})
				a.href = URL.createObjectURL(file)
				a.download = 'json.txt'
				a.click()
			})
		},
		exportHtml() {
			this.$refs.emailEditor.editor.exportHtml((data) => {
				console.log('exportHtml', data);
			});
		},
		async sendEmail() {
			try {
				const valid = this.$refs.form.validate()
				if (valid) {
					this.$refs.emailEditor.editor.exportHtml(async (data) => {
						this.loading = true
						
						await emailApi.sendEmail({
							title: 'Test email',
							body: data.html,
							receiver: this.email,
						})

						this.notify({
							text: 'Email sent',
							color: 'success'
						}, { root: true })
						this.loading = false
					})
				}
			} catch (error) {
				this.notify({
					text: 'Can not send email',
					color: 'error'
				}, { root: true })
			}
		},
	},
}
</script>

<style>
.unlayer-editor {
	height: 80vh;
}
</style>