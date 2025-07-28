<template>
	<v-card
		elevation="0"
		height="100%"
		outlined>
		<v-card-title
			class="has-border-bottom">
			Comments & Activity
		</v-card-title>
		<v-container>
			<v-form
				ref="form"
				lazy-validation
				@submit.prevent="createNote">
				<v-text-field
					v-model="newNote.text"
					outlined
					placeholder="Type something…"
					hint="Press Enter to submit"
					:rules="[v => !!v || 'Please type some note']"
					dense
					required
					@blur="resetValidation">
				</v-text-field>
			</v-form>
			<div style="max-height: 9em;" class="overflow-y-auto">
				<v-simple-table class="v-data-table__no-borders">
					<template #default>
						<tbody>
							<comment
								v-for="item in items"
								:key="item.id"
								:value="item">
							</comment>
						</tbody>
					</template>
				</v-simple-table>
			</div>
		</v-container>
	</v-card>
</template>

<script>
import { clone } from 'lodash'

import Comment from './Comment'

export default {
	components: {
		Comment,
	},
	props: {
		items: {
			type: Array,
			default: () => ([]),
		},
	},
	data: () => ({
		newNote: {
			text: '',
		},
	}),
	methods: {
		createNote() {
			const valid = this.$refs.form.validate()
			if(valid) {
				this.$emit('create', clone(this.newNote))
				this.$refs.form.reset()
			}
		},
		resetValidation() {
			return this.$refs.form.resetValidation()
		},
	},
}
</script>