<template>
	<div>
		<slot name="title"></slot>
		
		<v-data-table
			v-on="$listeners"
			v-bind="$attrs"
			v-if="items"
			:headers="headers"
			:items="items"
			:items-per-page="15"
			:search="search"
			elevation="0"
			:mobile-breakpoint="0">

			<template v-slot:top>
				<v-toolbar flat>
					<v-row class="justify-end">
						<v-col cols="8" md="6" lg="4">
							<v-text-field
								v-model="search"
								prepend-icon="mdi-magnify"
								label="Search"
								hide-details
								clearable
								dense>
							</v-text-field>
						</v-col>
					</v-row>
				</v-toolbar>
			</template>

			<template v-slot:item.actions="{ item }">
				<v-icon
					small
					class="mr-2"
					color="amber"
					@click.stop.prevent="editItem(item)">
					mdi-pencil
				</v-icon>
						
				<v-icon
					small
					color="red"
					@click.stop.prevent="deleteItem(item)">
					mdi-delete
				</v-icon>
			</template>

			<template
				v-for="(_, slot) in $scopedSlots"
				v-slot:[slot]="{item}">
				<slot :name="slot" :item="item"></slot>
			</template>

		</v-data-table>

		<v-dialog v-model="dialog"
			max-width="500px"
			scrollable>

			<a-form
				@cancel="dialog = false"
				@submit="submit">

				<slot
					name="form"
					:editedItem="editedItem">

					<vue-form-json-schema
						v-if="schema && uiSchema"
						v-model="editedItem"
						:schema="schema"
						:ui-schema="uiSchema"
						class="layout wrap">
					</vue-form-json-schema>
				</slot>

			</a-form>
								
		</v-dialog>

		<confirm
			ref="confirm">
		</confirm>
	</div>
</template>

<script>
import VueFormJsonSchema from 'vue-form-json-schema'
import AForm from './AForm'
import Confirm from './Confirm'

export default {
	components: {
		VueFormJsonSchema,
		AForm,
		Confirm,
	},
	props: {
		items: {
			type: Array,
			required: true,
		},
		headers: {
			type: Array,
			required: true,
		},
		schema: {
			type: Object,
		},
		uiSchema: {
			type: Array,
		},
	},
	data: () => ({
		editedItemIndex: -1,
		editedItem: null,
		dialog: false,
		search: '',
	}),
	methods: {
		addItem(item = {}) {
			this.editedItemIndex = -1
			this.editedItem = item
			this.$nextTick(() => this.dialog = true)
		},
		editItem(item) {
			this.editedItemIndex = this.items.indexOf(item)
			this.editedItem = Object.assign({}, item)
			this.$nextTick(() => this.dialog = true)
		},
		async deleteItem(item) {
			const confirm = await this.$refs.confirm.open('Delete', 'Are you sure?', { color: 'red' })
			if(confirm) this.$emit('delete', item, this.items.indexOf(item))
		},
		submit() {
			this.editedItemIndex === -1
				? this.$emit('create', this.editedItem)
				: this.$emit('update', this.editedItem, this.editedItemIndex)

			this.closeDialog()
		},
		closeDialog() {
			this.dialog = false
		},
	},
}
</script>