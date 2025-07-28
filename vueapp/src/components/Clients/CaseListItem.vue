<template>
	<v-list-item three-line
		:to="route"
		class="pl-0">
		<v-col cols="2">
			<v-img :src="require('@/assets/images/no_photo.png')" height="125" max-width="200"></v-img>
		</v-col>
		<v-col cols="7">
			<v-row>
				<v-col cols="3" class="py-1">
					<b>Address</b>
				</v-col>
				<v-col cols="9" class="py-1">{{ value.address_line1 }} {{ value.address_line2 }}</v-col>
			</v-row>
			<v-row>
				<v-col cols="3" class="py-1">
					<b>Legal Address</b>
				</v-col>
				<v-col cols="9" class="py-1">{{ value.apn }}</v-col>
			</v-row>
			<v-row>
				<v-col cols="3" class="py-1">
					<p>
						<b>Filing Fee Status</b>
					</p>
				</v-col>
				<v-col cols="9" class="py-1">
					{{ value.payment_status && value.payment_status.description }}

					<copy-payment-link
						v-if="value. application && value.application.payment_status_id !== 2"
						:application-id="value.application.id">
					</copy-payment-link>
				</v-col>
			</v-row>
		</v-col>
		<v-col cols="3" class="px-0">
			<v-row>
				<v-col cols="6" class="py-0">
					<span class="pr-4">
						<b>Case ID</b>
					</span>
					<span>{{ value.case_id }}</span>
				</v-col>
				<v-col cols="6" class="py-0">
					<span class="pr-4">
						<b>Tax Year</b>
					</span>
					<span>{{ value.tax_year }}</span>
				</v-col>
			</v-row>
			<v-row>
				<v-col
					class="pa-0">
					<client-status-stepper
						v-if="value.status"
						:step="value.status.status_order">
					</client-status-stepper>
				</v-col>
				<v-btn
					class="mr-4"
					small
					icon
					color="info"
					@click.stop.prevent="showTimeline = true">
					<v-icon small>mdi-information-outline</v-icon>
				</v-btn>
			</v-row>
			<v-row>
				<v-col cols="3" class="py-0">
					<span>
						<b>Status</b>
					</span>
				</v-col>
				<v-col cols="8" class="py-0">
					<span>{{ value.status && value.status.name }}</span>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="3" class="py-0">
					<span>
						<b>Date</b>
					</span>
				</v-col>
				<v-col cols="8" class="py-0">
					<span>{{ value.updated_at | date}}</span>
				</v-col>
			</v-row>
		</v-col>
		<case-timeline
			v-if="value.status"
			v-model="showTimeline"
			:step="value.status.status_order">
		</case-timeline>
	</v-list-item>
</template>

<script>
import ClientStatusStepper from './ClientStatusStepper'
import CaseTimeline from './CaseTimeline'
import CopyPaymentLink from '../Applications/CopyPaymentLink'

export default {
	components: {
		ClientStatusStepper,
		CaseTimeline,
		CopyPaymentLink,
	},
	props: {
		value: {
			type: Object,
			required: true,
		},
		clickable: {
			type: Boolean,
			default: true,
		},
	},
	data: () => ({
		showTimeline: false,
	}),
	computed: {
		route() {
			const route = {
				name: 'client-case',
				params: {
					id: this.value?.client_id,
					caseid: this.value?.id,
				},
			}
			return this.clickable ? route : null
		},
	},
}
</script>