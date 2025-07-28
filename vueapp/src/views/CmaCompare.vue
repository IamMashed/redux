<template>
	<div class="cma-compare-wrap">
		<v-card
			class="cma-compare-header"
			elevation="0"
			tile>
			<v-container>
				<v-row>
					<v-col>
						<h1 class="primary--text">Single CMA of {{ property.address }}</h1>

						<v-simple-table dense class="d-flex">
							<template #default>
								<tbody>
									<tr>
										<td>Good comps: {{ goodCompsCount }}</td>
									</tr>
									<tr>
										<td>All comps: {{ allCompsCount }}</td>
									</tr>
								</tbody>
							</template>
						</v-simple-table>
					</v-col>

					<v-simple-table class="col-6" dense>
						<template v-slot:default>
							<thead
								class="primary">
								<tr>
									<th></th>
									<th class="white--text">Assessment</th>
									<th class="white--text">Override</th>
									<th v-if="!isFL" class="white--text">Value</th>
									<th class="white--text">%</th>
									<th v-if="!isFL" class="white--text">MAX BY LAW</th>
								</tr>
							</thead>
							<tbody>
								<tr>
									<td>{{ assessment_date.assessment_name }} - Current</td>
									<td>{{ assessment_results.current_assessment_value | bignum }}</td>
									<td>
										<v-row>
											<v-col class="pa-0">
												<v-autonumeric
													v-model.number="assessment.override_value"
													:an-options="{
														decimalPlaces: 0,
													}"
													class="mt-0"
													style="font-size: 1em;"
													placeholder="0"
													single-line
													hide-details
													dense>
												</v-autonumeric>
											</v-col>
											<v-col cols="auto"
												class="pa-0">
												<v-btn
													v-if="isAdmin"
													color="primary"
													outlined
													class="ml-3"
													x-small
													icon
													@click="reloadSingleCMA(property, updated_comps_properties, ruleSet, assessment)">
													<v-icon small>mdi-check</v-icon>
												</v-btn>
											</v-col>
											<v-col cols="auto"
												class="pa-0">
												<v-btn
													v-if="isAdmin"
													color="primary"
													outlined
													class="ml-1"
													x-small
													icon
													@click="updateAssessment(assessment)">
													<v-icon small>mdi-database</v-icon>
												</v-btn>
											</v-col>
										</v-row>
									</td>
									<td v-if="!isFL">{{ assessment_results.current_market_value | currency }}</td>
									<td></td>
									<td v-if="!isFL"></td>
								</tr>
								<tr>
									<td>Proposed</td>
									<td>{{ Number(proposedAssessment) | bignum }}</td>
									<td></td>
									<td v-if="!isFL">{{ proposedMarketValue | currency }}</td>
									<td>{{ Number(((assessment_results.current_assessment_value - proposedAssessment)/assessment_results.current_assessment_value * 100).toFixed(2)) | percents }}</td>
									<td v-if="!isFL">25%</td>
								</tr>
								<tr>
									<td>Difference</td>
									<td>
										{{ assessment_results.current_assessment_value - proposedAssessment | bignum }}
									</td>
									<td>
										<span v-if="assessment.override_value">
											{{ assessment.override_value - proposedAssessment | bignum }}
										</span>
									</td>
									<td v-if="!isFL">{{ assessment_results.current_market_value - proposedMarketValue | currency }}</td>
									<td></td>
									<td v-if="!isFL">{{ assessment_results.current_assessment_value && (assessment_results.current_assessment_value * 0.25) | bignum }}</td>
								</tr>
								<!-- <tr v-if="isFL">
									<td>All Avg 1-4</td>
									<td>{{ average_ranges.misc && $options.filters.bignum(Number(average_ranges.misc['4'].claimed_market_value.toFixed(0))) }}</td>
									<td></td>
									<td></td>
									<td></td>
									<td></td>
								</tr> -->
								<tr v-if="isFL">
									<td>Good Avg 1-4</td>
									<td>{{ average_ranges.good['4'].claimed_market_value && $options.filters.bignum(Number(average_ranges.good['4'].claimed_market_value.toFixed(0))) }}</td>
									<td></td>
									<td></td>
									<td></td>
									<td v-if="!isFL"></td>
								</tr>
							</tbody>
						</template>
					</v-simple-table>
				</v-row>
			</v-container>
			<v-divider></v-divider>
		</v-card>

		<v-container>
		<v-card-actions class="d-print-none">

			<v-btn
				color="primary"
				outlined
				@click="reloadSingleCMA(property, updated_comps_properties, ruleSet, assessment)">
				<v-icon left>mdi-reload</v-icon>
				Re-run CMA
			</v-btn>

			<v-btn
				color="primary"
				outlined
				@click="printGoodPadReport">
				Good/Bad Report
			</v-btn>
			<v-btn
				v-if="property.county === 'suffolk'"
				color="primary"
				outlined
				@click="printGoodBadReportExtended">
				Full G/B Report
			</v-btn>

			<a-pdf-maker
				ref="goodBadReport"
				:content="pdfContent"
				:styles="pdfStyles"
				:default-style="{
					fontSize: 8,
					lineHeight: 1.5,
				}"
				:file-name="pdfFileName"
				:page-size="isFL ? 'A4' : 'LEGAL'"
				class="v-btn pa-0"
				hide-content>
			</a-pdf-maker>

			<v-btn
				color="secondary"
				outlined
				@click="print">
				<v-icon left>mdi-printer</v-icon>
				Print
			</v-btn>

			<v-btn
				color="secondary"
				outlined
				@click="$refs.cmaSettings.show()">
				<v-icon left>
					mdi-cog
				</v-icon>
				Settings
			</v-btn>

			<!-- <v-btn
				color="secondary"
				outlined
				:href="`${VUE_APP_API}generate-pdf?apn=${property.apn}&county=${property.county}&tax_year=${assessment.assessment_date && assessment.assessment_date.tax_year}`"
				target="_blank">
				<v-icon left>
					mdi-file-pdf
				</v-icon>
				Generate Application PDF
			</v-btn> -->

			<v-btn
				color="secondary"
				outlined
				:loading="loadingWorkup"
				@click="createCMAWorkup">
				<v-icon left>
					mdi-content-save
				</v-icon>
				Save Workup
			</v-btn>

			<v-btn
				color="secondary"
				outlined
				@click="unselectAllComps">
				Unselect All
			</v-btn>

			<a-pdf-maker
				ref="cmaPDF"
				:content="printPdfContent"
				:styles="pdfStyles"
				:default-style="{
					fontSize: 10,
					lineHeight: 1.5,
				}"
				:file-name="printPdfFileName"
				:page-size="isFL ? 'A4' : 'LEGAL'"
				page-orientation="landscape"
				hide-content>
			</a-pdf-maker>

			<v-spacer></v-spacer>

			<cma-log
				:rules="log_rules"
				:comps="log_comps"
				:loading="loadingLog"
				@load-data="loadCmaLog"
				@plot="showLogComps"
				@fly-to="flyToComp">
			</cma-log>

		</v-card-actions>

		<v-row v-if="cmaNotification">
			<v-col
				cols="12"
				md="6"
				offset-md="3">
				<cma-notification
					:notification="cmaNotification">
				</cma-notification>
			</v-col>
		</v-row>

		<v-row class="flex-nowrap">
			<v-col cols="3"
				v-if="filters"
				class="primary lighten-4 mt-3">
			</v-col>

			<!-- <v-col cols="auto"
				class="pa-0 mt-3"
				style="z-index: 2;">
				<v-btn
					color="primary lighten-4"
					class="pa-0 black--text"
					min-width="30"
					min-height="48"
					depressed
					tile
					small
					@click="filters = !filters"
					style="position: absolute;">
					<v-icon x-small>{{ filters ? `mdi-close` : `mdi-cog` }}</v-icon>
				</v-btn>
			</v-col> -->

			<v-col cols="12">
				<v-tabs v-model="tab"
					class="pl-3">
					<v-tab class="d-print-none">
						CMA
					</v-tab>
					<v-tab class="d-print-none">
						Map
					</v-tab>

					<v-tabs-items v-model="tab">
					<v-tab-item>
						<div class="d-none d-print-block">
							<h3 class="text-center white-space-pre">{{ settings.settings && settings.settings.pdf_header }}</h3>
						</div>
						
						<a-comparison-table
									:items="[
										property,
										...selected_comps_properties,
									]"
									:fields="fields"
									:locked="loading"
									:locked-items="lockedComps"
									:item-class="(item) => {
										return item.status === 'bad' ? 'bad-comparison-table-cell red--text' : ''
									}"
									:cell-class="highlightedClass"
									class="my-5"
									ref="cmaTable"
									@update="updateComp"
									@context="highlightField">

									<!-- <template #title="{ index}">
										{{ index ? `Comparable #${index}` : 'Subject' }}
									</template> -->

									<template #r_type="{ item, value, editItem, index }">
										<v-row class="align-center">
											<v-col cols="8"
												class="text-center">
												{{ item.r_type === 'SBJ' ? 'Subject' : `Comparable #${index} (${item.r_type})` }}
											</v-col>
											<v-col cols="2"
												class="text-right">
												<v-btn
													color="amber"
													icon
													@click="editItem(item)">
													<v-icon
														small>
														mdi-pencil
													</v-icon>
												</v-btn>
											</v-col>
											<v-col cols="2"
												class="text-right">
												<v-btn
													color="error"
													icon
													@click="selectComp(item.id, false)">
													<v-icon
														small>
														mdi-close
													</v-icon>
												</v-btn>
											</v-col>
										</v-row>
									</template>

									<template #comparables="{ item }">
										<v-row>
											<v-col
												cols="4"
												class="text-center">
												Sec
											</v-col>
											<v-col
												cols="4"
												class="text-center">
												Block
											</v-col>
											<v-col
												cols="4"
												class="text-center">
												Lot
											</v-col>
										</v-row>
										<v-row>
											<v-col
												cols="4"
												class="text-center"
												:class="{
													'yellow': item.section === property.section && item.block === property.block
												}">
												{{ item.section }}
											</v-col>
											<v-col
												cols="4"
												class="text-center"
												:class="{
													'yellow': item.section === property.section && item.block === property.block
												}">
												{{ item.block }}
											</v-col>
											<v-col
												cols="4"
												class="text-center">
												{{ item.lot }}
											</v-col>
										</v-row>
									</template>

									<template #photos="{ value, item }">
										<div class="d-flex justify-center">
											<v-img
												:src="findByKey(value, (item) => item.is_best === true).url || require('@/assets/images/no_photo.png')"
												lazy-src="@/assets/images/no_photo.png"
												height="130"
												max-width="200"
												class="cursor-pointer"
												@click="showPhotoGallery(value, item)">
											</v-img>
										</div>
									</template>

									<template #address="{ item, value }">
										<span :class="{ 'yellow d-flex align-center comparison-table-cell__content': item.street === property.street }">{{ value }}</span>
									</template>

									<template #proximity="{ item }">
										{{ item.proximity | miles }}
									</template>

									<template #property_class="{ item }">
										{{ item.property_class_description }} ({{ item.class }})
									</template>

									<template #water_category="{ value }">
										({{ value }}) {{ value | mapperFilter(constants.water_category_map) }}
									</template>

									<template #land_tag="{ value }">
										({{ value }}) {{ value | mapperFilter(constants.land_tag_map) }}
									</template>

									<template #owners="{ value }">
										{{ value | lastOwners }}
									</template>

									<template #description="{ item }">
										<v-row class="flex-nowrap">
											<v-col
												:cols="item.r_type === 'SBJ' ? 12 : 6"
												class="text-center">
												Description
											</v-col>
											<v-col
												v-if="item.r_type !== 'SBJ'"
												cols="6"
												class="text-center">
												+/- Adj
											</v-col>
										</v-row>
									</template>

									<template #adjustments.GLA.title="{ value }">
										{{ value }} (sqft)
									</template>

									<template #adjustments.LOT.title="{ value }">
										{{ value }} (acres)
									</template>

									<!-- Iterate adjustments list and show slots -->
									<template
										v-for="adj in adjustmentsList"
										v-slot:[`adjustments.${adj}.row`]="{ row }">
										<tr :key="adj.key">
											<td class="text-uppercase">
												{{ transAdjustments[row.text] && transAdjustments[row.text].name }}
											</td>
											<td v-for="(cell, i) in row.cells" :key="`${i}`"
												class="comparison-table-cell"
												:class="[
													cell.item.status === 'bad' ? 'bad-comparison-table-cell lighten-4 red--text' : row.class,
													highlightedClass(cell.item, row.value),
												]"
												@contextmenu.prevent="highlightField(cell.item, row.value)">
												<v-row
													class="flex-nowrap">
													<v-col
														cols="6"
														class="text-uppercase">
														<span v-if="row.render">
															{{ row.render(cell.value, cell.item) }}
														</span>
														<!-- If mapper is constants is present -->
														<span v-else-if="constants[`${row.text.toLowerCase()}_type_map`]">
															{{ cell.item[transAdjustments[row.text] && transAdjustments[row.text].property_field] | mapperFilter(constants[`${row.text.toLowerCase()}_type_map`]) | bignum }}
														</span>
														<span v-else>
															{{ cell.value && cell.value.comp_value || '-' }}
														</span>
													</v-col>
													<v-divider vertical></v-divider>
													<v-col
														cols="6"
														class="text-right">
														<!-- <v-tooltip v-if="cell.value"
															top>
															<template #activator="{ on }">
																<span
																	v-on="on">
																	{{ cell.value.value | currency }}
																</span>
															</template>
															<span>{{ cell.value.rule_value }}</span>
														</v-tooltip> -->
														<span v-if="cell.value">
															{{ cell.value.value | currency }}
														</span>
													</v-col>
												</v-row>
											</td>
										</tr>
									</template>

									<template #adjustments.LOT.row="{ row }">
										<tr>
											<td class="text-uppercase">
												{{ transAdjustments[row.text] && transAdjustments[row.text].name }}
											</td>
											<td v-for="(cell, i) in row.cells" :key="`${i}`"
												class="comparison-table-cell"
												:class="[
													cell.item.status === 'bad' ? 'bad-comparison-table-cell lighten-4 red--text' : row.class,
													highlightedClass(cell.item, row.value),
												]"
												@contextmenu.prevent="highlightField(cell.item, row.value)">
												<v-row
													class="flex-nowrap">
													<v-col
														cols="6">
														{{ cell.item[transAdjustments[row.text] && transAdjustments[row.text].property_field] | mapperFilter(constants[`${row.text.toLowerCase()}_type_map`]) | bignum }}
														<span v-if="cell.item.lot_size_sqft">/{{ cell.item.lot_size_sqft | bignum }}</span>
													</v-col>
													<v-divider vertical></v-divider>
													<v-col
														cols="6"
														class="text-right">
														<span v-if="cell.value">
															{{ cell.value.value | currency }}
														</span>
													</v-col>
												</v-row>
											</td>
										</tr>
									</template>

									<template #adjustments.POOL.row="{ row }">
										<tr>
											<td class="text-uppercase">
												{{ transAdjustments[row.text] && transAdjustments[row.text].name }}
											</td>
											<td v-for="(cell, i) in row.cells" :key="`${i}`"
												class="comparison-table-cell"
												:class="[
													cell.item.status === 'bad' ? 'bad-comparison-table-cell lighten-4 red--text' : row.class,
													highlightedClass(cell.item, row.value),
												]"
												@contextmenu.prevent="highlightField(cell.item, row.value)">
												<v-row
													class="flex-nowrap">
													<v-col
														cols="6">
														{{ cell.value && cell.value.comp_value | booleanFilter }}
													</v-col>
													<v-divider vertical></v-divider>
													<v-col
														cols="6"
														class="text-right">
														<!-- <v-tooltip v-if="cell.value"
															top>
															<template #activator="{ on }">
																<span
																	v-on="on">
																	{{ cell.value.value | currency }}
																</span>
															</template>
															<span>{{ cell.value.rule_value }}</span>
														</v-tooltip> -->
														<span v-if="cell.value">
															{{ cell.value.value | currency }}
														</span>
													</v-col>
												</v-row>
											</td>
										</tr>
									</template>

									<template #adjustments.TIME_ADJ.row="{ row }">
										<tr>
											<td class="text-uppercase">
												{{ transAdjustments[row.text] && transAdjustments[row.text].name }}
											</td>
											<td v-for="(cell, i) in row.cells" :key="`${i}`"
												class="comparison-table-cell"
												:class="[
													cell.item.status === 'bad' ? 'bad-comparison-table-cell lighten-4 red--text' : row.class,
													highlightedClass(cell.item, row.value),
												]"
												@contextmenu.prevent="highlightField(cell.item, row.value)">
												<v-row
													class="flex-nowrap">
													<v-col
														cols="6">
														{{ cell.value && cell.value.comp_value | date }}
													</v-col>
													<v-divider vertical></v-divider>
													<v-col
														cols="6"
														class="text-right">
														<!-- <v-tooltip v-if="cell.value"
															top>
															<template #activator="{ on }">
																<span
																	v-on="on">
																	{{ cell.value.value | currency }}
																</span>
															</template>
															<span>{{ cell.value.rule_value }}</span>
														</v-tooltip> -->
														<span v-if="cell.value">
															{{ cell.value.value | currency }}
														</span>
													</v-col>
												</v-row>
											</td>
										</tr>
									</template>

									<template #adjustments.LOCATION.row="{ row }">
										<tr>
											<td class="text-uppercase">
												{{ transAdjustments[row.text] && transAdjustments[row.text].name }}
											</td>
											<td v-for="(cell, i) in row.cells" :key="`${i}`"
												class="comparison-table-cell"
												:class="[
													cell.item.status === 'bad' ? 'bad-comparison-table-cell lighten-4 red--text' : row.class,
													highlightedClass(cell.item, row.value),
												]"
												@contextmenu.prevent="highlightField(cell.item, row.value)">
												<v-row
													class="flex-nowrap">
													<v-col
														cols="6"
														class="text-uppercase">
														<!-- {{ Number(cell.item.adjustments.LOCATION && cell.item.adjustments.LOCATION.comp_value) | mapperFilter(obsolescences, (v) => v ? v.rule_name : '-') }} -->
														<span v-if="cell.value.comp_value">
															({{ cell.value.comp_value }})
														</span>
														{{ Number(cell.value && cell.value.comp_value) | mapperFilter(obsolescences, (v) => v ? v.rule_name : '-') }}
														({{ cell.value && cell.value.rule_value }})
													</v-col>
													<v-divider vertical></v-divider>
													<v-col
														cols="6"
														class="text-right">
														<!-- <v-tooltip v-if="cell.value"
															top>
															<template #activator="{ on }">
																<span
																	v-on="on">
																	{{ cell.value.value | currency }}
																</span>
															</template>
															<span>{{ cell.value.rule_value }}</span>
														</v-tooltip> -->
														<span v-if="cell.value">
															{{ cell.value.value | currency }}
														</span>
													</v-col>
												</v-row>
												<!-- <template v-if="cell.item.obso_result">
													<v-row v-for="(obs, key) in cell.item.obso_result.comp_obsolescences"
														:key="key"
														class="flex-nowrap">
														<v-col
															cols="6"
															class="text-uppercase">
															{{ obs.obs_name }} ({{ Number(obs.value) | percents }})
														</v-col>
														<v-divider vertical></v-divider>
														<v-col
															cols="6"
															class="text-right">
															{{ obs.price_change | currency }}
														</v-col>
													</v-row>
												</template> -->
											</td>
										</tr>
									</template>

									<template #adjustments.WATER.row="{ row }">
										<tr>
											<td class="text-uppercase">
												{{ transAdjustments[row.text] && transAdjustments[row.text].name }}
											</td>
											<td v-for="(cell, i) in row.cells" :key="`${i}`"
												class="comparison-table-cell"
												:class="[
													cell.item.status === 'bad' ? 'bad-comparison-table-cell lighten-4 red--text' : row.class,
													highlightedClass(cell.item, row.value),
												]"
												@contextmenu.prevent="highlightField(cell.item, row.value)">
												<v-row
													class="flex-nowrap">
													<v-col
														cols="6"
														class="text-uppercase">
														{{ cell.value && cell.value.comp_value ? 'YES' : 'NO' }}
														({{ (cell.value && cell.value.comp_percent_value) || 0 }}%)
													</v-col>
													<v-divider vertical></v-divider>
													<v-col
														cols="6"
														class="text-right">
														<span v-if="cell.value">
															{{ cell.value.value | currency }}
														</span>
													</v-col>
												</v-row>
											</td>
										</tr>
									</template>

									<template #gross_adjustments="{ item: { adjustments } }">
										<v-row class="flex-nowrap">
											<v-col cols="6">
											</v-col>
											<v-divider vertical></v-divider>
											<v-col cols="6"
												class="text-right">
												{{ Object.values(adjustments).reduce((a, { value }) => a + Math.abs(value), 0) || '' | currency }}
											</v-col>
										</v-row>
									</template>

									<template #other_adjustment="{ item }">
										<v-row class="flex-nowrap">
											<v-col cols="6">
												{{ item.other_adjustment_description }}
											</v-col>
											<v-divider vertical></v-divider>
											<v-col cols="6"
												class="text-right">
												{{ item.other_adjustment | currency }}
											</v-col>
										</v-row>
									</template>

									<template #adjustment_delta_value="{ value }">
										<v-row class="flex-nowrap">
											<v-col cols="6">
											</v-col>
											<v-divider vertical></v-divider>
											<v-col cols="6"
											class="text-right">
												{{ value | currency }}
											</v-col>
										</v-row>
									</template>

									<template #adjusted_market_value="{ value }">
										<v-row class="flex-nowrap">
											<v-col cols="6">
											</v-col>
											<v-divider vertical></v-divider>
											<v-col cols="6"
											class="text-right">
												{{ value | currency }}
											</v-col>
										</v-row>
									</template>

									<template #adjustments.COST_OF_SALE.value="{
										value,
										item: {
											r_type,
											adjustments,
										},
									}">
										<span v-if="r_type === 'SBJ'">
											Per F.S. 193.011(1),(8) and form DR-493
										</span>
										<v-row v-else
											class="flex-nowrap">
											<v-col cols="6">
											</v-col>
											<v-divider vertical></v-divider>
											<v-col cols="6"
												class="text-right">
												{{ adjustments.COST_OF_SALE && adjustments.COST_OF_SALE.value | currency }}
											</v-col>
										</v-row>
									</template>

									<template #cos_adjusted_sale="{
										item: {
											r_type,
											adjustments,
											adjusted_market_value,
										},
									}">
										<v-row v-if="r_type !== 'SBJ'"
											class="flex-nowrap">
											<v-col cols="6">
											</v-col>
											<v-divider vertical></v-divider>
											<v-col cols="6"
												class="text-right">
												{{ (adjusted_market_value + (adjustments.COST_OF_SALE && adjustments.COST_OF_SALE.value)) | currency }}
											</v-col>
										</v-row>
									</template>

									<template #form="{ editedItem }">
										<property-form
											:item.sync="editedItem"
											:fields="adjustmentsList">
										</property-form>
									</template>

									<template #form-actions="{ cancel, submit, editedItem }">
										<v-spacer></v-spacer>

										<v-btn
											text
											color="grey"
											class="text-none"
											@click="cancel">
											Cancel
										</v-btn>

										<v-btn
											text
											class="text-none v-btn--filled"
											color="success"
											@click="submit">
											Submit
										</v-btn>

										<v-btn
											v-if="isAdmin"
											text
											class="text-none v-btn--filled"
											color="error"
											@click="updateProperty(editedItem)">
											Override Database
										</v-btn>
									</template>

						</a-comparison-table>

						<v-row>
							<v-col
								md="8"
								offset-md="4">
								<v-textarea
									v-model="printFieldTop"
									rows="2"
									class="mb-2 red--text"
									hide-details
									outlined
									dense>
								</v-textarea>
								<v-textarea
									v-if="!isFL"
									v-model="printFieldBottom"
									rows="2"
									class="red--text"
									hide-details
									outlined
									dense>
								</v-textarea>
							</v-col>
						</v-row>
					</v-tab-item>
					<v-tab-item>
						<a-map
							ref="map"
							:style-id="mapStyle.value"
							:center="mapCenter"
							:width="mapWidth"
							:height="mapHeight">
							<template>
								<v-card class="map-controls ma-2">
									<v-expansion-panels>
										<v-expansion-panel>
											<v-expansion-panel-header>
												<h4>Options</h4>
											</v-expansion-panel-header>
											<v-expansion-panel-content>
												<v-radio-group v-model="mapStyle"
													class="mt-0">
													<v-radio
														v-for="(style, key) in mapStyles"
														:key="key"
														:label="style.text"
														:value="style">
													</v-radio>
												</v-radio-group>
												<v-select
													v-model="mapCompFilter"
													:items="mapCompFilters"
													label="Comp status"
													return-object
													dense>
												</v-select>
												<v-switch v-model="isShowTaxLayer"
													label="Parcels"
													hide-details
													inset
													dense>
												</v-switch>
												<v-switch v-model="isShowLogComps"
													label="Log Comps"
													inset
													dense>
												</v-switch>
											</v-expansion-panel-content>
										</v-expansion-panel>
									</v-expansion-panels>
								</v-card>
							</template>
							<!-- <a-map-layer
								v-for="(r, key) in subjectRadiuses"
								:key="key"
								:layer="r">
							</a-map-layer> -->

							<a-map-layer
								:layer="taxLayer">
							</a-map-layer>

							<a-map-layer
								:layer="taxLineLayer">
							</a-map-layer>

							<a-map-layer
								v-if="mapRoadsLayer.sourceLayer"
								:layer="roadsLayer">
							</a-map-layer>

							<a-map-layer
								:layer="obsFeatures"
								@click="showObsMapPopup">
							</a-map-layer>

							<a-map-layer
								:layer="obsLineFeatures"
								@click="showObsMapPopup">
							</a-map-layer>

							<a-map-layer
								ref="compFeaturesLayer"
								:layer="compFeatures"
								:cluster-layer="compFeaturesClusters"
								@cluster-layer-loaded="clusterLayerLoaded"
								@click="showMapPopup">
							</a-map-layer>
						</a-map>
					</v-tab-item>
					</v-tabs-items>
				</v-tabs>
			</v-col>
		</v-row>

		<v-data-table
			:items="tableComps"
			:headers="selectedTableCompsHeaders"
			fixed-header
			height="27vh"
			id="comp-selection-table"
			class="mt-5 d-print-none fixed-row-table overscroll-none"
			:items-per-page="-1"
			:custom-sort="sortCompsTable"
			hide-default-footer
			dense>

			<template #top>
				<v-dialog
					v-model="tableCompsSettingsDialog"
					max-width="500">

					<v-card>
						<v-toolbar
							elevation="0">
							<v-toolbar-title>Table Settings</v-toolbar-title>
							<v-spacer></v-spacer>
							<v-btn
								icon
								@click="tableCompsSettingsDialog = false">
								<v-icon>mdi-close</v-icon>
							</v-btn>
						</v-toolbar>
						<v-container>
							<v-btn
								color="error"
								outlined
								x-small
								@click="resetTableCompsHeader">
								Reset to default
							</v-btn>
							<v-list >

								<draggable
									:list="tableCompsHeaders"
									tag="v-list-item-group">
									<template v-for="item in tableCompsHeaders">
										<v-list-item
											v-if="item"
											:key="item.value"
											:class="{ 'v-item--active v-list-item--active primary--text': item.show }"
											class="v-item--border-bottom cursor-grab"
											dense>
											<v-list-item-content>
												<v-list-item-title v-text="item.text"></v-list-item-title>
											</v-list-item-content>

											<v-list-item-action
												class="ma-0">
												<v-checkbox
													v-if="item"
													v-model="item.show"
													hide-details
													class="ma-0 pa-0"
													dense>
												</v-checkbox>
											</v-list-item-action>
										</v-list-item>
									</template>
								</draggable>
							</v-list>

						</v-container>
					</v-card>
				</v-dialog>
			</template>

			<template #header.settings>
				<v-btn
					class="white--text"
					text
					x-small
					icon
					@click="tableCompsSettingsDialog = true">
					<v-icon small>mdi-cog</v-icon>
				</v-btn>
			</template>

			<template #item.selected="{ item }">
				<div :id="`comp-${item.id}`">
					<v-checkbox
						:value="item.selected"
						@change="(e) => selectComp(item.id, e)"
						dense
						hide-details
						class="ma-1 pa-0">
					</v-checkbox>
				</div>
			</template>

			<template #item.r_type="{ item, value }">
				<a @click="flyToComp(item.id)">
					{{ value }}
				</a>
			</template>

			<template #item.photos="{ value, item }">
				<v-img
					:src="findByKey(item.photos, (item) => item.is_best === true).url"
					lazy-src="@/assets/images/no_photo.png"
					max-height="33"
					max-width="45"
					class="cursor-pointer"
					@click="showPhotoGallery(value, item)">
				</v-img>
			</template>

			<template #item.proximity="{ value }">
				{{ value | miles }}
			</template>

			<template #item.adjusted_market_value="{ value, item }">
				<span v-if="isFL && item.adjustments && item.adjustments.COST_OF_SALE">
					{{ Number(value + item.adjustments.COST_OF_SALE.value) || value | currency }}
				</span>
				<span v-else>
					{{ value | currency }}
				</span>
			</template>

		</v-data-table>

		<a-photo-gallery
			:photos="galleryPhotos"
			ref="gallery"
			@upload-photo="uploadPhoto"
			@update-photo="updatePhoto"
			@delete-photo="deletePhoto">
		</a-photo-gallery>

		<v-overlay :value="loading">
			<v-progress-circular
				:size="70"
				:width="7"
				color="primary"
				indeterminate>
			</v-progress-circular>
		</v-overlay>

		</v-container>

		<cma-settings
			ref="cmaSettings"
			:rule-set.sync="ruleSet"
			:assessment-date-id.sync="assessment_date_id"
			:assessment-dates="countyAssessmentDates"
			:assessment-ratio="assessment_results.assessment_ratio"
			:settings.sync="settings"
			@close="reloadSingleCMA(property, updated_comps_properties, ruleSet, assessment)">
		</cma-settings>

		<confirm ref="confirm"></confirm>

		<cma-print-dialog
			ref="cmaPrintDialog"
			v-model="printPdfFileNameField">
		</cma-print-dialog>

	</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../api/apiFactory'
