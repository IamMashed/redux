<template>
	<v-container class="pa-4">
		<v-form>
			<v-row>
				<v-col cols="3">
					<v-row class="pb-5">
						<v-col cols="5" class="py-0">
							<span>
								<b>Full Address</b>
							</span>
						</v-col>
						<v-col cols="7" class="py-0">
							<span>{{ property.address_line_1 }}</span>
							<v-divider></v-divider>
							<span>{{ property.city }}</span>
							<v-divider></v-divider>
							<span>{{ property.state }} {{ property.zip }}</span>
							<v-divider></v-divider>
						</v-col>
					</v-row>
					<v-row>
						<v-col cols="7">
							<span>
								<b>School District</b>
							</span>
						</v-col>
						<v-col cols="5">
							<span>{{ property.school_district }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col cols="7">
							<span>
								<b>Building Class</b>
							</span>
						</v-col>
						<v-col cols="5">
							<span>{{ property.property_class }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col cols="7">
							<span>
								<b>SWISS Code</b>
							</span>
						</v-col>
						<v-col cols="5">
							<!-- TODO: Add model -->
							<span>{{ }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col cols="7">
							<span>
								<b>PIN Code</b>
							</span>
						</v-col>
						<v-col cols="5">
							<span>{{ value.pin_code }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col cols="7">
							<span>
								<b>Payment Type</b>
							</span>
						</v-col>
						<v-col v-if="isCaseEditable"
							cols="5"
							class="py-2">
							<v-select
								v-model="localCase.payment_type_id"
								:items="paymentTypes"
								item-value="id"
								item-text="description"
								hide-details
								outlined
								dense>
							</v-select>
						</v-col>
						<v-col v-else
							cols="5">
							<span>{{ value.payment_type &&  value.payment_type.description }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col cols="7">
							<span>
								<b>Payment Status</b>
							</span>
						</v-col>
						<v-col v-if="isCaseEditable"
							cols="5"
							class="py-2">
							<v-select
								v-model="localCase.payment_status_id"
								:items="paymentStatuses"
								item-value="id"
								item-text="description"
								hide-details
								outlined
								dense>
							</v-select>
						</v-col>
						<v-col v-else
							cols="5">
							<span>{{ value.payment_status &&  value.payment_status.description }}</span>
						</v-col>
					</v-row>
					<v-row>
						<v-col>
							<router-link
								:to="{
									name: 'cma-compare',
									params: {
										id: property.id,
									}
								}"
								target="_blank">
								<b>Run Single CMA</b>
							</router-link>
						</v-col>
					</v-row>
				</v-col>

				<v-col cols="4">
					<v-row>
						<v-col cols="2" class="py-0">
							<b>Folio</b>
						</v-col>
						<v-col cols="7" class="py-0">
							<span>{{ property.apn }}</span>
						</v-col>
					</v-row>
					<v-row class="mb-13">
						<v-col class="py-0">
							<b class="mr-4">Sec</b>
							<span>{{ property.section }}</span>
						</v-col>
						<v-col class="py-0">
							<b class="mr-4">Block</b>
							<span>{{ property.block }}</span>
						</v-col>
						<v-col class="py-0">
							<b class="mr-4">Lot</b>
							<span>{{ property.lot }}</span>
						</v-col>
					</v-row>
					<v-row>
						<v-col cols="4">
							<b>Land Use Code</b>
						</v-col>
						<v-col cols="2">
							<span>{{ property.land_use }}</span>
						</v-col>
						<v-col cols="6">
							<span>{{ property.land_use | mapperFilter(constants.land_tag_map) }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col cols="4">
							<b>County Name</b>
						</v-col>
						<v-col cols="2">
							<span>{{ property.property_county && property.property_county.number }}</span>
						</v-col>
						<v-col cols="6">
							<span>{{ property.property_county && property.property_county.name }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col cols="4">
							<b>Town Name</b>
						</v-col>
						<v-col cols="2">
							<!-- TODO: Add model field -->
							<span>{{  }}</span>
						</v-col>
						<v-col cols="6">
							<span>{{ property.town }}</span>
						</v-col>
					</v-row>

					<v-divider></v-divider>
					<v-row>
						<v-col cols="4">
							<b>Market Value (Roll)</b>
						</v-col>
						<v-col cols="2">
						</v-col>
						<v-col cols="6">
							<span>{{ localCase.assessment && localCase.assessment.value | bignum }}</span>
						</v-col>
					</v-row>
					<v-divider></v-divider>

					<v-row>
						<v-col cols="4">
							<b>Market Value (Override)</b>
						</v-col>
						<v-col cols="2">
						</v-col>
						<v-col v-if="isCaseEditable"
							cols="6">
							<v-autonumeric
								v-if="localCase.assessment"
								v-model="localCase.assessment.market_value_override"
								:an-options="{
									decimalPlaces: 0,
									emptyInputBehavior: 'null',
								}"
								outlined
								dense>
							</v-autonumeric>
						</v-col>
						<v-col
							v-else
							cols="6">
							<span>{{ localCase.assessment && localCase.assessment.market_value_override | bignum }}</span>
						</v-col>
					</v-row>
				</v-col>

				<v-col>
					<v-row>
						<v-col class="py-0">
							<b>Property Inventory</b>
						</v-col>
						<v-col v-if="this.isAdmin || this.isMember"
							class="py-0"
							cols="auto">
							<v-btn v-if="!isCaseEditable"
								small
								icon
								@click="isCaseEditable = !isCaseEditable">
								<v-icon>mdi-square-edit-outline</v-icon>
							</v-btn>
							<v-card-actions v-else
								class="pa-0">
								<v-btn
									color="success"
									small
									tile
									outlined
									icon
									@click="save">
									<v-icon small>mdi-check</v-icon>
								</v-btn>
								<v-btn
									color="error"
									small
									tile
									outlined
									icon
									@click="cancel">
									<v-icon small>mdi-close</v-icon>
								</v-btn>
							</v-card-actions>
						</v-col>
					</v-row>
					<v-row>
						<v-col>GLA</v-col>
						<v-col cols="2">{{ property.gla_sqft | bignum }}</v-col>
						<v-col>UNDER AIR GLA</v-col>
						<v-col cols="2">{{ property.under_air_gla_sqft | bignum }}</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col>LOT</v-col>
						<v-col cols="2">{{ property.lot_size | bignum }}</v-col>
						<v-col>TIME ADJ</v-col>
						<!-- TODO: Add model field -->
						<v-col cols="2"></v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col>GARAGE</v-col>
						<v-col cols="2">{{ property.garages | bignum }}</v-col>
						<v-col>POOL</v-col>
						<v-col cols="2">{{ property.pool | booleanFilter }}</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col>LOCATION ADJ</v-col>
						<!-- TODO: Add model field -->
						<v-col cols="2"></v-col>
						<v-col>FULL BATH</v-col>
						<v-col cols="2">{{ property.full_baths | bignum }}</v-col>
					</v-row>
					<v-divider></v-divider>
					<v-row>
						<v-col>COST OF SALE</v-col>
						<!-- TODO: Add model field -->
						<v-col cols="2"></v-col>
						<v-col>HALF BATH</v-col>
						<v-col cols="2">{{ property.half_baths | bignum }}</v-col>
					</v-row>
					<v-divider></v-divider>
				</v-col>
			</v-row>
		</v-form>
	</v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { clone } from 'lodash'

export default {
	props: {
		value: {
			type: Object,
			required: true,
		},
	},
	data: () => ({
		localCase: {},
		isCaseEditable: false,
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
			'isMember',
		]),
		...mapGetters('constants', [
			'constants',
		]),
		...mapGetters('paymentTypes', [
			'paymentTypes',
		]),
		...mapGetters('paymentStatuses', [
			'paymentStatuses',
		]),
		property() {
			return this.value?.property || {}
		},
	},
	methods: {
		...mapActions('paymentTypes', [
			'loadPaymentTypes',
		]),
		...mapActions('paymentStatuses', [
			'loadPaymentStatuses',
		]),
		save() {
			this.$emit('input', this.localCase)
			this.isCaseEditable = false
		},
		cancel() {
			this.localCase = clone(this.value)
			this.isCaseEditable = false
		},
	},
	mounted() {
		this.loadPaymentTypes()
		this.loadPaymentStatuses()
	},
	watch: {
		value: {
			deep: true,
			immediate: true,
			handler(newVal) {
				this.localCase = clone(newVal)
			},
		},
	},
}
</script>