import { Model } from '@vuex-orm/core'
import filters from '../filters/filters'

class Comp extends Model {

	static entity = 'comps'

	static fields () {
		return {
			id: this.number(),
			address: this.string(null).nullable(),
			address_line_1: this.string(null).nullable(),
			address_line_2: this.string(null).nullable(),
			address_unit: this.string(null).nullable(),
			adjusted_market_value: this.number(null).nullable(),
			adjustment_delta_value: this.number(null).nullable(),
			adjustments: this.attr(),
			age: this.number(null).nullable(),
			apn: this.string(null).nullable(),
			assessment_stage: this.string(null).nullable(),
			basement_type: this.number(null).nullable(),
			bedrooms: this.number(null).nullable(),
			block: this.string(null).nullable(),
			building_code: this.number(null).nullable(),
			buyer_full_name: this.string(null).nullable(),
			city: this.string(null).nullable(),
			comp_assessment_value: this.number(null).nullable(),
			comp_market_value: this.number(null).nullable(),
			condition: this.string(null).nullable(),
			condo_code: this.string(null).nullable(),
			condo_code_description: this.string(null).nullable(),
			condo_view_floor: this.string(null).nullable(),
			condo_view_influence: this.string(null).nullable(),
			condo_view_location: this.string(null).nullable(),
			coordinate_x: this.number(null).nullable(),
			coordinate_y: this.number(null).nullable(),
			county: this.string(null).nullable(),
			cma_notification: this.attr(null).nullable(),
			data_composite: this.number(null).nullable(),
			district: this.attr(null).nullable(),
			effective_age: this.number(null).nullable(),
			fireplaces: this.number(null).nullable(),
			full_baths: this.number(null).nullable(),
			garage_type: this.number(null).nullable(),
			garages: this.number(null).nullable(),
			gas: this.boolean(null).nullable(),
			gla_sqft: this.number(null).nullable(),
			half_baths: this.number(null).nullable(),
			hamlet: this.string(null).nullable(),
			heat_type: this.string(null).nullable(),
			is_condo: this.boolean(null).nullable(),
			is_listed: this.boolean(null).nullable(),
			is_residential: this.boolean(null).nullable(),
			kitchens: this.number(null).nullable(),
			land_tag: this.number(null).nullable(),
			land_type_code: this.string(null).nullable(),
			land_use: this.number(null).nullable(),
			last_sale_date: this.string(null).nullable(),
			last_sale_price:this.number(null).nullable(),
			latitude: this.number(null).nullable(),
			legal: this.string(null).nullable(),
			location: this.number(null).nullable(),
			longitude: this.number(null).nullable(),
			lot: this.string(null).nullable(),
			lot_size: this.number(null).nullable(),
			lot_size_sqft: this.number(null).nullable(),
			new_record: this.boolean(null).nullable(),
			number: this.string(null).nullable(),
			obs_geojson: this.attr({}).nullable(),
			origin: this.string(null).nullable(),
			other_adjustment: this.string(null).nullable(),
			other_adjustment_description: this.string(null).nullable(),
			owners: this.attr([]),
			patio_type: this.number(null).nullable(),
			paving_type: this.number(null).nullable(),
			photos: this.attr([]),
			pool: this.boolean(null).nullable(),
			porch_type: this.number(null).nullable(),
			price_per_sqft: this.number(null).nullable(),
			print_key: this.string(null).nullable(),
			print_sale_info: this.boolean(null).nullable(),
			priority: this.number(null).nullable(),
			property_class: this.number(null).nullable(),
			property_class_description: this.string(null).nullable(),
			property_class_type: this.number(null).nullable(),
			property_county: this.attr({}),
			property_style: this.string(null).nullable(),
			proximity: this.number(null).nullable(),
			reference_building: this.number(null).nullable(),
			rooms: this.number(null).nullable(),
			school_district: this.number(null).nullable(),
			section: this.string(null).nullable(),
			seller_full_name: this.string(null).nullable(),
			sewer_type: this.number(null).nullable(),
			state: this.string(null).nullable(),
			status: this.string(null).nullable(),
			story_height: this.number(null).nullable(),
			street: this.string(null).nullable(),
			subdivision: this.string(null).nullable(),
			town: this.string(null).nullable(),
			under_air_gla_sqft: this.number(null).nullable(),
			village: this.string(null).nullable(),
			water_category: this.number(null).nullable(),
			water_type: this.number(null).nullable(),
			waterfront: this.boolean(null).nullable(),
			workups: this.attr([]),
			year: this.number(null).nullable(),
			zip: this.number(null).nullable(),

			r_type: this.string(null).nullable(),
			selected: this.boolean(false),
		}
	}

	get proximity_formatted() {
		const { proximity } = this
		return Number(proximity).toFixed(2) || proximity
	}

	get gla_sqft_formatted() {
		return filters.bignum(this.gla_sqft)
	}

	get last_sale_price_formatted() {
		return filters.currency(this.last_sale_price)
	}

	get last_sale_date_formatted() {
		return filters.date(this.last_sale_date)
	}

	get class() {
		return filters.classFilter(this.property_class, this.county)
	}

	get style() {
		const store = this.$store()
		const constants = store.getters['constants/constants']
		return filters.mapperFilter(this.property_style, constants.property_style_map)
	}

	get baths() {
		return this.full_baths + (0.5 * this.half_baths)
	}

	get age_effective_age() {
		const {
			age,
			effective_age,
		} = this

		let text = age
		if (effective_age) {
			text += ` (${effective_age})`
		}

		return text
	}

	get condo_view() {
		const {
			county,
			condo_code,
			condo_code_description,
			condo_view_floor,
			condo_view_influence,
			condo_view_location,
		} = this
		if (county === 'broward') {
			return `${condo_view_floor} ${condo_view_location} ${condo_view_influence}`
		} else {
			if (condo_code) {
				return `(${condo_code}) ${ condo_code_description }`
			} else {
				return `-`
			}
		}
	}

	get adjusted_market_value_formatted() {
		return filters.currency(this.adjusted_market_value)
	}

	get comp_assessment_value_formatted() {
		return filters.bignum(this.comp_assessment_value)
	}

	get is_subject() {
		return this.r_type === 'SBJ'
	}

}

export default Comp