import { keyBy, resolve } from '../utils'
import { filter, cloneDeep, uniqBy, uniqWith, isEqual } from 'lodash'
import { format } from 'date-fns'
import mapboxgl from 'mapbox-gl/dist/mapbox-gl'
import axios from 'axios'
import Vue from 'vue'
import countyFilter from '../mixins/countyFilter'

import CmaReportService from '../services/pdf/CmaReport.service'
import MapboxApiService from '../services/pdf/MapboxApi.service'
import GoodBadReportService from '../services/pdf/GoodBadReport.service'
import GoodBadReportExtended from '../services/pdf/GoodBadReportExtended'

import AComparisonTable from '../components/AComparisonTable'
import PropertyForm from '../components/Forms/PropertyForm'
import CmaSettings from '../components/CMA/CMASettings'
import CmaLog from '../components/CMA/CMALog'
import CmaNotification from '../components/CMA/CMANotification'
import CmaPrintDialog from '../components/CMA/CMAPrintDialog'
import APdfMaker from '../components/APdfMaker'
import AMap from '../components/AMap'
import AMapLayer from '../components/AMapLayer'
import AMapPopup from '../components/AMapPopup.vue'
import AMapLogPopup from '../components/AMapLogPopup.vue'
import AMapObsPopup from '../components/AMapObsPopup.vue'
import APhotoGallery from '../components/APhotoGallery'
import Confirm from '../components/Confirm'
import Draggable from 'vuedraggable'

