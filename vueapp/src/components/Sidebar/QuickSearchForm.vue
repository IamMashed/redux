<template>
	<v-form ref="form"
		class="quick-search-from"
		autocomplete="off"
		@submit.prevent="quickSearch">
		<v-menu offset-y
			max-height="50vh">
			<template v-slot:activator="{ on, attrs }">
				<v-text-field
					v-model="search"
					v-on="on"
					v-bind="attrs"
					class="mx-4"
					color="primary"
					prepend-inner-icon="mdi-magnify"
					placeholder="Search"
					:loading="loading"
					hint="Press Enter to submit"
					dense
					outlined>
				</v-text-field>
			</template>
			<v-list v-if="isMenu"
				dense>
				<template v-for="(group, g) in resultGroups">
					<v-divider
						v-if="g > 0"
						:key="`${g}-divider`"></v-divider>
					<v-subheader
						:key="`${g}-subheader`"
						class="pl-4 grey--text text-uppercase"
						inset>
						{{ group.groupName }}
					</v-subheader>
					<quick-search-item
						v-for="(item, key) in group.results"
						:key="`${g}-${key}`"
						:item="item">
					</quick-search-item>
				</template>
			</v-list>
		</v-menu>
	</v-form>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'

const quickSearchApi = apiFactory.get('quick-search')

import QuickSearchItem from './QuickSearchItem'

export default {
	components: {
		QuickSearchItem,
	},
	data: () => ({
		search: '',
		results: [],
		loading: false,
	}),
	computed: {
		...mapGetters('search', [
			'entities',
		]),
		isMenu() {
			return this.results.length > 0
		},
		resultGroups() {
			return this.entities.map(item => {
				const results = this.results.filter(r => r.entity === item.name)
				return {
					...item,
					results,
				}
			})
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		async quickSearch() {
			try {
				this.loading = true
				const { data } = await quickSearchApi.search({ search: this.search })
				this.results = data
			} catch (error) {
				this.notify({
					text: 'Can not perform search',
					color: 'error'
				}, { root: true })
			} finally {
				this.loading = false
			}
		},
	},
}
</script>

<style lang="scss">

.quick-search-from {

	.v-text-field--outlined {

		&.v-input--is-focused {
			width: 20em;
			max-width: 20em;
			z-index: 1;
		}

		&:not(.v-input--is-focused):not(.v-input--has-state) {
			& > .v-input__control {
				& > .v-input__slot {
					background-color: #303741;
					
					fieldset {
						border-color: #9ca6af;
					}

					input {
						color: #9ca6af;
					}
				}
			}
		}

		& > .v-input__control {
			& > .v-input__slot {
				background-color: #ffffff;

				input {
					color: #151b26;
				}
			}
		}
	}
}

</style>