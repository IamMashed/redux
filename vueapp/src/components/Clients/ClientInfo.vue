<template>
	<v-card outlined
		height="100%">
		<v-card-title>
			Client Info
			<v-spacer></v-spacer>
			<template v-if="this.isAdmin || this.isMember">
				<v-btn v-if="!isClientEditable"
					small
					icon
					@click="isClientEditable = !isClientEditable">
					<v-icon>mdi-square-edit-outline</v-icon>
				</v-btn>
				<v-card-actions v-else
					class="pa-0">
					<v-btn
						color="success"
						small
						tile
						outlined
						icon
						@click="save">
						<v-icon small>mdi-check</v-icon>
					</v-btn>
					<v-btn
						color="error"
						small
						tile
						outlined
						icon
						@click="cancel">
						<v-icon small>mdi-close</v-icon>
					</v-btn>
				</v-card-actions>
			</template>
		</v-card-title>
		<v-divider></v-divider>
		<v-container class="pb-0">
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Client ID</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<v-text-field v-if="isClientEditable"
						v-model="localClient.case_id"
						hide-details
						outlined
						dense>
					</v-text-field>
					<p v-else class="mb-0">{{ client.case_id }}</p>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>First Name</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<v-text-field v-if="isClientEditable"
						v-model="localClient.first_name"
						hide-details
						outlined
						dense>
					</v-text-field>
					<p v-else class="mb-0">{{ client.first_name }}</p>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Last Name</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<v-text-field v-if="isClientEditable"
						v-model="localClient.last_name"
						hide-details
						outlined
						dense>
					</v-text-field>
					<p v-else class="mb-0">{{ client.last_name }}</p>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Tags</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<v-autocomplete
						v-if="isClientEditable"
						v-model="localClient.tags"
						:items="tags"
						chips
						dense
						small-chips
						multiple
						outlined
						hide-details
						item-text="name"
						item-value="id"
						return-object>
						<template #selection="{ item, select, attrs }">
							<v-chip
								v-bind="attrs"
								:key="item.id"
								small
								dark
								class="chip--select-multi ma-1"
								:color="`${colorHash(item.name)} lighten-2`"
								@input="select">
								{{ item.name }}
							</v-chip>
						</template>
					</v-autocomplete>
					<v-chip
						v-else
						v-for="(item) in client.tags"
						:key="item.id"
						small
						dark
						class="chip--select-multi ma-1"
						:color="`${colorHash(item.name)} lighten-2`">
						{{ item.name }}
					</v-chip>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Mailing Address</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<template v-if="isClientEditable">
						<v-text-field
							v-model="localClient.mailing_line1"
							hide-details
							outlined
							dense>
						</v-text-field>
						<v-text-field
							v-model="localClient.mailing_line2"
							hide-details
							outlined
							dense>
						</v-text-field>
						<v-text-field
							v-model="localClient.mailing_line3"
							hide-details
							outlined
							dense>
						</v-text-field>
					</template>
					<template v-else>
						<p>{{ client.mailing_line1 }}<p>
						<p>{{ client.mailing_line2 }}<p>
						<p>{{ client.mailing_line3 }}</p>
					</template>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Phone 1</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<v-text-field
						v-if="isClientEditable"
						v-model="localClient.phone_number_1"
						hide-details
						outlined
						dense>
					</v-text-field>
					<p v-else class="mb-0">{{ client.phone_number_1 | phone }}</p>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Phone 2</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<v-text-field
						v-if="isClientEditable"
						v-model="localClient.phone_number_2"
						hide-details
						outlined
						dense>
					</v-text-field>
					<p v-else class="mb-0">{{ client.phone_number_2 | phone }}</p>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Email</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<v-text-field v-if="isClientEditable && localClient.email"
						v-model="localClient.email.email_address"
						hide-details
						outlined
						dense>
					</v-text-field>
					<p v-else class="mb-0">{{ client.email && client.email.email_address }}</p>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Total Paid</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<!-- TODO: add model -->
					<p></p>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="4" class="py-1">
					<p class="mb-2">
						<b>Total Balance</b>
					</p>
				</v-col>
				<v-col cols="8" class="py-1">
					<!-- TODO: add model -->
					<p></p>
				</v-col>
			</v-row>
		</v-container>
	</v-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { clone } from 'lodash'
import colorHash from '../../mixins/colorHash'

export default {
	mixins: [
		colorHash,
	],
	props: {
		client: {
			type: Object,
			required: true,
		},
	},
	data: () => ({
		isClientEditable: false,
		localClient: {},
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
			'isMember',
		]),
		...mapGetters('tags', [
			'tags',
		]),
	},
	methods: {
		...mapActions('tags', [
			'loadTags',
		]),
		save() {
			this.$emit('update:client', this.localClient)
			this.isClientEditable = false
		},
		cancel() {
			this.localClient = clone(this.client)
			this.isClientEditable = false
		},
	},
	mounted() {
		this.loadTags()
	},
	watch: {
		client: {
			deep: true,
			immediate: true,
			handler(newVal) {
				this.localClient = clone(newVal)
			},
		},
	},
}
</script>