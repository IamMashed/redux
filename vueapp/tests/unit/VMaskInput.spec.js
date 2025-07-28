import {
	mount,
	createLocalVue,
} from '@vue/test-utils'
import Vuetify from 'vuetify'
import VMaskInput from '@/components/VMaskInput.vue'

describe('VMaskInput.vue', () => {
	let localVue
	let vuetify

	beforeEach(() => {
		localVue = createLocalVue()
		vuetify = new Vuetify()
	})

	it('format phone number correctly', () => {
		const mask = '(999) 999-9999'
		const value = '5879111731'
		const displayValue = '(587) 911-1731'

		const wrapper = mount(VMaskInput, {
			localVue,
			vuetify,
			propsData: {
				mask,
				value,
			},
		})
		expect(wrapper.find('input').element.value).toMatch(displayValue)
	})
})