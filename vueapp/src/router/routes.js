import Home from '../views/Home.vue'

const routes = [
	{
		path: '/',
		name: 'home',
		component: Home,
	},
	{
		path: '/dashboard',
		name: 'dashboard',
		component: () => import('../views/Dashboard.vue'),
		meta: {
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'guest',
			],
		},
	},
	{
		path: '/ratios',
		name: 'ratios',
		component: () => import('../views/Ratios.vue'),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/time-adjustments',
		name: 'time-adjustments',
		component: () => import('../views/TimeAdjustments.vue'),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/cma',
		name: 'cma',
		component: () => import('../views/Cma.vue'),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		},
	},
	{
		path: '/cma/:id',
		name: 'cma-compare',
		component: () => import('../views/CmaCompare.vue'),
		props: ({ params, query }) => ({
			id: Number(params.id),
			assessmentDateId: Number(query['assessment-date']) || null,
		}),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		}
	},
	{
		path: '/workups/:id',
		name: 'workup',
		component: () => import('../views/Workup.vue'),
		props: ({ params }) => ({
			id: Number(params.id),
		}),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		}
	},
	{
		path: '/assessment-dates',
		name: 'assessment-dates',
		component: () => import('../views/AssessmentDates.vue'),
		props: true,
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/rule-sets',
		name: 'rule-sets',
		component: () => import('../views/RuleSets.vue'),
		props: true,
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/rule-sets/:id',
		name: 'rule-set',
		component: () => import('../views/RuleSets/Edit.vue'),
		props: (route) => ({
			id: Number(route.params.id)
		}),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/rule-sets/create',
		name: 'create-rule-set',
		component: () => import('../views/RuleSets/Create.vue'),
		props: true,
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/misc-settings',
		name: 'misc-settings',
		component: () => import('../views/MiscSettings.vue'),
		props: true,
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/applications',
		name: 'applications',
		component: () => import('../views/CaseManagement/Applications.vue'),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		},
	},
	{
		path: '/applications/:status(incoming|rejected|reviewed|approved|fully_rejected)/:id',
		name: 'application',
		component: () => import('../views/CaseManagement/Application.vue'),
		props: (route) => ({
			id: Number(route.params.id),
			status: route.params.status,
		}),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		},
	},
	{
		path: '/case-management/tags',
		name: 'tags',
		component: () => import('../views/CaseManagement/Tags.vue'),
		props: true,
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
			],
		},
	},
	{
		path: '/admin',
		name: 'admin',
		component: () => import('../views/Admin.vue'),
		props: true,
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
			],
		},
	},
	{
		path: '/users/:id',
		name: 'user',
		component: () => import('../views/User.vue'),
		props: (route) => ({
			id: Number(route.params.id),
		}),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
			],
		},
	},
	{
		path: '/users/create',
		name: 'user-create',
		component: () => import('../views/User.vue'),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
			],
		},
	},
	{
		path: '/lookup',
		name: 'lookup',
		component: () => import('../views/Lookup.vue'),
		props: true,
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		},
	},
	{
		path: '/clients/:id',
		component: () => import('../views/Client.vue'),
		props: (route) => ({
			id: Number(route.params.id)
		}),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		},
		children: [
			{
				path: '',
				name: 'client',
				component: () => import('../components/Clients/Cases.vue'),
				meta: {
					auth: true,
					allowedRoles: [
						'admin',
						'member',
						'viewer',
					],
				},
			},
			{
				path: 'cases/:caseid',
				name: 'client-case',
				component: () => import('../components/Clients/Case.vue'),
				props: (route) => ({
					caseid: Number(route.params.caseid),
				}),
				meta: {
					auth: true,
					allowedRoles: [
						'admin',
						'member',
						'viewer',
					],
				},
			},
		],
	},
	{
		path: '/upload-data',
		name: 'upload-data',
		component: () => import('../views/UploadData.vue'),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		},
	},
	{
		path: '/email-templates',
		name: 'email-templates',
		component: () => import('../views/EmailTemplates.vue'),
		meta: { 
			auth: true,
			allowedRoles: [
				'admin',
				'member',
				'viewer',
			],
		},
	},
]

export default routes