<template>
	<tr class="comment">
		<td class="px-0">
			<v-icon
				:color="noteType.color || 'primary'"
				small
				class="outlined ma-1 mr-4">
				{{ noteType.icon || 'mdi-comment-processing' }}
			</v-icon>
		</td>
		<td class="pl-0">
			<!-- Show address and link to case if sender is Application and has nested case -->
			<span v-if="value.sender === 1 && senderModel.case_property">
				(<router-link
					:to="{
						name: 'client-case',
						params: {
							id: this.senderModel.client_id,
							caseid: this.senderModel.case_property_id,
						},
					}">
					{{ senderModel.case_property.address_line1 }}, {{ senderModel.case_property.address_line2 }}
				</router-link>)
			</span>

			<!-- Show address and link to case if sender is Case -->
			<span v-if="value.sender === 3">
				(<router-link
					:to="{
						name: 'client-case',
						params: {
							id: this.senderModel.client_id,
							caseid: this.senderModel.id,
						},
					}">
					{{ senderModel.address_line1  }}, {{ senderModel.address_line2 }}
				</router-link>)
			</span>
			{{ value.text }}
			<file-downloader
				v-if="value.attachment_extension"
				:id="value.id"
				:name="value.text">
			</file-downloader>
		</td>
		<td class="grey--text">
			{{ value.created_by && value.created_by.username }}
		</td>
		<td class="text-right grey--text pr-0">
			{{ value.created_at | datetime }}
		</td>
	</tr>
</template>

<script>
import FileDownloader from '../FileDownloader'

export default {
	components: {
		FileDownloader,
	},
	props: {
		value: {
			type: Object,
			required: true,
		},
	},
	data: () => ({
		noteTypes: [
			{
				name: 'updated',
				icon: 'mdi-pencil',
			},
			{
				name: 'submitted',
				icon: 'mdi-file-outline',
			},
			{
				name: 'reviewed',
				icon: 'mdi-check',
			},
			{
				name: 'approved',
				icon: 'mdi-check-all',
				color: 'success',
			},
			{
				name: 'approved_contract',
				icon: 'mdi-check-all',
				color: 'success',
			},
			{
				name: 'rejected',
				icon: 'mdi-close',
				color: 'error',
			},
			{
				name: 'fully_rejected',
				icon: 'mdi-delete-forever-outline',
				color: 'error',
			},
			{
				name: 'bounced',
				icon: 'mdi-email-off-outline',
				color: 'error',
			},
			{
				name: 'paid',
				icon: 'mdi-currency-usd',
				color: 'success',
			},
		],
	}),
	computed: {
		noteType() {
			return this.noteTypes.find(item => item.name === this.value.type?.action) || {}
		},
		senderModel() {
			return this.value?.sender_model || {}
		},
	},
}
</script>

<style lang="scss">
.comment td:nth-child(3) {
	width: 8em;
}

.comment td:nth-child(4) {
	width: 15em;
}
</style>