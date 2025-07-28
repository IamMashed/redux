<template>
	<v-navigation-drawer
		v-model="show"
		app
		clipped
		:width="180"
		class="dark-color d-print-none">
		<v-list
			dense
			dark
			class="mt-6">

			<v-img
				v-if="isPTRC"
				src="@/assets/images/logo_ptrc.png"
				width="90"
				class="ma-auto">
			</v-img>
			<v-img
				v-else
				src="@/assets/images/logo_redux.png"
				width="150"
				class="ma-auto">
			</v-img>

			<v-subheader
				class="font-weight-bold text-uppercase subtitle-1 justify-center mt-5">
				Navigation
			</v-subheader>

			<quick-search-form></quick-search-form>

			<v-list-item-group color="primary">

				<v-divider></v-divider>

				<template
					v-for="(item, key) in filtredItems">

					<!-- TODO: Remove this after SPA migration completed -->
					<v-list-item
						v-if="item.href"
						:key="key"
						:href="item.href"
						:disabled="item.disabled"
						exact
						class="py-2"
						active-class="dark-color lighten-1 white--text">
						<v-list-item-content>
							<v-list-item-title>{{ item.title }}</v-list-item-title>
						</v-list-item-content>
					</v-list-item>

					<v-list-group
						v-else-if="item.group"
						:key="key"
						class="py-2"
						active-class="dark-color lighten-1 white--text">
						<template v-slot:activator>
							<v-list-item-title>{{ item.title }}</v-list-item-title>
						</template>

						<v-list
							v-if="item.items">
							<v-list-item-group color="primary">
								<v-list-item
									v-for="(item, key) in item.items"
									:key="key"
									:to="item.route"
									:exact="item.exact"
									:disabled="item.disabled"
									active-class="dark-color lighten-1 white--text">
									<v-list-item-title
										class="text-right">
										{{ item.title }}
									</v-list-item-title>
								</v-list-item>
							</v-list-item-group>
						</v-list>
					</v-list-group>

					<v-list-item
						v-else
						:key="key"
						:to="{
							params: $route.params,
							...item.route,
						}"
						:exact="item.exact"
						:disabled="item.disabled"
						class="py-2"
						active-class="dark-color lighten-1 white--text">

						<v-list-item-content>
							<v-list-item-title>
								{{ item.title }}
							</v-list-item-title>
						</v-list-item-content>

						<v-list-item-icon
							class="align-center">
							<v-chip
								v-if="item.chip"
								color="error"
								x-small>
								{{ item.chip }}
							</v-chip>
						</v-list-item-icon>
					</v-list-item>

					<v-divider :key="`${key}-divider`"></v-divider>

				</template>
			</v-list-item-group>
			
		</v-list>

		<template v-slot:append>
			<div class="d-flex justify-center">
				<v-btn
					href="/logout"
					small>
					Logout
				</v-btn>
			</div>
			<div class="pa-4 white--text">
				<small>Version: {{ version }}</small>
			</div>
		</template>

	</v-navigation-drawer>
</template>

<script>
import { mapGetters } from 'vuex'
import { version } from '../../package.json'

import QuickSearchForm from './Sidebar/QuickSearchForm'

export default {
	components: {
		QuickSearchForm,
	},
	data: () => ({
		version,
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
			'isMember',
			'isViewer',
			'isPTRC',
		]),
		...mapGetters('applications', {
			defaultApplicationStatus: 'defaultStatus',
			totalApplicationsCount: 'total',
		}),
		applicationsRoute() {
			const { key, applications } = this.defaultApplicationStatus
			return {
				name: 'application',
				params: {
					id: applications?.[0],
					status: key,
				},
			}
		},
		items() {
			return [
				{
					title: 'Dashboard',
					route: { name: 'dashboard' },
					exact: true,
					show: true,
				},
				{
					title: 'Tasks',
					group: true,
					items: [
						{
							title: 'Need to Answer',
							route: '',
							exact: true,
						},
						{
							title: 'Waiting for Answer',
							route: '',
							exact: true,
						},
					],
					show: this.isAdmin || this.isMember,
				},
				{
					title: 'Advanced Search',
					route: { name: 'lookup', hash: '#filters' },
					exact: true,
					show: !this.isPTRC && (this.isAdmin || this.isMember || this.isViewer),
				},
				{
					title: 'Single CMA',
					route: { name: 'cma' },
					exact: true,
					show: this.isAdmin || this.isMember || this.isViewer,
				},
				{
					title: 'Mass CMA',
					href: '/masscma',
					show: this.isAdmin || this.isMember,
				},
				{
					title: 'Applications',
					route: { name: 'applications' },
					exact: true,
					chip: this.totalApplicationsCount || '0',
					show: !this.isPTRC && (this.isAdmin || this.isMember || this.isViewer),
				},
				{
					title: 'Settings',
					group: true,
					items: [
						{
							title: 'Assessment Ratios',
							route: { name: 'ratios' },
							exact: true,
						},
						{
							title: 'Rule Sets',
							route: { name: 'rule-sets' },
						},
						{
							title: 'Time Adjustments',
							route: { name: 'time-adjustments' },
							exact: true,
						},
						{
							title: 'Assessment Dates',
							route: { name: 'assessment-dates' },
							exact: true,
						},
						{
							title: 'Client Tags',
							route: { name: 'tags' },
							exact: true,
						},
						{
							title: 'Misc Settings',
							route: { name: 'misc-settings' },
							exact: true,
						},
						{
							title: 'Upload Data',
							route: { name: 'upload-data' },
							exact: true,
						},
					],
					show: this.isAdmin || this.isMember,
				},
				{
					title: 'Admin',
					route: { name: 'admin' },
					exact: true,
					show: this.isAdmin,
				},
				{
					title: 'Email Templates (Demo)',
					route: { name: 'email-templates' },
					exact: true,
					show: this.isAdmin,
				},
			]
		},
		filtredItems() {
			return this.items.filter(item => !!item.show)
		},
		show: {
			get() {
				return this.$store.state.sidebar.show;
			},
			set(value) {
				this.$store.commit('sidebar/SET_SHOW', value);
			},
		},
	},
}
</script>