import Comp from '../models/Comp'
import AssessmentResult from '../models/AssessmentResult'

import noPhoto from '@/assets/images/no_photo.png'
import assessmentsApi from '../api/assessmentsApi'

const singleCmaApi = apiFactory.get('single-cma')
const globalSettingsApi = apiFactory.get('global-settings')
const propertiesApi = apiFactory.get('properties')
const propertiesPhotosApi = apiFactory.get('properties-photos')
const assessmentDatesApi = apiFactory.get('assessment-dates')
const singleCmaWorkupsApi = apiFactory.get('single-cma-workups')

export default {
	components: {
		AComparisonTable,
		PropertyForm,
		CmaSettings,
		CmaLog,
		CmaNotification,
		CmaPrintDialog,
		APdfMaker,
		AMap,
		AMapLayer,
		APhotoGallery,
		Confirm,
		Draggable,
	},
	props: {
		id: {
			required: true,
		},
		assessmentDateId: {
			type: Number,
			required: false,
			default: null,
		},
	},
	mixins: [
		countyFilter,
	],
	filters: {
		booleanFilter: (v) => {
			return v === 'True' ? 'YES' : 'NO'
		},
	},
	data: () => ({
		VUE_APP_API: process.env.VUE_APP_API,
		AMapPopup: Vue.extend(AMapPopup),
		AMapLogPopup: Vue.extend(AMapLogPopup),
		AMapObsPopup: Vue.extend(AMapObsPopup),
		loading: true,
		loadingWorkup: false,
		loadingLog: false,
		property: {},
		comps: [],
		nearbyComps: [],
		updatedCompIds: [],
		assessment_results: {},
		average_ranges: {},
		log_rules: [],
		log_comps: [],
		pdfStyles: {
			title: {
				fontSize: 11,
				bold: true,
				decoration: 'underline',
				alignment: 'center',
			},
			subtitle: {
				bold: true,
				decoration: 'underline',
				alignment: 'center',
			},
			tableTitle: {
				fontSize: 10,
				bold: true,
				alignment: 'center',
			},
			tableText: {
				lineHeight: 1,
				alignment: 'center',
			},
			cmaTableTitle: {
				fontSize: 14,
				lineHeight: 1,
				bold: true,
				alignment: 'center',
			},
			cmaTableText: {
				lineHeight: 1,
				alignment: 'left',
			},
			printFieldText: {
				fontSize: 14,
				lineHeight: 1,
				bold: true,
			},
		},
		pdfFileName: 'Good/Bad.pdf',
		mapStyle: {
			text: 'Satellite',
			value: 'redux1/ck7tqt0yy03sb1ipekp8z2a6d',
		},
		mapStyles: [
			{
				text: 'Street',
				value: 'redux1/ck7trjlhr071w1imiu00gffuu/draft', // mapbox://styles/redux1/ck7trjlhr071w1imiu00gffuu/draft
			},
			{
				text: 'Satellite',
				value: 'redux1/ck7tqt0yy03sb1ipekp8z2a6d', // mapbox://styles/redux1/ck7tqt0yy03sb1ipekp8z2a6d
			},
		],
		mapCompFilters: [
			{
				text: 'All',
				value: null,
			},
			{
				text: 'Only Selected',
				value: {
					selected: true,
				},
			},
			{
				text: 'Good',
				value: {
					status: 'good'
				},
			},
			{
				text: 'Bad',
				value: {
					status: 'bad'
				},
			},
		],
		mapCompFilter: {
			text: 'All',
			value: null,
			// text: 'Good (initial)',
			// value: ({ status, selected}) => {
			// 	return status === 'good' || selected
			// },
		},
		mapTaxLayers: [
			{
				county: 'broward',
				layer: {
					source: 'redux1.2h0xp3m8',
					sourceLayer: 'broward',
					color: '#1c77ac',
				},
			},
			{
				county: 'miamidade',
				layer: {
					source: 'redux1.9i3ly7fx',
					sourceLayer: 'miamidade-38lfvt',
					color: '#1c77ac',
				},
			},
			{
				county: 'nassau',
				layer: {
					source: 'redux1.6wzefil1',
					sourceLayer: 'nassau_v2-czwspg',
					color: '#1c77ac',
				},
			},
			{
				county: 'palmbeach',
				layer: {
					source: 'redux1.b1eyhjoa',
					sourceLayer: 'palmbeach-apjj98',
					color: '#1c77ac',
				},
			},
			{
				county: 'suffolk',
				layer: {
					source: 'redux1.83sm6s9y',
					sourceLayer: 'suffolk_full-dpr3tc',
					color: '#1c77ac',
				},
			},
		],
		mapRoadsLayers: [
			{
				county: 'broward',
				layer: {
					source: '',
					sourceLayer: '',
				},
			},
			{
				county: 'miamidade',
				layer: {
					source: '',
					sourceLayer: '',
				},
			},
			{
				county: 'nassau',
				layer: {
					source: 'redux1.6zq0qosm',
					sourceLayer: 'nassau_ways-a2w3ul',
				},
			},
			{
				county: 'palmbeach',
				layer: {
					source: '',
					sourceLayer: '',
				},
			},
			{
				county: 'suffolk',
				layer: {
					source: '',
					sourceLayer: '',
				},
			},
		],
		mapWidth: '100%',
		mapHeight: '62vh',
		// Promise resolve function
		// mapInited: null,
		isShowTaxLayer: false,
		settings: {},
		assessmentCut: 450000, // max current assessed market to show 25% law reduction
		printFieldTop: '',
		printFieldBottom: '',
		innerTableLayout: {
			hLineWidth: () => 1,
			vLineWidth: () => 1,
			hLineColor: () => 'black',
			vLineColor: () => 'black',
			paddingLeft: () => 0,
			paddingRight: () => 0,
			paddingTop: () => 0,
			paddingBottom: () => 0,
		},
		pdfContent: [],
		printPdfContent: [],
		printPdfFileNameField: 'address',
		galleryPhotos: [],
		galleryProperty: {},
		assessmentDates: [],
		filters: false,
		ruleSet: {},
		assessment_date_id: null,
		assessment: {},
		// cmaConfig: {
		// 	: null,
		// 	sale_date_to: '',
		// 	sale_date_from: '',
		// },
		defaultTableCompsHeaders: [
			{
				text: '',
				value: 'selected',
				class: 'secondary white--text',
				show: true,
				sortable: false,
			},
			{
				text: 'R_TYPE',
				value: 'r_type',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'PHOTOS',
				value: 'photos',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'RADIUS_MIL',
				value: 'proximity',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'L_SF',
				value: 'gla_sqft_formatted',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'STYLE',
				value: 'style',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'BUILT',
				value: 'age',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'ADJ_VALUE',
				value: 'adjusted_market_value',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'NUMBER',
				value: 'number',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'ST_NAME',
				value: 'street',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'SALE_PRICE',
				value: 'last_sale_price_formatted',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'SALE_DATE',
				value: 'last_sale_date_formatted',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'CLASS',
				value: 'class',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'TOWN',
				value: 'town',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'ROOMS',
				value: 'rooms',
				class: 'secondary white--text',
			},
			{
				text: 'BUILDING_CODE',
				value: 'building_code',
				class: 'secondary white--text',
			},
			{
				text: 'VILLAGE',
				value: 'village',
				class: 'secondary white--text',
			},
			{
				text: 'LOT',
				value: 'lot',
				class: 'secondary white--text',
			},
			{
				text: 'ID',
				value: 'id',
				class: 'secondary white--text',
			},
			{
				text: 'GARAGE_TYPE',
				value: 'garage_type',
				class: 'secondary white--text',
			},
			{
				text: 'WATERFRONT',
				value: 'waterfront',
				class: 'secondary white--text',
			},
			{
				text: 'KITCHENS',
				value: 'kitchens',
				class: 'secondary white--text',
			},
			{
				text: 'STATE',
				value: 'state',
				class: 'secondary white--text',
			},
			{
				text: 'SELLER',
				value: 'seller_full_name',
				class: 'secondary white--text',
			},
			{
				text: 'LOT_SIZE',
				value: 'lot_size',
				class: 'secondary white--text',
			},
			{
				text: 'SUBDIVISION',
				value: 'subdivision',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'ADDRESS',
				value: 'address',
				class: 'secondary white--text',
			},
			{
				text: 'FIREPLACES',
				value: 'fireplaces',
				class: 'secondary white--text',
			},
			{
				text: 'PAVING_TYPE',
				value: 'paving_type',
				class: 'secondary white--text',
			},
			{
				text: 'PATIO_TYPE',
				value: 'patio_type',
				class: 'secondary white--text',
			},
			{
				text: 'IS_LISTED',
				value: 'is_listed',
				class: 'secondary white--text',
			},
			{
				text: 'CONDITION',
				value: 'condition',
				class: 'secondary white--text',
			},
			{
				text: 'IS_CONDO',
				value: 'is_condo',
				class: 'secondary white--text',
			},
			{
				text: 'ADJ_DELTA_VALUE',
				value: 'adjustment_delta_value',
				class: 'secondary white--text',
			},
			{
				text: 'SECTION',
				value: 'section',
				class: 'secondary white--text',
			},
			{
				text: 'BASEMENT_TYPE',
				value: 'basement_type',
				class: 'secondary white--text',
			},
			{
				text: 'PORCH_TYPE',
				value: 'porch_type',
				class: 'secondary white--text',
			},
			{
				text: 'LOCATION',
				value: 'location',
				class: 'secondary white--text',
			},
			{
				text: 'ASSESSMENT_VALUE',
				value: 'comp_assessment_value',
				class: 'secondary white--text',
			},
			{
				text: 'SCHOOL_DIST',
				value: 'school_district',
				class: 'secondary white--text',
			},
			{
				text: 'HEAT_TYPE',
				value: 'heat_type',
				class: 'secondary white--text',
			},
			{
				text: 'POOL',
				value: 'pool',
				class: 'secondary white--text',
			},
			{
				text: 'BLOCK',
				value: 'block',
				class: 'secondary white--text',
			},
			{
				text: 'BUYER',
				value: 'buyer_full_name',
				class: 'secondary white--text',
			},
			{
				text: 'LAND_USE',
				value: 'land_use',
				class: 'secondary white--text',
			},
			{
				text: 'BEDROOMS',
				value: 'bedrooms',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'FULL_BATH',
				value: 'full_baths',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'HALF_BATH',
				value: 'half_baths',
				class: 'secondary white--text',
				show: true,
			},
			{
				text: 'GARAGES',
				value: 'garages',
				class: 'secondary white--text',
			},
			{
				text: 'APN',
				value: 'apn',
				class: 'secondary white--text',
			},
			{
				text: 'MARKET_VALUE',
				value: 'comp_market_value',
				class: 'secondary white--text',
			},
			{
				text: 'CONDO VIEW',
				value: 'condo_view',
				class: 'secondary white--text',
			},
			
		],
		tableCompsHeaders: [],
		tableCompsSettingsDialog: false,
		tab: 0,
		isShowLogComps: false,
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
		]),
		...mapGetters('counties', [
			'counties',
		]),
		...mapGetters('constants', [
			'constants',
		]),
		...mapGetters('adjustments', [
			'transAdjustments',
		]),
		...mapGetters('obsolescences', [
			'obsolescences',
		]),
		/**
		 * Check if current property located in Florida
		 * @returns {Boolean}
		 */
		isFL() {
			return this.property?.state === 'FL'
		},
		selected_comps_properties() {
			return this.comps.filter(item => item.selected)
		},
		updated_comps_properties() {
			return this.comps.filter(item => this.updatedCompIds.indexOf(item.id) >= 0)
		},
		proposedMarketValue() {
			const sum = this.selected_comps_properties.reduce((a, b) => {
				const {
					adjusted_market_value,
					adjustments,
				} = b
				if (this.isFL) {
					const cos_adjusted_sale = adjusted_market_value + adjustments?.COST_OF_SALE?.value
					return a + cos_adjusted_sale
				} else {
					return a + adjusted_market_value
				}
			}, 0)
			const length = this.selected_comps_properties.length
			return sum / length || 0
		},
		proposedAssessment() {
			if (this.proposedMarketValue) {
				return Number(this.proposedMarketValue * this.assessment_results.assessment_ratio).toFixed()
			} else {
				return this.assessment_results?.current_assessment_value
			}
		},
		adjustmentsList() {
			const adjs = this.comps[0] ? Object.keys(this.comps[0].adjustments) : []
			return adjs.filter(item => {
				if (item === 'COST_OF_SALE') {
					return false
				}
				return true
			})
		},
		printAdjustmentsList() {
			return this.adjustmentsList.filter(item => {
				if (item === 'LOCATION' || item === 'COST_OF_SALE' || item === 'WATER') {
					return false
				}
				return true
			})
		},
		cmaNotification() {
			return this.property?.cma_notification;
		},
		fields() {
			return [
				{
					text: 'Property Title',
					value: 'r_type',
				},
				{
					text: 'Comparables',
					value: 'comparables',
					class: 'primary lighten-4',
				},
				{
					text: 'ParID (APN)',
					value: 'apn',
					class: 'primary lighten-4',
				},
				{
					text: 'Subj Photo',
					value: 'photos',
					class: 'grey lighten-2 pa-0',
				},
				{
					text: 'Address',
					value: 'address',
				},
				{
					text: 'Proximity',
					value: 'proximity',
				},
				...(
					this.isFL
					? [{
						text: 'Subdivision',
						value: 'subdivision',
					}] : []
				),
				{
					text: 'School Dist',
					value: 'school_district',
				},
				{
					text: 'Class',
					value: 'property_class',
				},
				{
					text: 'Age',
					value: 'age_effective_age',
				},
				{
					text: 'Style',
					value: 'style',
				},
				...(
					this.property.water_category
						? [{
							text: 'Water Category',
							value: 'water_category',
						}] : []
				),
				...(
					this.isFL
					? [{
						text: 'Land Tag',
						value: 'land_tag',
					}] : []
				),
				...(
					this.property.is_condo && this.property.county === 'miamidade'
						? [{
							text: 'CONDO VIEW',
							value: 'condo_view',
						}] : []
				),
				...(
					this.property.is_condo && this.property.county === 'broward'
						? [{
							text: 'CONDO FLOOR',
							value: 'condo_view_floor',
						}, {
							text: 'CONDO LOCATION',
							value: 'condo_view_location',
						}, {
							text: 'CONDO INFLUENCE',
							value: 'condo_view_influence',
						}] : []
				),
				{
					text: 'Sale Price',
					value: 'last_sale_price_formatted',
				},
				{
					text: 'Sale Date',
					value: 'last_sale_date_formatted',
				},
				...(
					this.isFL
					? [
						{
							text: 'OWNERS',
							value: 'owners',
						},
					]
					: [
						{
							text: 'BUYER',
							value: 'buyer_full_name',
						},
						{
							text: 'SELLER',
							value: 'seller_full_name',
						},
					]
				),
				{
					text: '',
					value: 'description',
					class: 'primary lighten-4',
				},
				...(
					this.adjustmentsList.map(adj => ({
						text: adj,
						value: `adjustments.${adj}`,
						class: 'primary lighten-4',
						...(
							adj === 'AGE' ? {
								render: (v, item) => {
									if (item.r_type === 'SBJ') {
										return `${v?.comp_value}`
									} else {
										return `${v?.comp_value} (${Number(v?.comp_percent_value || 0).toFixed(0)}%)`
									}
								}
							} : {}
						),
						...(
							adj === 'GLA' ? {
								render: (v) => {
									return this.$options.filters.bignum(Number(v?.comp_value))
								}
							} : {}
						),
						...(
							adj === 'CONDO_VIEW_FLOOR' ? {
								render: (v, item) => {
									if (item.r_type === 'SBJ') {
										return `${v?.comp_value}`
									} else {
										return `${v?.comp_value} (${Number(v?.comp_percent_value || 0).toFixed(0)}%)`
									}
								}
							} : {}
						),
					}))
				),
				{
					text: 'Other Adjustment',
					value: 'other_adjustment',
					class: 'primary lighten-4',
				},
				{
					text: 'GROSS ADJ.',
					value: 'gross_adjustments',
				},
				{
					text: 'Net ADJ.',
					value: 'adjustment_delta_value',
				},
				{
					text: this.isFL ? 'Adjusted Sale $' : 'Net Adj. Value',
					value: 'adjusted_market_value',
				},
				...(
					this.isFL
					? [
						{
							text: `COS Adjustment ${this.property?.adjustments?.COST_OF_SALE?.rule_value}%`,
							value: 'adjustments.COST_OF_SALE.value',
						}, {
							text: 'COS Adjusted Sale $',
							value: 'cos_adjusted_sale',
						},
					] : []
				),
			]
		},
		good_comps_properties() {
			return this.comps.filter(item => item.status === 'good')
		},
		bad_comps_properties() {
			return this.comps.filter(item => item.status === 'bad')
		},
		compsByProximity() {
			return JSON.parse(JSON.stringify(this.comps)).sort(this.sortCompsByProximity)
		},
		goodCompsCount() {
			return this.good_comps_properties.length
		},
		badCompsCount() {
			return this.bad_comps_properties.length
		},
		allCompsCount() {
			return this.comps.length
		},
		compsToSelectCount() {
			// TODO: Check if we should show only subject when cma notification is success
			if (this.isFL && this.cmaNotification?.status === 'success') {
				return 0
			} else {
				return 4
			}
		},
		pdfTableAllHeaders() {
			return [
				...(
					this.isFL 
					? [{
						text: 'FOLIO',
						value: 'apn',
						noWrap: true,
					}] 
					
					: [{
						text: 'SEC',
						value: 'section',
						noWrap: true,
					},
					{
						text: 'BLOCK',
						value: 'block',
						noWrap: true,
					},
					{
						text: 'LOT',
						value: 'lot',
						noWrap: true,
					}]
				),
				{
					text: 'SD',
					value: 'school_district',
					noWrap: true,
				},
				{
					text: 'LIV_SF',
					value: 'gla_sqft_formatted',
					noWrap: true,
				},
				{
					text: 'NUM',
					value: 'number',
				},
				{
					text: 'ST_NAME',
					value: 'street',
					noWrap: true,
				},
				{
					text: 'CLASS',
					value: 'class',
				},
				{
					text: 'STYLE',
					value: 'style',
				},
				{
					text: 'AV_TOT',
					value: 'comp_assessment_value',
				},
				{
					text: 'ACRES',
					value: 'lot_size',
				},
				{
					text: 'BTH * 0.5',
					value: 'baths',
				},
				{
					text: 'HBTH',
					value: 'half_baths',
				},
				{
					text: 'BED',
					value: 'bedrooms',
				},
				// Show columns for every adjustments
				// ...(
				// 	this.adjustmentsList ? this.adjustmentsList.map(adj => ({
				// 		text: adj,
				// 		value: `adjustments.${adj}.comp_value`,
				// 		noWrap: true,
				// 	}))
				// 	: []
				// ),
				{
					text: 'BUILT',
					value: 'age',
					noWrap: true,
				},
				{
					text: 'SALE_PRICE',
					value: 'last_sale_price_formatted',
					noWrap: true,
				},
				{
					text: 'SALE_DATE',
					value: 'last_sale_date_formatted',
				},
				{
					text: 'R_TYPE',
					value: 'r_type',
				},
				{
					text: 'BAD',
					value: 'status',
					noWrap: true,
					format: (val) => {
						return val === 'bad' ? 'x' : ''
					},
				},
				{
					text: 'ADJ/V',
					value: 'adjusted_market_value',
					render: (text, item) => {
						let value = item.adjusted_market_value
						if (this.isFL) {
							value += item.adjustments?.COST_OF_SALE?.value
						}
						return {
							text: this.$options.filters.currency(value) || '',
							margin: [0, 0, 0, 0],
							noWrap: true,
						}
					},
				},
				{
					text: 'PROXIM',
					value: 'proximity',
					format: (val) => {
						return Number(val).toFixed(2) || val
					},
				},
			]
		},
		printPdfFileName() {
			const name = resolve(this.printPdfFileNameField, this.property)
			return `CMA ${name}.pdf`
		},
		// TODO: Put into CmaReportService
		printPdfFields() {
			return [
				{
					text: 'Property title',
					value: 'r_type',
					render: (text, item, field, index) => {
						let title = this.isFL ? `COMPARABLE #${index}` : `C${index}`
						if (text === 'SBJ') {
							title = this.isFL ? 'SUBJECT' : 'SBJ'
						}
						return {
							text: title,
							alignment: 'center',
							fillColor: this.isFL ? '#ccc' : '',
							bold: true,
							colSpan: 2,	
						}
					},
					...(
						this.isFL
							? {
								hLineWidth: 1.5,
								hLineColor: 'black',
							} : {}
					),
					renderField: (text) => ({
						text: this.isFL ? '' : text,
						fillColor: this.isFL ? '#ccc' : '',
						margin: [0, 0, 0, 0],
						noWrap: true,
						bold: true,
					}),
				},
				...(
					!this.isFL
					? [
						{
							text: 'Comparables',
							value: 'comparables',
							render: (text, item, field) => ({
								columns: [
									{
										stack: [
											'Sec',
											{
												text: item.section,
												background: item.section === this.property.section && item.block === this.property.block ? 'yellow' : ''
											},
										],
										alignment: 'center',
									},
									{
										stack: [
											'Block',
											{
												text: item.block,
												background: item.section === this.property.section && item.block === this.property.block ? 'yellow' : ''
											},
										],
										alignment: 'center',
									},
									{
										stack: [
											'Lot',
											item.lot,
										],
										alignment: 'center',
									},
								],
								fillColor: this.highlightedClass(item, field.value),
								colSpan: 2,
							}),
						},
					] : []
				),
				{
					text: this.isFL ? 'Folio' : 'PARID (APN)',
					value: 'apn',
					alignment: 'center',
					hLineWidth: 1.5,
					hLineColor: 'black',
					colSpan: 2,
				},
				...(
					[
						this.property,
						...this.selected_comps_properties,
					].some(item => item.photos?.length > 0)
					? [{
						text: 'Subj Photo',
						value: 'photos',
						render: async (text) => {
							const url = this.findByKey(text, (item) => item.is_best === true).url
							let image = await this.getBase64(url)
							if(!image) {
								image = await this.getBase64(noPhoto)
							}
							const width = this.isFL ? 140 : 167
							const height = 90
							return {
								image: image ? `data:image/jpeg;base64, ${image}` : '',
								width,
								height,
								cover: [width, height],
								alignment: 'center',
								colSpan: 2,
							}
						},
						hLineWidth: 1.5,
						hLineColor: 'black',
						colSpan: 2,
					}] : []
				),
				{
					text: 'Address',
					value: 'address_line_1',
					render: (text, item, field) => ({
						text: `${item.address_line_1} ${item.address_line_2 ? item.address_line_2 : ''}`,
						background: item.street === this.property.street ? 'yellow' : '',
						fillColor: this.highlightedClass(item, field.value),
						margin: [-5, 0],
						alignment: 'center',
						colSpan: 2,
					})
				},
				{
					text: 'Proximity',
					value: 'proximity',
					render: (text, item, field) => ({
						text: this.$options.filters.miles(text),
						fillColor: this.highlightedClass(item, field.value),
						alignment: 'center',
						colSpan: 2,
					}),
				},
				
				...(
					this.isFL
					? [
						{
							text: 'Subdivision',
							value: 'subdivision',
							render: (text) => {
								return {
									text,
									alignment: 'center',
									truncate: true,
									colSpan: 2,
								}
							},
						},
					] : []
				),
				...(
					!this.isFL
					? [
						{
							text: 'School District',
							value: 'school_district', 
							alignment: 'center',
							colSpan: 2,
						},
					] : []
				),
				{
					text: 'Class',
					value: 'class',
					render: (text, item, field) => {
						text = `${item.property_class_description || ''} (${text})`
						return {
							text,
							fillColor: this.highlightedClass(item, field.value),
							alignment: 'center',
							colSpan: 2,
						}
					},
				},
				{
					text: 'Age',
					value: 'age_effective_age',
					alignment: 'center',
					colSpan: 2,
				},
				...(
					!this.isFL
					? [
						{
							text: 'Style',
							value: 'style',
							alignment: 'center',
							colSpan: 2,
						},
					] : []
				),
				...(
					this.property.is_condo && this.property.county === 'miamidade'
						? [{
							text: 'Condo View',
							value: 'condo_view',
							colSpan: 2,
						}] : []
				),
				...(
					this.property.is_condo && this.property.county === 'broward'
						? [{
							text: 'Condo Floor',
							value: 'condo_view_floor',
							colSpan: 2,
						}, {
							text: 'Condo Location',
							value: 'condo_view_location',
							colSpan: 2,
						}, {
							text: 'Condo Influence',
							value: 'condo_view_influence',
							colSpan: 2,
						}] : []
				),
				...(
					this.property.water_category
						? [{
							text: 'Water Category',
							value: 'water_category',
							render: (text) => ({
								text: `(${text?text:'-'}) ${text?this.$options.filters.mapperFilter(text, this.constants.water_category_map):'No Water'}`,
								alignment: 'center',
							}),
							colSpan: 2,
						}] : []
				),
				...(
					!this.property.is_condo && this.property.county === 'broward'
						? [{
							text: 'Land Tag',
							value: 'land_tag',
							render: (text) => ({
								text: `(${text}) ${this.$options.filters.mapperFilter(text, this.constants.land_tag_map)}`,
								alignment: 'center',
							}),
							colSpan: 2,
						}] : []
				),
				{
					text: 'Sale Price',
					value: 'last_sale_price_formatted',
					render: (text, item, field) => {
						if (item.r_type === 'SBJ' && !item.print_sale_info) {
							text = ''
						}
						return {
							text,
							fillColor: this.highlightedClass(item, field.value),
							alignment: 'center',
							colSpan: 2,
						}
					},
				},
				{
					text: 'Sale Date',
					value: 'last_sale_date_formatted',
					render: (text, item, field) => {
						if (item.r_type === 'SBJ' && !item.print_sale_info) {
							text = ''
						}
						return {
							text,
							fillColor: this.highlightedClass(item, field.value),
							alignment: 'center',
							colSpan: 2,
						}
					},
					hLineWidth: 1.5,
					hLineColor: 'black',
				},
				{
					cells: [
						{
							value: 'description',
							render: (text, comp) => ({
								text: 'Description',
								colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
								fillColor: this.isFL ? '#ccc' : '',
								alignment: 'center',
								bold: true,
							}),
						},
						{
							value: 'description',
							render: () => ({
								text: '+/- Adj',
								fillColor: this.isFL ? '#ccc' : '',
								alignment: 'center',
								bold: true,
							}),
						}
					],
					renderField: () => ({
						text: '',
						fillColor: this.isFL ? '#ccc' : '',
					}),
					hLineWidth: 1.5,
					hLineColor: 'black',
				},
				...(
					this.printAdjustmentsList.map(adj => {
						const adjName = this.transAdjustments?.[adj]?.name || adj
						const adjustments = this.property?.adjustments
						const ruleValue = adjustments?.[adj]?.rule_value
						const showFormattedRuleValue = this.settings?.settings?.show_formatted_rule_value

						let formattedRuleValue = null
						if (showFormattedRuleValue) {
							formattedRuleValue = this.$options.filters.currency(Number(ruleValue))

							if (adj === 'GLA' || adj === 'LOT') {
								formattedRuleValue += '/sf'
							} else if (adj === 'AGE') {
								formattedRuleValue = null
							}
						}

						let text = adjName

						return {
							text,
							value: `adjustments.${adj}`,
							cells: [
								{
									value: `adjustments.${adj}`,
									render: (value, item, cellField) => {
										const field = item[this.transAdjustments?.[value?.key]?.property_field]
										
										let mValue = this.$options.filters.mapperFilter(
											field,
											this.constants[`${value?.key?.toLowerCase()}_type_map`]
										)
										if (adj === 'LOT') {
											const lotSizeSqft = item?.lot_size_sqft
											if (lotSizeSqft) {
												mValue += `/${this.$options.filters.bignum(lotSizeSqft)}`
											}
										}

										let text = mValue
										if (adj === 'POOL') {
											mValue = item?.adjustments?.[adj]?.comp_value
											text = this.$options.filters.booleanFilter(mValue)
										} else if (adj === 'AGE' || adj === 'CONDO_VIEW_FLOOR') {
											const v = item?.adjustments?.[adj]
											if (item.r_type === 'SBJ') {
												text = `${v?.comp_value}`
											} else {
												text = `${v?.comp_value} (${Number(v?.comp_percent_value || 0).toFixed(0)}%)`
											}
										} else {
											text = this.$options.filters.bignum(mValue) || ''
										}
										text = text.toUpperCase()

										return {
											text,
											alignment: 'center',
											colSpan: item?.r_type === 'SBJ' ? 2 : 1,
											fillColor: this.highlightedClass(item, cellField.value),
										}
									},
								},
								{
									value: `adjustments.${adj}`,
									render: (value, item, cellField) => {
										const adjusted = item?.adjustments?.[adj]?.value || ''

										return {
											text: this.$options.filters.currency(adjusted),
											alignment: 'right',
											bold: true,
											fillColor: this.highlightedClass(item, cellField.value),
										}
									},
								},
							],
							renderField: (text) => ({
								columns: [
									{
										width: '50%',
										text,
										bold: true,
									},
									{
										width: '50%',
										text: ruleValue && formattedRuleValue ? `(${formattedRuleValue})` : '',
										alignment: 'right',
									},
								],
								margin: [0, 0, 0, 0],
								noWrap: true,
							}),
						}
					})
				),
				...(
					this.property.adjustments.WATER ? [{
						text: 'Water',
						cells: [
							{
								value: 'adjustments.WATER',
								render: (text, comp) => {
									const percentValue = text?.comp_percent_value
									text = comp?.adjustments?.WATER?.comp_value

									return {
										text: `${text ? 'YES' : 'NO'} (${percentValue || 0}%)`,
										alignment: 'center',
										colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
									}
								},
							},
							{
								value: 'adjustments.WATER',
								render: (text, comp) => {
									const adjusted = comp?.adjustments?.WATER?.value

									return {
										text: this.$options.filters.currency(adjusted),
										alignment: 'right',
										bold: true,
									}
								},
							},
						],
					}] : []
				),
				...( this.property?.adjustments?.LOCATION ?
					[{
						text: 'Obsolescence',
						cells: [
							{
								value: 'adjustments.LOCATION',
								render: (text, comp) => {
									const ruleValue = text?.rule_value
									let mappedText = text.comp_value ? `(${text.comp_value}) ` : ''
									mappedText += this.$options.filters.mapperFilter(Number(text?.comp_value) || 0, this.obsolescences, (v) => v ? v.rule_name : '-')

									return {
										columns: [
											{
												width: '55%',
												text: mappedText,
												maxHeight: 15,
												truncate: true,
											},
											{
												width: '45%',
												text: `(${ruleValue})`,
												maxHeight: 15,
												margin: [0, 0, -5, 0],
											},
										],
										alignment: 'center',
										colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
									}
								},
							},
							{
								value: 'adjustments.LOCATION',
								render: (text, comp) => {
									const adjusted = comp?.adjustments?.LOCATION?.value

									return {
										text: this.$options.filters.currency(adjusted),
										alignment: 'right',
										bold: true,
									}
								},
							}
						],
					}] : []
				),
				{
					text: 'Other Adj.',
					cells: [
						{
							value: 'other_adjustment_description',
							render: (value, comp) => ({
								text: value,
								alignment: 'center',
								colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
							})
						},
						{
							value: 'other_adjustment',
							render: (value, comp, field) => ({
								text: this.$options.filters.currency(value) || ' ',
								alignment: 'right',
								fillColor: this.highlightedClass(comp, field.value),
							}),
						},
					],
					hLineWidth: 1.5,
					hLineColor: 'black',
				},
				{
					text: 'Net Adj.',
					cells: [
						{
							value: 'adjustment_delta_value',
							render: (value, comp, field) => ({
								text: '',
								colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
								fillColor: this.highlightedClass(comp, field.value),
							}),
						},
						{
							value: 'adjustment_delta_value',
							render: (value, comp, field) => ({
								text: this.$options.filters.currency(value),
								alignment: 'right',
								fillColor: this.highlightedClass(comp, field.value),
							}),
						},
					],
					renderField: (text) => ({
						text: text,
						fillColor: this.isFL ? '#ccc' : '',
						margin: [0, 0, 0, 0],
						noWrap: true,
						bold: true,
					}),
				},
				{
					text: this.isFL ? 'Adjusted Sale $' : 'Net Adj. Value',
					cells: [
						{
							value: 'adjusted_market_value',
							render: (value, comp, field) => ({
								text: '',
								colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
								fillColor: this.highlightedClass(comp, field.value),
							}),
						},
						{
							value: 'adjusted_market_value',
							render: (value, comp, field) => ({
								text: this.$options.filters.currency(value),
								alignment: 'right',
								bold: true,
								fillColor: this.highlightedClass(comp, field.value),
							}),
						},
					],
					renderField: (text) => ({
						text: text,
						fillColor: this.isFL ? '#ccc' : '',
						margin: [0, 0, 0, 0],
						noWrap: true,
						bold: true,
					}),
				},
				...(
					this.isFL
					? [
						{
							text: `COS Adjustment ${this.property?.adjustments?.COST_OF_SALE?.rule_value}%`,
							cells: [
								{
									value: 'adjustments.COST_OF_SALE.value',
									render: (value, comp, field) => ({
										text: comp?.r_type === 'SBJ' ? 'Per F.S. 193.011(1),(8) and form DR-493' : '',
										fillColor: this.highlightedClass(comp, field.value),
										rowSpan: comp?.r_type === 'SBJ' ? 2 : 1,
										colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
									}),
								},
								{
									value: 'adjustments.COST_OF_SALE.value',
									render: (value, comp, field) => ({
										text: this.$options.filters.currency(value),
										alignment: 'right',
										fillColor: this.highlightedClass(comp, field.value),
									}),
								},
							],
							renderField: (text) => ({
								text: text,
								fillColor: this.isFL ? '#ccc' : '',
								margin: [0, 0, 0, 0],
								noWrap: true,
								bold: true,
							}),
						},
						{
							text: 'COS Adjusted Sale $',
							cells: [
								{
									value: 'adjusted_market_value',
									render: (value, comp, field) => ({
										text: '',
										colSpan: comp?.r_type === 'SBJ' ? 2 : 1,
										fillColor: this.highlightedClass(comp, field.value),
									}),
								},
								{
									value: 'adjusted_market_value',
									render: (value, comp, field) => ({
										text: this.$options.filters.currency(value + comp.adjustments?.COST_OF_SALE?.value),
										alignment: 'right',
										fillColor: this.highlightedClass(comp, field.value),
									}),
								},
							],
							renderField: (text) => ({
								text: text,
								fillColor: this.isFL ? '#ccc' : '',
								margin: [0, 0, 0, 0],
								noWrap: true,
								bold: true,
							}),
						},
					] : []
				),
			]
		},
		mapComps() {
			let comps
			if(this.isShowLogComps) {
				comps = this.log_comps
			} else {
				comps = this.comps
			}
			if(this.mapCompFilter.value) {
				comps = filter(comps, this.mapCompFilter.value)
			}
			return comps.slice(0, 1001)
		},
		tableComps() {
			return [
				this.property,
				...this.comps
			]
		},
		lockedComps() {
			return [ this.property?.id ]
		},
		compSource() {
			return {
					type: 'geojson',
					data: {
						type: 'FeatureCollection',
						features: [ this.property, ...this.mapComps ].map(item => {
							return {
								geometry: {
									coordinates: [
										item?.longitude,
										item?.latitude
									],
									type: 'Point',
								},
								properties: {
									icon: item.r_type === 'SBJ' ? 'map-marker-sbj'
										: item.status === 'good'
											? (item.selected ? 'map-marker-good-selected' 	: 	'map-marker-good')
											: (item.selected ? 'map-marker-bad-selected' 	: 	'map-marker-bad'),
									title: item?.r_type ? (item.r_type === 'SBJ' ? 'S' : item.r_type) : item.r_type,
									textColor: '#ffffff',
									...item,
								},
							}
						})
					},
					// cluster: true,
					// clusterRadius: 1,
					// clusterMaxZoom: 22,
				}
		},
		compFeatures() {
			return {
				id: 'comp-features',
				type: 'symbol',
				source: this.compSource,
				layout: {
					// get the icon name from the source's "icon" property
					// concatenate the name to get an icon from the style's sprite sheet
					'icon-image': ['get', 'icon'],
					'icon-size': 0.6,
					// get the title name from the source's "title" property
					'text-field': ['get', 'title'],
					'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
					'text-offset': [0, -1.2],
					'text-anchor': 'top',
					'text-size': 11,
					'icon-allow-overlap': true,
					'text-allow-overlap': true,
					// 'text-color': ['get', 'textColor'],
				},
				paint: {
					'text-color': '#ffffff',
				},
			}
		},
		compFeaturesClusters() {
			return {
				id: 'comp-features-clusters',
				type: 'circle',
				paint: {
					'circle-color': '#51bbd6',
					'circle-radius': 20,
				},
			}
		},
		obsFeatures() {
			let features = [
				this.property,
				...this.mapComps,
			].map(item => item.obs_geojson)
			.flat()
			.filter(Boolean)

			features = uniqWith(features, isEqual)

			return {
				id: 'obs-features',
				type: 'fill',
				source: {
					type: 'geojson',
					data: {
						type: 'FeatureCollection',
						features,
					},
				},
				paint: {
					'fill-outline-color': '#f00',
					'fill-color': '#f00',
					'fill-opacity': 0.5,
				},
				'filter': ['==', '$type', 'Polygon'],
			}
		},
		obsLineFeatures() {
			return {
				id: 'obs-line-features',
				type: 'line',
				source: {
					type: 'geojson',
					data: {
						type: 'FeatureCollection',
						features: [
								this.property,
								...this.mapComps,
							].map(item => item.obs_geojson)
							.flat()
							.filter(Boolean),
					},
				},
				paint: {
					'line-color': '#f00',
					'line-width': 5,
				},
			}
		},
		mapTaxLayer() {
			return this.mapTaxLayers.find(item => item.county === this.property?.county)?.layer || {}
		},
		mapRoadsLayer() {
			return this.mapRoadsLayers.find(item => item.county === this.property?.county)?.layer || {}
		},
		taxLayer() {
			return {
				id: 'tax-layer',
				type: 'fill',
				source: {
					type: 'vector',
					url: `mapbox://${this.mapTaxLayer.source}`
				},
				'source-layer': this.mapTaxLayer.sourceLayer,
				layout: {
					visibility: this.isShowTaxLayer && this.mapStyle?.text === 'Street' ? 'visible' : 'none',
				},
				paint: {
					'fill-outline-color': this.mapTaxLayer.color,
					'fill-color': this.mapTaxLayer.color,
					'fill-opacity': 0.3,
				},
			}
		},
		taxLineLayer() {
			return {
				id: 'tax-line-layer',
				type: 'line',
				source: {
					type: 'vector',
					url: `mapbox://${this.mapTaxLayer.source}`
				},
				'source-layer': this.mapTaxLayer.sourceLayer,
				layout: {
					visibility: this.isShowTaxLayer ? 'visible' : 'none',
				},
				paint: {
					'line-color': this.mapTaxLayer.color,
					'line-width': 2,
				},
			}
		},
		roadsLayer() {
			return {
				id: 'roads-layer',
				type: 'line',
				source: {
					type: 'vector',
					url: `mapbox://${this.mapRoadsLayer.source}`
				},
				'source-layer': this.mapRoadsLayer.sourceLayer,
				layout: {
					visibility: this.isShowTaxLayer ? 'visible' : 'none',
				},
				paint: {
					'line-color': '#1dbab4',
					'line-width': 2,
				},
			}
		},
		mapCenter() {
			return [this.property.longitude || -73, this.property.latitude || 41]
		},
		subjectRadiuses() {
			const radiuses = [ 250, 500, 1000 ]
			return radiuses.map(r => this.createSubjectRadius(r * 0.3048, this.mapCenter))
		},

		countyAssessmentDates() {
			return this.assessmentDates.filter(item => item.county === this.property?.county)
		},

		selectedTableCompsHeaders() {
			return [
				{
					text: '',
					value: 'settings',
					class: 'secondary white--text pa-0 px-1',
					show: true,
					sortable: false,
					width: 'auto',
				},
				...this.tableCompsHeaders.filter(item => item.show),
			]
		},
		
		assessment_date() {
			return this.countyAssessmentDates?.find(item => item.id === this.assessment_date_id) || {}
		},
	},
	methods: {
		...mapActions('notification', [
			'notify',
		]),
		...mapActions('counties', [
			'loadCounties',
		]),
		...mapActions('constants', [
			'loadConstants',
		]),
		...mapActions('adjustments', [
			'loadAdjustments',
		]),
		...mapActions('obsolescences', [
			'loadObsolescences',
		]),
		findByKey(arr = [], findFunc) {
			const item = arr.find(item => findFunc(item))
			return item ?? {}
		},
		async loadSettings(county) {
			try {
				const { data } = await globalSettingsApi.getAll({ county })
				this.settings = data[0]
			} catch(error) {
				this.notify({
					text: 'Can not load global settings',
					color: 'error'
				}, { root: true })
			}
		},
		/**
		 * Transform comps to use in Comparison table
		 * @param {Array} comps
		 */
		transformComps(comps) {
			return comps.map((item) => {
				item.adjustments = keyBy(item.adjustments, 'key')
				return item
			})
		},
		async loadSingleCMA(propertyid) {
			try {
				this.loading = true
				const { data } = await singleCmaApi.get(propertyid, {
					assessment_date_id: this.assessmentDateId,
				})
				this.saveCMAResults(data)
				await this.transformCMAResults()
				// this.selectComps(this.comps.filter(c => c.status === 'good')
				// 							.slice(0, 4)
				// 							.map(c => c.id))

				let sortedComps = cloneDeep(this.comps)
				this.selectComps(sortedComps.slice(0, this.compsToSelectCount)
											.map(c => c.id))
			} catch(error) {
				this.notify({
					text: 'Can not load Single CMA results',
					color: 'error'
				}, { root: true })
			} finally {
				this.loading = false
			}
		},
		async reloadSingleCMA(subject, all_comps, rule_set, assessment) {
			try {
				this.loading = true
				const ids = this.selected_comps_properties.map(c => c.id)
				const payload = {
					subject,
					all_comps,
					rule_set,
					assessment,
				}
				const params = {
					override_assessment_value: this.assessment.override_value,
				}
				// const { data } = await singleCmaApi.post(payload, this.cmaConfig)
				const { data } = await singleCmaApi.post(payload, params)
				this.saveCMAResults(data)
				await this.transformCMAResults()
				this.selectComps(ids)
			} catch(error) {
				this.notify({
					text: 'Can not load Single CMA results',
					color: 'error'
				}, { root: true })
			} finally {
				this.loading = false
			}
		},
		async loadNearbyCMA(propertyid) {
			try {
				const { data } = await singleCmaApi.get(propertyid, {
					nearby: true,
					assessment_date_id: this.assessmentDateId,
				})
				this.nearbyComps = data.all_comps.map(comp => {
					return new Comp(comp)
				})
			} catch(error) {
				this.notify({
					text: 'Can not load nearby CMA results',
					color: 'error'
				}, { root: true })
			}
		},

		async loadCmaLog() {
			try {
				this.loadingLog = true
				const payload = {
					subject: this.property,
					all_comps: this.comps,
					rule_set: this.ruleSet,
					assessment: this.assessment,
				}
				const { data } = await singleCmaApi.log(this.id, payload)
				this.log_rules = data?.rules
				this.log_comps = data?.comps
			} catch (error) {
				this.notify({
					text: 'Can not load CMA Log',
					color: 'error'
				}, { root: true })
			} finally {
				this.loadingLog = false
			}
		},

		saveCMAResults(data) {
			this.assessment = data.assessment
			this.assessment_date_id = data.assessment_date_id
			this.assessment_results = new AssessmentResult(data.assessment_results)
			this.average_ranges = data.average_ranges
			this.property = new Comp(data.subject)
			this.property.r_type = 'SBJ'
			this.property.table_fixed = true

			let c = 1
			let bc = 1
			this.comps = data.all_comps.map(comp => {
				const r_type = comp.status === 'good' ? `C${c++}` : `BC${bc++}`
				return new Comp({
					...comp,
					r_type,
				})
			})
			// If Florida - ignore good/bad
			if (!this.isFL) {
				this.comps.sort(this.sortComps)
			}
		},
		/**
		 * Compose pdf photo row for Good/Bad report
		 * @param {Array} items property models array
		 */
		async composePdfPhotoRow(items) {
			return {
				columns: [
					...(
						await Promise.all(items.map(async (comp) => {
							const url = this.findByKey(comp.photos, (item) => item.is_best === true).url

							let image = await this.getBase64(url)
							if(!image) {
								image = await this.getBase64(noPhoto)
							}
								
							return {
								width: '20%',
								stack: [
									{
										image: `data:image/jpeg;base64, ${image}`,
										width: 100,
										alignment: 'center',
									}, {
										text: `${comp.r_type || ''}    ${comp.section}-${comp.block}-${comp.lot}`,
										alignment: 'center',
									},
								],
							}
						}))
					),	
				],
				margin: [ 0, 5, 0, 5 ],
			}
		},
		async composePdfPropDetailedRow(prop) {
			const url = this.findByKey(prop.photos, (item) => item.is_best === true).url

			let image = await this.getBase64(url)
			if(!image) {
				image = await this.getBase64(noPhoto)
			}

			return {
				columns: [
					{
						width: '20%',
						stack: [
							{
								image: `data:image/jpeg;base64, ${image}`,
								width: 100,
								alignment: 'center',
							},
						],
					},
					{
						width: '10%',
						text: '',
					},
					{
						width: '20%',
						stack: [
							{
								text: 'SUBJECT',
								alignment: 'center',
							},
							{
								columns: [
									{
										stack: [
											'SEC',
											prop.section,
											'GLA',
											'Sale Date',
											'Sale Price',
										],
									},
									{
										stack: [
											'BLOCK',
											prop.block,
											'=',
											'=',
											'=',
										],
									},
									{
										stack: [
											'LOT',
											prop.lot,
											{
												text: prop.gla_sqft_formatted,
												bold: true,
											},
											{
												text: prop.last_sale_date_formatted,
												bold: true,
											},
											{
												text: prop.last_sale_price_formatted,
												bold: true,
											},
										],
									},
								],
							},
						],
					},
				],
				margin: [ 0, 10, 0, 5 ],
			}
		},
		/**
		 * Get pdf file name from property fields
		 * @param {Object} prop property model
		 */
		getPdfFileName({ section, block, lot }) {
			return `${section}_${block}_${lot}gb.pdf`
		},
		async printGoodPadReport() {
			this.pdfContent = await this.genPdfContent()

			this.$nextTick(() => {
				this.$refs.goodBadReport.print()
			})
		},
		printGoodBadReportExtended() {
			const items = [
				this.property,
				...this.comps,
			]

			const nearbyItems = [
				this.property,
				...this.nearbyComps,
			]

			const report = new GoodBadReportExtended({
				items,
				nearbyItems,
				averageRanges: this.average_ranges,
				assessmentResults: this.assessment_results,
				styles: this.pdfStyles,
			})

			report.print()
		},
		async generatePrintPDF() {

			const features = cloneDeep([
				this.property,
				...this.comps,
			])

			const markers = features
				.filter(({
					selected,
					r_type,
				}) => selected || r_type === 'SBJ')
				.map(({
					longitude,
					latitude,
					r_type,
				}, index) => {
					let label = 'good'
					if (r_type === 'SBJ') label = 'sbj'
					else if (index <= 10) label = `good-${index}`
					return {
						label,
						coords: [
							longitude,
							latitude,
						],
					}
				})

			const mapImgUrl = MapboxApiService.genStaticMapURL({
				styleId: this.mapStyle?.value,
				markers,
			})

			const mapImg = await this.getBase64(mapImgUrl)

			const cmaComps = cloneDeep(this.$refs.cmaTable.localItems)

			const comments = [
				this.printFieldTop,
				...(!this.isFL
					? [ this.printFieldBottom ]
					: []
				),
			]

			// Generate PDF content
			this.printPdfContent = await CmaReportService.genContent({
				comps: cmaComps,
				fields: this.printPdfFields,
				property: this.property,
				header: this.settings?.settings?.pdf_header,
				results: this.assessment_results,
				comments,
				proposedAssessment: this.proposedAssessment,
				proposedMarketValue: this.proposedMarketValue,
				mapImg: `data:image/jpeg;base64, ${mapImg}`,
				cellClass: this.highlightedClass,
			})
		},
		async print() {
			await this.$refs.cmaPrintDialog.open()
			await this.generatePrintPDF()
			this.$nextTick(() => {
				this.$refs.cmaPDF.print()
			})
		},
		printHadler(e) {
			if (e.code == 'KeyP' && (e.ctrlKey || e.metaKey)) {
				this.print()
			}
		},
		createSubjectRadius(r, coordinates) {
			return {
				id: `subject-radius-${r}`,
				type: 'circle',
				source: {
					type: 'geojson',
					data: {
						type: 'FeatureCollection',
						features: [
							{
								type: 'Feature',
								geometry: {
									type: 'Point',
									coordinates,
								},
							},
						],
					},
				},
				paint: {
					'circle-radius': {
						stops: [
							[0, 0],
							[20, r / 0.075 / Math.cos(coordinates[1] * Math.PI / 180)]
						],
						base: 2,
					},
					'circle-color': 'transparent',
					'circle-stroke-color': 'blue',
					'circle-stroke-width': 2,
					'circle-stroke-opacity': 0.6,
				},
			}
		},
		showMapPopup(feature, map) {

			// Populate the popup and set its coordinates
			// based on the feature found.
			new mapboxgl.Popup()
				.setLngLat(feature.geometry.coordinates)
				.setHTML('<div id="vue-popup-content"></div>')
				.addTo(map)

			const Component = this.isShowLogComps ? this.AMapLogPopup : this.AMapPopup

			const popup = new Component({
				propsData: {
					feature: feature
				}
			}).$mount('#vue-popup-content')

			popup.$on('selection', this.selectComp)
			popup.$on('show', this.scrollToComp)
		},

		showObsMapPopup(feature, map, $event) {

			// Populate the popup and set its coordinates
			// based on the feature found.
			new mapboxgl.Popup()
				.setLngLat($event.lngLat)
				.setHTML('<div id="vue-popup-content"></div>')
				.addTo(map)

			const Component = this.AMapObsPopup

			new Component({
				propsData: {
					feature: feature
				}
			}).$mount('#vue-popup-content')
		},

		clusterLayerLoaded(clusters) {
			const compFeaturesLayer = this.$refs.compFeaturesLayer

			clusters.forEach(cluster => {

				const clusterFeatures = cluster.properties.features

				const spiderifiedCluster = {
					// id: clusterId,
					coordinates: clusterFeatures[0].geometry.coordinates,
				}

				if (clusterFeatures.find(feature => feature.properties.r_type === 'SBJ' || feature.properties.selected)) {
					compFeaturesLayer.buildSpider(spiderifiedCluster, clusterFeatures)
				}
			})
		},

		/**
		 * Change comp selection by id
		 * @param {Number} id comp id
		 * @param {Boolean} value true
		 */
		selectComp(id, value = true) {
			const comp = this.comps.find(item => item.id === id)
			const index = this.comps.findIndex(item => item.id === id)
			comp.selected = value
			return this.$set(this.comps, index, comp)
		},

		/**
		 * Unselect all comps
		 */
		unselectAllComps() {
			let comps = cloneDeep(this.comps)
			comps = comps.map(comp => ({
				...comp,
				selected: false,
			}))
			this.$set(this, 'comps', comps)
		},

		/**
		 * Change comp selection from array of ids
		 * @param {Array} ids comp ids array
		 * @param {Boolean} value true
		 */
		selectComps(ids = [], value = true) {
			ids.forEach(id => {
				const index = this.comps.findIndex(item => item.id === id)
				const comp = this.comps[index]
				comp.selected = value
				this.$set(this.comps, index, comp)
			})
		},

		/**
		 * Scroll to comp in table
		 * @param {Number} id comp id
		 */
		scrollToComp(id) {
			this.$scrollTo(`#comp-${id}`, 500, {
				onDone: () => {
					this.$scrollTo(`#comp-${id}`, 500, {
						container: '#comp-selection-table .v-data-table__wrapper',
						offset: -60,
						onDone: (elem) => {
							const tr = elem.closest('tr')
							tr.classList.add('highlight')
							setTimeout(() => {
								tr.classList.remove('highlight')
							}, 3000)
						},
					})
				},
			})
		},


		/**
		 * Fly to comp position on the map
		 * @param {Number} id
		 */
		flyToComp(id) {
			try {
				const comp = this.mapComps.find(item => item.id === id)
				this.$refs.map?.map.flyTo({
					center: [ comp.longitude, comp.latitude ],
					essential: true,
				})
			} catch (error) {
				console.error(error)
			}
		},

		async updateComp(comp) {
			if (comp.is_subject) {
				try {
					this.loading = true
					const {
						updated_comps_properties,
						ruleSet,
						assessment,
					} = this
					await this.reloadSingleCMA(comp, updated_comps_properties, ruleSet, assessment)
				} catch (error) {
					this.notify({
						text: 'Can not re-analyze subject property',
						color: 'error'
					}, { root: true })
				} finally {
					this.loading = false
				}
			} else {
				const index = this.comps.findIndex(item => item.id === comp.id)
				this.updatedCompIds.push(comp.id)
				this.$set(this.comps, index, comp)

				try {
					this.loading = true

					const payload = {
						subject: this.property,
						all_comps: [ comp ],
						rule_set: this.ruleSet,
						assessment: this.assessment,
					}
					const { data } = await propertiesApi.analyze(payload)
					const [ newComp ] = this.transformComps(data.all_comps)
					this.$set(this.comps, index, new Comp({ ...comp, ...newComp }))
				} catch(error) {
					this.notify({
						text: 'Can not re-analyze property',
						color: 'error'
					}, { root: true })
				} finally {
					this.loading = false
				}
			}
		},
		/**
		 * Sort comps by status and proximity
		 */
		sortComps(a, b) {
			// Firstly sort by status from good to bad
			if (a.status > b.status) return -1
			if (a.status < b.status) return 1

			// Then sort by priority
			return a.priority - b.priority
		},
		sortCompsByProximity(a, b) {
			return a.proximity - b.proximity
		},
		sortCompsTable(items, sortBy, sortDesc) {
			sortBy = sortBy[0]
			sortDesc = sortDesc[0]
			items.sort((a, b) => {
				if(a.table_fixed) return -1
				if(b.table_fixed) return 1

				if(sortDesc) {
					return b[sortBy] < a[sortBy] ? -1 : 1
				} else {
					return a[sortBy] < b[sortBy] ? -1 : 1
				}
			})
			return items
		},
		async transformCMAResults() {
			await this.loadObsolescences(this.property?.county)
			await this.loadConstants({ county: this.property?.county })

			// Add results to subject model
			const comp = this.comps[0]
			if(comp) {
				this.property.adjustments = keyBy(comp.adjustments.map(item => ({
					name: item.name,
					key: item.key,
					comp_value: item.subject_value,
					rule_value: item.subject_rule_value || item.rule_value,
				})), 'key')

				// Add Obso Result from first comp to subject property
				// if(comp.obso_result) {
				// 	const obso_result = {
				// 		comp_obsolescences: comp.obso_result.subject_obsolescences
				// 	}
				// 	this.property.obso_result = obso_result
				// }
			}

			// Generate pdf file name for Good/Bad report
			this.pdfFileName = this.getPdfFileName(this.property)
			
			// Transform received comps
			this.comps = this.transformComps(this.comps)
		},

		async getBase64(url) {
			try {
				const { data } = await axios.get(url, {
					responseType: 'arraybuffer'
				})

				const response = Buffer.from(data, 'binary')
				return response.toString('base64')
			} catch (error) {
				return null
			}
		},

		async updateProperty(property) {
			try {
				const confirm = await this.$refs.confirm.open('Override Database', 'Are you sure you want to do this?', { color: 'error' })
				if(confirm) {
					await propertiesApi.update(property)
					this.loadSingleCMA(this.id)
					this.notify({
						text: 'Property overriden',
						color: 'success'
					}, { root: true })
				}
				this.$refs.cmaTable.closeDialog()
			} catch (error) {
				this.notify({
					text: 'Can not override the property',
					color: 'error'
				}, { root: true })
				throw error
			}
		},

		/**
		 * Show photo gallery
		 */
		showPhotoGallery(photos = Array, property = Object) {
			this.galleryPhotos = photos
			this.galleryProperty = property
			this.$refs.gallery.open()
		},

		/**
		 * Upload photo
		 */
		async uploadPhoto(file = File) {
			try {
				// Upload photo to server
				const propertyId = this.galleryProperty.id
				let formData = new FormData()
				formData.append('property_photo', file)
				const { data } = await propertiesPhotosApi.create(propertyId, formData)

				if(propertyId === this.property.id) {
					this.$set(this.property.photos, this.property.photos.length, data)
					this.galleryPhotos = this.property.photos
				} else {
					const propertyIndex = this.comps.findIndex(item => item.id === propertyId)
					this.$set(this.comps[propertyIndex].photos, this.comps[propertyIndex].photos.length, data)
				}

				this.notify({
					text: 'Photo saved',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not save photo',
					color: 'error'
				}, { root: true })
				throw error
			}
		},

		/**
		 * Update photo of property
		 */
		async updatePhoto(photo) {
			try {
				// Update photo in db
				const propertyId = this.galleryProperty.id
				const { data } = await propertiesPhotosApi.update(propertyId, photo)

				// Update photos locally
				if(propertyId === this.property.id) {
					this.property.photos = this.deselectPhotos(this.property.photos)
					const photoIndex = this.property.photos.findIndex(item => item.id === photo.id)
					this.$set(this.property.photos, photoIndex, data)
					this.galleryPhotos = this.property.photos
				} else {
					const propertyIndex = this.comps.findIndex(item => item.id === propertyId)
					this.comps[propertyIndex].photos = this.deselectPhotos(this.comps[propertyIndex].photos)
					const photoIndex = this.comps[propertyIndex].photos.findIndex(item => item.id === photo.id)
					this.$set(this.comps[propertyIndex].photos, photoIndex, data)
					this.galleryPhotos = this.comps[propertyIndex].photos
				}

				this.notify({
					text: 'Photo updated',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not update photo',
					color: 'error'
				}, { root: true })
			}
		},

		/**
		 * Delete photo of property
		 */
		async deletePhoto(photoId) {
			try {
				// Delete photo in db
				const propertyId = this.galleryProperty.id
				await propertiesPhotosApi.delete(propertyId, photoId)

				// Remove photo locally in models and update galleryPhotos
				if(propertyId === this.property.id) {
					const photoIndex = this.property.photos.findIndex(item => item.id === photoId)
					this.$delete(this.property.photos, photoIndex)
					this.galleryPhotos = this.property.photos
				} else {
					const propertyIndex = this.comps.findIndex(item => item.id === propertyId)
					const photoIndex = this.comps[propertyIndex].photos.findIndex(item => item.id === photoId)
					this.$delete(this.comps[propertyIndex].photos, photoIndex)
					this.galleryPhotos = this.comps[propertyIndex].photos
				}

				this.notify({
					text: 'Photo deleted',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not delete photo',
					color: 'error'
				}, { root: true })
			}
		},

		deselectPhotos(photos = []) {
			return photos.map(item => {
				return { ...item, is_best: false }
			})
		},

		async loadAssessmentDates() {
			try {
				const { data } = await assessmentDatesApi.getAll()
				this.assessmentDates = data
			} catch(error) {
				this.notify({
					text: 'Can not load Assessment Dates',
					color: 'error'
				}, { root: true })
			}
		},

		async loadAssessment(assessmentDateId) {
			try {
				const { data: [ assessment ] } = await assessmentDatesApi.getAssessments(assessmentDateId, {
					property_id: this.id,
					limit: 1,
				})
				this.assessment = assessment
			} catch(error) {
				this.notify({
					text: 'Can not load Assessment',
					color: 'error'
				}, { root: true })
			}
		},

		async updateAssessment(assessment) {
			try {
				const confirm = await this.$refs.confirm.open('Save Assessment', 'Are you sure you want to do this?', { color: 'error' })
				if(confirm) {
					const { data } = await assessmentsApi.update(assessment)
					this.assessment = data
					this.notify({
						text: 'Assessment updated',
						color: 'success'
					}, { root: true })
					this.loadSingleCMA(this.id)
				}
			} catch (error) {
				this.notify({
					text: 'Can not update Assessment',
					color: 'error'
				}, { root: true })
				throw error
			}
		},

		async loadRuleSet(assessmentDateId) {
			try {
				const { data: [ ruleSet ] } = await assessmentDatesApi.getRuleSets(assessmentDateId)
				this.ruleSet = ruleSet
			} catch(error) {
				this.notify({
					text: 'Can not load Rule Set',
					color: 'error'
				}, { root: true })
			}
		},

		getTableCompsHeaders() {
			const savedHeaders = JSON.parse(localStorage.getItem('tableCompsHeaders')) || []
			const headers = [
				...savedHeaders,
				...this.defaultTableCompsHeaders,
			]
			const uniqHeaders = uniqBy(headers, 'value')
			if(headers) {
				this.tableCompsHeaders = uniqHeaders
			}
		},
 
		resetTableCompsHeader() {
			this.tableCompsHeaders = cloneDeep(this.defaultTableCompsHeaders)
		},

		async genPdfContent() {
			return [
				{
					columns: [
						{
							width: '25%',
							stack: [
								format(new Date(), 'EEEE, MMMM d, yyyy'),
								`TOTAL RECORDS = ${this.allCompsCount}`
							],
						},
						{
							width: '50%',
							stack: [
								{
									text: `${this.countyFilter(this.property?.county)} COMPARABLES SPECIAL REPORT (1A)`.toUpperCase(),
									style: [ 'title' ],
								},
								{
									text: `${this.property?.town || this.property?.village} - (County mode)`,
									style: [ 'subtitle' ],
								},
							],
						},
						{
							width: '25%',
							stack: [
								{
									columns: [
										{
											stack: [
												' ',
												'SUBJECT',
											],
										},
										{
											stack: [
												'SEC',
												this.property?.section,
											],
										},
										{
											stack: [
												'BLOCK',
												this.property?.block,
											],
										},
										{
											stack: [
												'LOT',
												this.property?.lot,
											],
										},
									],
								},
								{
									columns: [
										'Subject ADJ/V',
										{
											text: this.$options.filters.currency(this.assessment_results?.current_market_value),
											bold: true,
										},
									],
								}
							],
						},
					],
					columnGap: 10
				},
				{
					text: 'Good Comps',
					style: [ 'tableTitle' ],
				},
				GoodBadReportService.composePdfTable(
					this.pdfTableAllHeaders,
					[ this.property, ...this.good_comps_properties.slice(0, 21) ]
				),
				{
					text: `TOTAL GOOD COMPS = ${this.goodCompsCount}`,
				},
				{
					text: 'Bad Comps',
					style: [ 'tableTitle' ],
				},
				GoodBadReportService.composePdfTable(
					this.pdfTableAllHeaders,
					[ this.property, ...this.bad_comps_properties.slice(0, 9) ]
				),
				{
					text: `TOTAL BAD COMPS = ${this.badCompsCount}`,
					columns: [
						{
							text: `TOTAL BAD COMPS = ${this.badCompsCount}`,
						},
						{
							width: '25%',
							columns: [
								'Subject ADJ/V',
								{
									text: this.$options.filters.currency(this.assessment_results?.current_market_value),
									bold: true,
								},
							]
						},
					]
				},
				{
					columns: [
						{
							stack: [
								'GOOD AVERAGE ADJ/V 1-4',
								'GOOD AVERAGE ADJ/V 1-8',
								'GOOD AVERAGE ADJ/V 1-12',
							],
						},
						{
							stack: [
								this.$options.filters.bignum(Number(this.average_ranges?.good?.['4']?.proposed_assessment_value)),
								this.$options.filters.bignum(Number(this.average_ranges?.good?.['8']?.proposed_assessment_value)),
								this.$options.filters.bignum(Number(this.average_ranges?.good?.['12']?.proposed_assessment_value)),
							],
						},
						{
							stack: [
								this.$options.filters.bignum(Number(this.average_ranges?.good?.['4']?.claimed_market_value?.toFixed(0))),
								this.$options.filters.bignum(Number(this.average_ranges?.good?.['8']?.claimed_market_value?.toFixed(0))),
								this.$options.filters.bignum(Number(this.average_ranges?.good?.['12']?.claimed_market_value?.toFixed(0))),
							],
						},
						{
							stack: [
								'ALL AVERAGE ADJ/V 1-4',
								'ALL AVERAGE ADJ/V 1-8',
								'ALL AVERAGE ADJ/V 1-12',
							],
						},
						{
							stack: [
								this.$options.filters.bignum(Number(this.average_ranges?.misc?.['4']?.proposed_assessment_value)),
								this.$options.filters.bignum(Number(this.average_ranges?.misc?.['8']?.proposed_assessment_value)),
								this.$options.filters.bignum(Number(this.average_ranges?.misc?.['12']?.proposed_assessment_value)),
							],
						},
						{
							stack: [
								this.$options.filters.bignum(Number(this.average_ranges?.misc?.['4']?.claimed_market_value?.toFixed(0))),
								this.$options.filters.bignum(Number(this.average_ranges?.misc?.['8']?.claimed_market_value?.toFixed(0))),
								this.$options.filters.bignum(Number(this.average_ranges?.misc?.['12']?.claimed_market_value?.toFixed(0))),
							],
						},
					],
				},
				{
					text: 'Same Street/Block',
					style: [ 'tableTitle' ],
				},
				GoodBadReportService.composePdfTable(
					this.pdfTableAllHeaders,
					[ this.property, ...this.nearbyComps.slice(0, 12) ]
				),
				await this.composePdfPropDetailedRow(this.property),
				await this.composePdfPhotoRow(this.good_comps_properties.slice(0, 5)),
				await this.composePdfPhotoRow(this.bad_comps_properties.slice(0, 5).slice(0, 5)),
				await this.composePdfPhotoRow(this.nearbyComps.slice(0, 5).slice(0, 5)),
			]
		},

		/**
		 * Add comp field to highlighted_fields array
		 * This array used to hightlight these fields
		 * on the table and PDF
		 * @param {Object} comp property model
		 * @param {String} field property field key
		 */
		highlightField(comp, field) {
			const index = this.comps.findIndex(item => item.id === comp.id)
			if(!comp.highlighted_fields) {
				comp.highlighted_fields = []
			}

			const highlightedIndex = comp.highlighted_fields.indexOf(field)
			if(highlightedIndex >= 0) {
				this.$delete(comp.highlighted_fields, highlightedIndex)
			} else {
				comp.highlighted_fields.push(field)
			}
			
			if(comp.id == this.id) {
				this.$set(this.property, 'highlighted_fields', comp.highlighted_fields)
			} else {
				this.$set(this.comps, index, comp)
			}

			this.$forceUpdate()
		},

		/**
		 * Define is field is highlighted and add yellow class
		 * @param {Object} comp property model
		 * @param {String} field property field key
		 */
		highlightedClass(comp, field) {
			return 	comp.highlighted_fields &&
					comp.highlighted_fields.indexOf(field) >= 0 
						? 'yellow'
						: ''
		},

		/**
		 * Show Log Comps on map
		 * @param {String} filter filter
		 */
		showLogComps(filter) {
			this.tab = 1
			this.isShowLogComps = true
			this.mapCompFilter = {
				text: '',
				value: filter,
			}
		},

		// mapDataLoadHandler(e) {
		// 	if(e.sourceId === 'comp-features') {
		// 		this.mapInited(true)
		// 	}
		// },

		/**
		 * Create Single CMA Workup
		 */
		async createCMAWorkup() {
			try {
				this.loadingWorkup = true
				const cma_payload = {
					subject: this.property,
					average_ranges: this.average_ranges,
					assessment_date_id: this.assessment_date_id,
					assessment_results: {
						...this.assessment_results,
						proposed_assessment_value: this.proposedAssessment,
					},
					all_comps: this.comps, //TODO: internal data was changed, update fields
					assessment: this.assessment,
				}
				const workup = {
					property_id: this.id,
					is_primary: true,
					cma_payload,
				}
				await this.generatePrintPDF()
				const cmaPdfBlob = await this.$refs.cmaPDF.getBlob()

				this.pdfContent = await this.genPdfContent()
				await this.$nextTick()
				const goodBadPdfBlob = await this.$refs.goodBadReport.getBlob()

				const formData = new FormData()
				formData.append('data', JSON.stringify(workup))
				formData.append('report_file', cmaPdfBlob, `${this.id}.pdf`)
				formData.append('good_bad_report_file', goodBadPdfBlob, `${this.id}.pdf`)

				// Create Workup
				const { data } = await singleCmaWorkupsApi.create(formData)

				// Download Evidence Package for current Workup
				await this.downloadEvidencePackage(data.id)

				this.notify({
					text: 'CMA Workup created',
					color: 'success'
				}, { root: true })
			} catch (error) {
				const message = error?.response?.data?.message || error
				this.notify({
					text: `Can not create CMA Workup. ${message}`,
					color: 'error'
				}, { root: true })
			} finally {
				this.loadingWorkup = false
			}
		},

		/**
		 * Open PDF URL in new window
		 */
		async downloadEvidencePackage(workupId) {
			try {
				window.open(`${this.VUE_APP_API}single-cma-workups/${workupId}/evidence-package`, '_blank');
			} catch (error) {
				this.notify({
					text: 'Can not download Evidence Package',
					color: 'error'
				}, { root: true })
			}
		},

		/**
		 * Reset CMA page for new property
		 */
		reset() {
			this.printFieldTop = ''
			this.printFieldBottom = ''
			this.assessment.override_value = 0
		},

		/**
		 * Load all data on init and on prop change
		 */
		loadData() {
			this.reset()
			this.loadCounties()
			this.loadAdjustments()
			this.loadAssessmentDates()
			this.loadSingleCMA(this.id)
			this.loadNearbyCMA(this.id)
			document.addEventListener('keydown', this.printHadler)
			this.getTableCompsHeaders()
		},

	},
	watch: {
		'id': {
			immediate: true,
			handler: 'loadData',
		},
		'assessment_date_id'(newVal) {
			this.$router.push({
				name: 'cma-compare',
				params: {
					id: this.id,
				},
				query: {
					'assessment-date': newVal,
				},
			})
			this.loadAssessment(newVal)
			this.loadRuleSet(newVal)
		},
		'property.county'(newVal) {
			if (newVal) {
				this.loadSettings(newVal)
			}
		},
		tableCompsHeaders:{
			deep: true,
			handler(newVal) {
				localStorage.setItem('tableCompsHeaders', JSON.stringify(newVal))
			},
		},
		'tab'(newVal) {
			// resize map if map tab open
			if (newVal === 1) {
				setTimeout(() => {
					this.$refs.map.map.resize()
				}, 1)
			}
		},
	},
	created() {
		this.mapStyle = this.mapStyles.find(item => item.text === this.mapStyle.text)
	},
	beforeDestroy() {
        document.removeEventListener('keydown', this.printHadler)
    },
}
</script>

<style lang="scss">
.cma-compare-wrap {
	position: relative;

	.cma-compare-header {
		position: sticky;
		top: 0;
		z-index: 3;
	}
}

.map-controls {
	position: absolute;
	z-index: 2;
}

.v-application .bad-comparison-table-cell {
	background-color: #ffebee !important;

	&.lighten-4 {
		background-color: #fecdd2 !important;
	}
}

#comp-selection-table.v-data-table {
	th:nth-child(1),
	td:nth-child(1),
	th:nth-child(2),
	td:nth-child(2) {
		padding: 0;
	}
}
</style>
