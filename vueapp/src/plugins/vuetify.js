import Vue from 'vue';
import Vuetify, {
	VTextField, 
	VSelect,
	VListItemGroup,
} from 'vuetify/lib'
import {
	Ripple,
} from 'vuetify/lib/directives'

Vue.use(Vuetify, {
	components: {
		VTextField,
		VSelect,
		VListItemGroup,
	},
	directives: {
		Ripple,
	},
})

export default new Vuetify({
	theme: {
		options: {
			customProperties: true,
		},
		themes: {
			light: {
				primary: {
					darken2: '#466f9d', 
					base: '#1D99D3',
					lighten4: '#ebf2f6',
					lighten5: '#f9fdff',
				},
				secondary: '#1dbab4',
				// accent: '#82B1FF',
				error: '#FF5263',
				// info: '#2196F3',
				success: '#25E8C8',
				// warning: '#FFC107',
				'dark-color': {
					base: '#151B26',
					lighten1: '#303741',
				},
			},
		},
	},
});