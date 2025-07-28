<template>
	<v-card 
		elevation="0"
		height="100%"
		outlined>
		<v-card-title>
			Roll Info
		</v-card-title>

		<v-divider></v-divider>

		<residential-alert
			v-if="!property.is_residential">
		</residential-alert>

		<v-container class="pa-0">
			<v-row class="ma-0">
				<v-col cols="6" class="has-border-right">
					<v-row>
						<v-col cols="9" class="py-0">
							<v-text-field
								v-model="property.address_line_1"
								label="Property Address"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
						<v-col cols="3" class="py-0">
							<!-- TODO: add model -->
							<v-text-field
								label="Unit #"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
					</v-row>

					<v-row>
						<v-col cols="12" class="py-0">
							<v-text-field
								v-model="property.address_line_2"
								class="pt-0 mt-0"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
					</v-row>

					<v-row>
						<v-col cols="7" class="py-0">
							<v-text-field
								v-model="property.town"
								class="pt-0 mt-0"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
						<v-col cols="2" class="py-0">
							<v-text-field
								v-model="property.state"
								class="pt-0 mt-0"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
						<v-col cols="3" class="py-0">
							<v-text-field
								v-model="property.zip"
								class="pt-0 mt-0"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
					</v-row>

					<v-row dense class="mt-4">
						<v-col cols="6" class="py-0">
							<v-text-field
								v-model="property.apn"
								label="Legal ID"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
						<v-col cols="6" class="py-0">
							<v-text-field
								:value="countyFilter(property.county, counties)"
								label="County"
								hide-details
								disabled></v-text-field>
						</v-col>
					</v-row>

					<v-row class="mt-2">
						<v-col class="py-0">
							<v-text-field
								v-model="property.district"
								label="Dist"
								disabled>
							</v-text-field>
						</v-col>
						<v-col class="py-0">
							<v-text-field
								v-model="property.section"
								label="Sec"
								disabled>
							</v-text-field>
						</v-col>
						<v-col class="py-0">
							<v-text-field
								v-model="property.block"
								label="Block"
								disabled>
							</v-text-field>
						</v-col>
						<v-col class="py-0">
							<v-text-field
								v-model="property.lot"
								label="Lot"
								disabled>
							</v-text-field>
						</v-col>
					</v-row>
					<v-row class="py-0" dense>
						<v-col class="py-0">
							<v-text-field
								v-model="property.property_class"
								label="Building Class"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
						<v-col class="py-0">
							<v-text-field
								v-model="assessment.swiss_code"
								label="Swiss Code"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
						<v-col cols="5" class="py-0">
							<v-text-field
								v-model="property.school_district"
								label="School District"
								hide-details
								disabled></v-text-field>
						</v-col>
					</v-row>
				</v-col>

				<v-col cols="6">
					<v-row>
						<v-col cols="9" class="py-0">
							<v-text-field
								v-model="lastOwners.first_full_name"
								label="First Owner Full Name"
								hide-details
								disabled></v-text-field>
						</v-col>
						<v-col cols="3" class="py-0">
							<v-text-field
								v-if="assessment.assessment_date"
								v-model="assessment.assessment_date.tax_year"
								label="Tax year"
								hide-details
								disabled></v-text-field>
						</v-col>
					</v-row>
					<v-text-field
						v-model="lastOwners.second_full_name"
						label="Second Owner Full Name"
						class="mt-4"
						hide-details
						disabled>
					</v-text-field>

					<v-row class="mt-4">
						<v-col cols="12" class="py-0">
							<v-text-field
								v-model="lastOwners.owner_address_1"
								label="Mailing Address"
								hide-details
								disabled>
							</v-text-field>
							<v-text-field
								v-model="lastOwners.owner_address_2"
								class="pt-0 mt-0"
								hide-details
								disabled>
							</v-text-field>
							<v-text-field
								v-model="lastOwners.owner_address_3"
								class="pt-0 mt-0"
								hide-details
								disabled>
							</v-text-field>
						</v-col>
					</v-row>

					<v-row class="mt-16 pt-10">
						<v-col class="pb-0">
							<v-btn
								:href="`https://www.pbcgov.org/papa/Asps/PropertyDetail/PropertyDetail.aspx?parcel=${application.apn}`"
								target="blank"
								color="primary"
								small
								outlined>
								Lookup Prop
							</v-btn>
						</v-col>
					</v-row>
				</v-col>
			</v-row>
		</v-container>
	</v-card>
</template>

<script>
import { mapGetters } from 'vuex'

import countyFilter from '../../mixins/countyFilter'

import ResidentialAlert from './ResidentialAlert'

export default {
	components: {
		ResidentialAlert,
	},
	props: {
		application: {
			type: Object,
			required: true,
		},
	},
	mixins: [
		countyFilter,
	],
	computed: {
		...mapGetters('counties', [
			'counties',
		]),
		property() {
			return this.application?.property || {}
		},
		assessment() {
			return this.application?.assessment || {}
		},
		lastOwners() {
			return this.property?.owners?.[0] || {}
		},
	},
}
</script>