<template>
	<v-app id="app">
		
		<app-sidebar></app-sidebar>
		
		<v-main>
			<transition name="slide-fade" mode="out-in">
				<router-view></router-view>
			</transition>

			<app-loader></app-loader>
		</v-main>

		<app-notification></app-notification>

	</v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import AppSidebar from './components/AppSidebar'
import AppNotification from './components/AppNotification'
import AppLoader from './components/AppLoader'

export default {
	components: {
		AppSidebar,
		AppNotification,
		AppLoader,
	},
	computed: {
		...mapGetters('auth', [
			'isAdmin',
			'isMember',
			'isPTRC',
		]),
	},
	methods: {
		...mapActions('auth', [
			'loadUser',
		]),
		...mapActions('applications', [
			'loadCaseInfo',
		]),
	},
}
</script>

<style lang="scss">

@import './scss/main.scss';

.slide-fade-enter-active {
	transition: all .3s ease;
}

.slide-fade-leave-active {
	transition: all .3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}

.slide-fade-enter, .slide-fade-leave-to {
	transform: translateX(2em);
	opacity: 0;
}

.white-space-pre {
	white-space: pre;
}

/* Printing styles */
@media print {

	@page {
		size: landscape;
	}

	.v-content {
		padding: 0 !important;
	}

	.container {
		max-width: unset;
	}
}

</style>