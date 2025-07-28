<template>
	<v-container
		class="d-flex pa-0 main-container">

		<aside class="filter-sidebar grey lighten-5">
			<v-container>
				<h2 class="overline">Filters</h2>

				<v-autocomplete
					v-model="filters['client.tags']"
					:items="tags"
					label="Tags"
					chips
					dense
					small-chips
					multiple
					hide-details
					item-text="name"
					item-value="id"
					return-object
					class="v-input--no-border mt-6">
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

				<v-divider class="mt-6"></v-divider>

				<v-autocomplete
					v-model="filters['assigned_to']"
					:items="users"
					label="Assigned To"
					chips
					dense
					small-chips
					multiple
					hide-details
					item-text="username"
					item-value="id"
					class="v-input--no-border mt-6">
					<template #selection="{ item, select, attrs }">
						<v-chip
							v-bind="attrs"
							:key="item.id"
							small
							dark
							class="chip--select-multi ma-1"
							:color="`${colorHash(item.username)} lighten-2`"
							@input="select">
							{{ item.username }}
						</v-chip>
					</template>
				</v-autocomplete>

			</v-container>
		</aside>
			
		<v-container>
			<h1 class="title">Applications</h1>
			<v-data-table
				:items="filteredApplications"
				:headers="headers">

				<template #item.client="{ item }">
					{{ item.first_name }} {{ item.last_name }}
				</template>

				<template #item.tags="{ item }">
					<v-autocomplete
						v-model="item.client.tags"
						:items="tags"
						chips
						dense
						small-chips
						multiple
						hide-details
						item-text="name"
						item-value="id"
						return-object
						class="v-input--no-border"
						@input="() => updateApplications(item)">
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
				</template>

				<template #item.assigned_to="{ item }">
					<v-autocomplete
						v-model="item.assigned_to"
						:items="users"
						chips
						dense
						small-chips
						hide-details
						item-text="username"
						item-value="id"
						class="v-input--no-border"
						@input="() => updateApplications(item)">
						<template #selection="{ item, select, attrs }">
							<v-chip
								v-bind="attrs"
								:key="item.id"
								small
								dark
								class="chip--select-multi ma-1"
								:color="`${colorHash(item.username)} lighten-2`"
								@input="select">
								{{ item.username }}
							</v-chip>
						</template>
					</v-autocomplete>
				</template>

				<template #item.updated_at="{ value, item }">
					{{ item.updated_at | date }}
				</template>
			</v-data-table>
		</v-container>

	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'
import { flatten, isEqual } from 'lodash'
import { resolve } from '../../utils'
import colorHash from '../../mixins/colorHash'

const applicationsApi = apiFactory.get('applications')

export default {
	mixins: [
		colorHash,
	],
	data: () => ({
		applications: [],
		headers: [
			{
				text: 'Client',
				value: 'client',
			},
			{
				text: 'Property',
				value: 'property_address',
			},
			{
				text: 'Tags',
				value: 'tags',
			},
			{
				text: 'Assigned To',
				value: 'assigned_to',
			},
			{
				text: 'Updated At',
				value: 'updated_at',
			},
		],
		filters: {
			'client.tags': [],
		},
	}),
	computed: {
		...mapGetters('tags', [
			'tags',
		]),
		...mapGetters('users', [
			'users',
		]),
		queryFilters() {
            const filters = this.filters
            let query = {}
            for (let keys in filters) {
                if (filters[keys].constructor === Array && filters[keys].length > 0) {
                    query[keys] = filters[keys]
                }
			}
			return query
		},
		filteredApplications() {
			const query = this.queryFilters

            let filteredData = this.applications.filter( (item) => {
                for (let key in query) {
					const val = resolve(key, item)
                    if (val === undefined) {
                        return false
                    } else if (!flatten(query[key]).find(i => {
							if(Array.isArray(val)) {
								return val.find(j => j.id === i.id)
							} else {
								return isEqual(i, val)
							}
						})) {
                        return false
                    } else {
                        return true
                    }
                }
                return true
			})
			return filteredData
		}
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		...mapActions('tags', [
			'loadTags',
		]),
		...mapActions('users', [
			'loadUsers',
		]),
		async loadApplications() {
			try {
				const { data } = await applicationsApi.getAll()
				this.applications = data
			} catch(error) {
				this.notify({
					text: 'Can not load Applications',
					color: 'error'
				}, { root: true })
			}
		},
		async updateApplications(application) {
			try {
				const { data } = await applicationsApi.update(application)
				const index = this.applications.findIndex(item => item.id === data.id)
				this.$set(this.applications, index, data)
			} catch(error) {
				this.notify({
					text: 'Can not update Application',
					color: 'error'
				}, { root: true })
			}
		},
	},
	mounted() {
		this.loadApplications()
		this.loadTags()
		this.loadUsers()
	},
}
</script>

<style scoped>
.main-container {
	min-height: 100vh;
}

.filter-sidebar {
	width: 15em;
}
</style>