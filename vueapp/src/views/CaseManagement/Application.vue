<template>
	<div>
		<v-toolbar
			class="has-border-bottom"
			dense
			elevation="0"
			outlined>
			<v-app-bar-nav-icon
				@click="toggleSidebar">
			</v-app-bar-nav-icon>
			<h1 class="title font-weight-bold mr-12 pr-12">Applications</h1>

			<v-tabs
				v-if="isControlable"
				ref="tabs"
				v-model="tab"
				class="ml-12">
				<template v-for="item in filteredStatuses">
					<v-tab
						v-if="item.count"
						:key="item.id"
						:to="{
							name: $route.name,
							params: {
								...$route.params,
								status: item.key,
								id: item.applications && item.applications[0],
							},
						}"
						class="mx-4">
						{{ item.text }} ({{ item.count }})
					</v-tab>
					<v-tab
						v-else
						:key="item.id"
						disabled
						class="mx-4">
						{{ item.text }} (0)
					</v-tab>
				</template>
			</v-tabs>

			<v-spacer></v-spacer>

			<v-btn
				color="success"
				outlined
				@click="isApplicationCreateForm = true">
				Create new application
			</v-btn>
		</v-toolbar>
		<v-container
			v-if="application.id">

			<div class="application-grid"
				:class="{
					'application-grid-online': !isPhysical,
					'application-grid-online--open': !isPhysical && showApplicationForm,
				}">

				<div id="application-nav">
					<v-card
						elevation="0"
						outlined>
						<v-row class="mx-0">
							<v-col>
								<v-btn
									v-if="status === 'reviewed' && isEditable"
									color="success"
									outlined
									@click="approveApplication(application)">
									Approve
								</v-btn>
								<v-btn
									v-else-if="isEditable"
									color="success"
									outlined
									:disabled="!application.signature_base64_encoded && !isPhysical"
									@click="reviewApplication(application)">
									Review
								</v-btn>
							</v-col>
							<v-col>
								<v-btn
									color="primary"
									outlined
									:to="{
										name: $route.name,
										params: {
											...$route.params,
											id: prevApplication,
										},
									}"
									:disabled="!prevApplication || !isControlable">
									Previous
								</v-btn>
							</v-col>
							<v-col>
								<v-btn
									color="primary"
									outlined
									:to="{
										name: $route.name,
										params: {
											...$route.params,
											id: nextApplication,
										},
									}"
									:disabled="!nextApplication || !isControlable">
									Next
								</v-btn>
							</v-col>
							<v-col>
								<v-btn
									v-if="isEditable"
									color="error"
									outlined
									@click="showRejectDialog">
									Reject
								</v-btn>
							</v-col>
							<v-col
								cols="auto">
								<v-autonumeric
									v-model.number="applicationNumber"
									:suffix="`/${applications.length}`"
									:an-options="{
										decimalPlaces: 0,
										minimumValue: 1,
										maximumValue: applications.length,
									}"
									outlined
									dense
									hide-details
									:disabled="!isControlable"
									class="application-number-input pa-0"
									style="width: 88px;">
								</v-autonumeric>
							</v-col>
						</v-row>
					</v-card>
				</div>

				<div id="application-toggle-form"
					v-if="!isPhysical">
					<v-card
						elevation="0"
						outlined
						class="py-1">
						<v-card-title>
							Application Form
							<v-spacer></v-spacer>
							<v-btn
								icon
								@click="showApplicationForm = !showApplicationForm">
								<v-icon>
									{{ showApplicationForm ? 'mdi-chevron-right' : 'mdi-chevron-down' }}
								</v-icon>
							</v-btn>
						</v-card-title>
					</v-card>
				</div>

				<div id="application-roll-info"
					v-if="property">

					<roll-info-physical
						v-if="isPhysical"
						:application="application">
					</roll-info-physical>

					<roll-info-online
						v-else
						:application="application">
					</roll-info-online>
				</div>

				<div id="application-app-info"
					v-if="property">
					
					<v-form
						ref="applicationInfo"
						v-model="isApplicationValid"
						:disabled="!isEditable"
						style="height: 100%;">

						<v-card v-if="isPhysical"
								height="100%"
								elevation="0"
								outlined>
								<v-card-title>
									Application Info
									<v-spacer></v-spacer>
									<v-btn
										color="primary"
										outlined
										small
										:loading="isFindPropertyLoading"
										:disabled="!isControlable"
										@click="findProperty">
										Find match
									</v-btn>
								</v-card-title>
								<v-divider></v-divider>

								<exist-client-alert
									v-if="isExistingClient"
									:clientid="client.id">
								</exist-client-alert>
								
								<v-container
									class="pt-1">
									<v-row>
										<v-col
											cols="7"
											class="py-0">
											<v-row>
												<v-col
													cols="4"
													class="py-0">
													<v-text-field
														ref="applicationFirstName"
														v-model="application.first_name"
														label="First Name"
														:rules="applicationFirstNameRules"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationFirstName && !$refs.applicationFirstName.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
												<v-col
													cols="5"
													class="py-0">
													<v-text-field
														ref="applicationLastName"
														v-model="application.last_name"
														label="Last Name"
														:rules="applicationLastNameRules"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationLastName && !$refs.applicationLastName.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
												<v-col
													cols="3"
													class="py-0">
													<v-text-field
														v-model="application.tax_year"
														label="Tax year"
														hide-details>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="9"
													class="py-0 mt-4">
													<v-text-field
														ref="applicationAddressLine1"
														v-model="application.address_line1"
														label="Property Address"
														:rules="applicationAddressLine1Rules"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationAddressLine1 && !$refs.applicationAddressLine1.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
												<v-col
													cols="3"
													class="py-0 mt-4">
													<!-- TODO: add model -->
													<v-text-field
														label="Unit #"
														hide-details>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<v-text-field
														ref="applicationAddressLine2"
														v-model="application.address_line2"
														:rules="applicationAddressLine2Rules"
														class="pt-0 mt-0"
														success
														hide-details>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="7"
													class="py-0">
													<v-text-field
														ref="applicationAddressCity"
														v-model="application.address_city"
														:rules="applicationCityRules"
														class="pt-0 mt-0"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationAddressCity && !$refs.applicationAddressCity.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
												<v-col
													cols="2"
													class="py-0">
													<v-text-field
														ref="applicationAddressState"
														v-model="application.address_state"
														class="pt-0 mt-0"
														:rules="applicationStateRules"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationAddressState && !$refs.applicationAddressState.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
												<v-col
													cols="3"
													class="py-0">
													<v-text-field
														ref="applicationAddressZip"
														v-model="application.address_zip"
														class="pt-0 mt-0"
														:rules="applicationZipRules"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationAddressZip && !$refs.applicationAddressZip.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0 mt-4">
													<v-text-field
														v-model="application.mailing_line1"
														label="Mailing Address"
														:class="{
															'v-input--error': !application.mailing_line1,
														}"
														hide-details>
													</v-text-field>
													<v-text-field
														v-model="application.mailing_line2"
														class="pt-0 mt-0"
														hide-details>
													</v-text-field>
													<v-text-field
														v-model="application.mailing_line3"
														class="pt-0 mt-0"
														hide-details>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row
												dense
												class="mt-3">
												<v-col
													cols="6"
													class="py-0">
													<v-text-field
														v-model="application.apn"
														label="Legal ID"
														hide-details>
													</v-text-field>
												</v-col>
												<v-col
													cols="6"
													class="py-0">
													<v-select
														v-model="application.county"
														:items="counties"
														label="County"
														item-value="id"
														item-text="name"
														outlined
														dense
														hide-details
														class="mt-1 pt-3">
													</v-select>
												</v-col>
											</v-row>

											<!-- <v-row
												class="mt-2">
												<v-col class="py-0">
													<v-text-field
														v-model="application.district"
														label="Dist">
													</v-text-field>
												</v-col>
												<v-col class="py-0">
													<v-text-field
														v-model="application.section"
														label="Sec">
													</v-text-field>
												</v-col>
												<v-col class="py-0">
													<v-text-field
														v-model="application.block"
														label="Block">
													</v-text-field>
												</v-col>
												<v-col class="py-0">
													<v-text-field
														v-model="application.lot"
														label="Lot">
													</v-text-field>
												</v-col>
											</v-row> -->
										</v-col>

										<v-col
											cols="5"
											class="py-0">
											<div
												class="d-flex mt-4"
												style="min-height: 1.625em;">
												<v-btn
													v-if="applicationChanged"
													color="success"
													outlined
													small
													@click="updateApplication(application)">
													Save
												</v-btn>
												<v-spacer></v-spacer>
												<v-btn
													v-if="applicationChanged"
													color="error"
													outlined
													small
													@click="resetApplication">
													Discard
												</v-btn>
											</div>
											<!-- <v-row>
												<v-col
													cols="8"
													class="py-0 mt-5">
													<v-text-field
														v-model="application.initials"
														label="Initial"
														:class="{ 'v-input--error' : !applicantInitialsMatch }">
													</v-text-field>
												</v-col>
											</v-row> -->

											<v-row
												class="mt-1">
												<v-col
													cols="8"
													class="py-0">
													<v-mask-input
														ref="applicationPhone1"
														v-model="application.phone_number_1"
														label="Phone 1"
														:mask="'(999) 999-9999'"
														:rules="phoneRulesRequired"
														:class="{
															'v-input--error': !application.phone_number_1,
														}"
														hide-details>
														<template #append
															v-if="$refs.applicationPhone1 && !$refs.applicationPhone1.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-mask-input>
												</v-col>
												<v-col
													cols="4"
													class="py-0">
													<span class="font-weight-bold">SMS</span>
													<v-checkbox
														v-model="application.sms_alerts_1"
														class="mt-0 ml-1 pt-0"
														hide-details>
													</v-checkbox>
												</v-col>
											</v-row>

											<v-row
												class="mt-2">
												<v-col
													cols="8"
													class="py-0">
													<v-mask-input
														ref="applicationPhone2"
														v-model="application.phone_number_2"
														label="Phone 2"
														:rules="phoneRules"
														:mask="'(999) 999-9999'">
														<template #append
															v-if="$refs.applicationPhone2 && !$refs.applicationPhone2.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-mask-input>
												</v-col>
												<v-col
													cols="4"
													class="py-0">
													<span class="font-weight-bold">SMS</span>
													<v-checkbox
														v-model="application.sms_alerts_2"
														class="mt-0 ml-1 pt-0">
													</v-checkbox>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<v-text-field
														ref="applicationEmail"
														v-model="application.email.email_address"
														label="Email"
														:rules="applicationEmailRules"
														:class="{
															'v-input--error': !application.email.email_address,
														}">
														<template #append
															v-if="$refs.applicationEmail && !$refs.applicationEmail.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<v-select
														v-model="application.application_type_id"
														:items="applicationTypes"
														label="Application Type"
														outlined
														dense
														item-value="id"
														item-text="description"
														class="mt-2">
													</v-select>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<v-select
														v-model="application.marketing_code_id"
														:items="marketingCodes"
														label="Marketing Code"
														outlined
														dense
														item-value="id"
														item-text="name"
														class="mt-2">
													</v-select>
												</v-col>
											</v-row>
										</v-col>
									</v-row>

									<v-row>
										<v-col
											cols="5"
											class="py-0">
											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<!-- TODO: add model -->
													<!-- <v-text-field
														label="Region"
														disabled>
													</v-text-field> -->
												</v-col>
											</v-row>
										</v-col>
									</v-row>

									<v-row class="mt-2">
										<v-col
											cols="7"
											class="py-0">
											<v-row
												dense>
												<v-col
													cols="4"
													class="py-0">
													<v-text-field
														v-model="property.property_class"
														label="Building Class"
														hide-details
														disabled>
													</v-text-field>
												</v-col>
												<v-col
													cols="3"
													class="py-0">
													<v-text-field
														v-model="assessment.swiss_code"
														label="Swiss Code"
														hide-details
														disabled>
													</v-text-field>
												</v-col>
												<v-col
													cols="5"
													class="py-0">
													<v-text-field
														v-model="property.school_district"
														label="School District"
														hide-details
														disabled>
													</v-text-field>
												</v-col>
											</v-row>
										</v-col>

										<v-col
											cols="5"
											class="py-0">
											<v-row>
												<v-col
													cols="8"
													class="py-0">
													<v-text-field
														v-if="application.source"
														v-model="application.source.name"
														label="Source"
														hide-details
														disabled>
													</v-text-field>
												</v-col>
											</v-row>
										</v-col>
									</v-row>

									<v-row>
										<v-col>
											<v-btn
												color="primary"
												outlined
												small
												class="mr-4"
												:loading="isAppRepairLoading"
												:disabled="!isControlable"
												@click="copyAppRepairLink(id)">
												Copy Repair Link
											</v-btn>
											<v-btn
												color="primary"
												outlined
												small
												:loading="isAppRepairLoading"
												:disabled="!isControlable"
												@click="sendMailAppRepairLink(id)">
												<v-icon>
													mdi-email-outline
												</v-icon>
											</v-btn>
										</v-col>
									</v-row>
								</v-container>
						</v-card>

						<v-card v-else
								height="100%"
								elevation="0"
								outlined>
								<v-card-title>
									Application Info
								</v-card-title>
								<v-divider></v-divider>

								<exist-client-alert
									v-if="isExistingClient"
									:clientid="client.id">
								</exist-client-alert>

								<v-container
									class="pa-0">
									<v-row class="ma-0">
										<v-col cols="7"
											class="has-border-right">
											<v-row>
												<v-col
													cols="4"
													class="py-0">
													<v-text-field
														ref="applicationFirstName"
														v-model="application.first_name"
														label="First Name"
														:rules="applicationFirstNameRules"
														@input="$refs.applicationInfo.validate()"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationFirstName && !$refs.applicationFirstName.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
												<v-col
													cols="5"
													class="py-0">
													<v-text-field
														ref="applicationLastName"
														v-model="application.last_name"
														label="Last Name"
														:rules="applicationLastNameRules"
														@input="$refs.applicationInfo.validate()"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationLastName && !$refs.applicationLastName.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
												<v-col
													cols="3"
													class="py-0">
													<v-text-field
														v-model="application.tax_year"
														label="Tax year"
														hide-details>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="3"
													class="py-0">
													<v-text-field
														ref="applicationInitials"
														v-model="application.initials"
														label="Initial"
														:rules="applicationInitialsRules"
														success
														hide-details>
														<template #append
															v-if="$refs.applicationInitials && !$refs.applicationInitials.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0 mt-4">
													<v-text-field
														v-model="application.mailing_line1"
														label="Mailing Address"
														:class="{
															'v-input--error': !application.mailing_line1,
														}"
														hide-details>
													</v-text-field>
													<v-text-field
														v-model="application.mailing_line2"
														class="pt-0 mt-0"
														hide-details>
													</v-text-field>
													<v-text-field
														v-model="application.mailing_line3"
														class="pt-0 mt-0"
														hide-details>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="9"
													class="">
													<v-select
														v-model="application.application_type_id"
														:items="applicationTypes"
														label="Application Type"
														outlined
														dense
														item-value="id"
														item-text="description"
														class="mt-2">
													</v-select>
												</v-col>

												<v-col
													cols="3"
													class="">
													<v-text-field
														v-if="application.source"
														v-model="application.source.name"
														label="Source"
														hide-details
														disabled>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col>
													<v-btn
														color="primary"
														outlined
														small
														class="mr-4"
														:loading="isAppRepairLoading"
														:disabled="!isControlable"
														@click="copyAppRepairLink(id)">
														{{ (application.source_id === 3 && !application.signature_base64_encoded) ?
															'Copy sign url' : 'Copy Repair Link' }}
													</v-btn>
													<v-btn
														v-if="application.source_id === 3 && !application.signature_base64_encoded"
														color="primary"
														outlined
														small
														:disabled="!isControlable"
														@click="sendSignEmail(id)">
														<v-icon left>
															mdi-email-outline
														</v-icon>
														Send Sign Email
													</v-btn>
													<v-btn
														v-else
														color="primary"
														outlined
														small
														:loading="isAppRepairLoading"
														:disabled="!isControlable"
														@click="sendMailAppRepairLink(id)">
														<v-icon>
															mdi-email-outline
														</v-icon>
													</v-btn>
												</v-col>
											</v-row>

											<v-row>
												<v-col>
													<div
														class="d-flex mt-7"
														style="min-height: 1.625em;">
														<v-btn
															v-if="applicationChanged"
															color="success"
															outlined
															small
															@click="updateApplication(application)">
															Save
														</v-btn>
														<v-spacer></v-spacer>
														<v-btn
															v-if="applicationChanged"
															color="error"
															outlined
															small
															@click="resetApplication">
															Discard
														</v-btn>
													</div>
												</v-col>
											</v-row>
										</v-col>

										<v-col cols="5">
											<v-row>
												<v-col
													cols="8"
													class="py-0">
													<v-mask-input
														ref="applicationPhone1"
														v-model="application.phone_number_1"
														label="Phone 1"
														:mask="'(999) 999-9999'"
														:class="{
															'v-input--error': !application.phone_number_1,
														}"
														:rules="phoneRulesRequired"
														hide-details>
														<template #append
															v-if="$refs.applicationPhone1 && !$refs.applicationPhone1.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-mask-input>
												</v-col>
												<v-col
													cols="4"
													class="py-0">
													<span class="font-weight-bold">SMS</span>
													<v-checkbox
														v-model="application.sms_alerts_1"
														class="mt-0 ml-1 pt-0"
														hide-details>
													</v-checkbox>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="8"
													class="py-0">
													<v-mask-input
														ref="applicationPhone2"
														v-model="application.phone_number_2"
														label="Phone 2"
														:rules="phoneRules"
														:mask="'(999) 999-9999'">
														<template #append
															v-if="$refs.applicationPhone2 && !$refs.applicationPhone2.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-mask-input>
												</v-col>
												<v-col
													cols="4"
													class="py-0">
													<span class="font-weight-bold">SMS</span>
													<v-checkbox
														v-model="application.sms_alerts_2"
														class="mt-0 ml-1 pt-0">
													</v-checkbox>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<v-text-field
														ref="applicationEmail"
														v-model="application.email.email_address"
														label="Email"
														:rules="applicationEmailRules"
														:class="{
															'v-input--error': !application.email.email_address,
														}">
														<template #append
															v-if="$refs.applicationEmail && !$refs.applicationEmail.valid">
															<v-icon
																color="error">
																mdi-exclamation-thick
															</v-icon>
														</template>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<v-select
														v-model="application.marketing_code_id"
														:items="marketingCodes"
														label="Marketing Code"
														outlined
														dense
														item-value="id"
														item-text="name"
														class="mt-2">
													</v-select>
												</v-col>
											</v-row>

											<v-row no-gutters
												class="mb-5">
												<v-col
													cols="5"
													class="py-0">
													<v-select
														v-model="application.payment_type_id"
														:items="paymentTypes"
														label="Payment Type"
														outlined
														dense
														item-value="id"
														item-text="description"
														class="mt-2"
														hide-details>
													</v-select>
												</v-col>
												<v-col
													cols="1"
													class="align-self-center text-center">
													<span class="pa-1">-</span>
												</v-col>
												<v-col
													cols="6"
													class="py-0">
													<v-select
														v-model="application.payment_status_id"
														:items="paymentStatuses"
														label="Payment Status"
														:rules="[
															v => v !== 1 || 'This application is unpaid',
														]"
														outlined
														dense
														item-value="id"
														item-text="name"
														class="mt-2"
														hide-details>
													</v-select>
												</v-col>
											</v-row>

											<v-row v-if="showBillingAmount">
												<v-col>
													<v-text-field
														v-if="application.billing"
														v-model.number="application.billing.amount"
														label="Payment Amount"
														outlined
														dense>
													</v-text-field>
												</v-col>
											</v-row>

											<v-row v-if="application.payment_status_id !== 2">
												<v-col>
													<copy-payment-link
														:application-id="application.id">
													</copy-payment-link>
												</v-col>
											</v-row>

											<v-row>
												<v-col
													cols="12"
													class="py-0">
													<div class="d-flex mb-2">
														<b>Signature</b>
														<v-spacer></v-spacer>
														<v-input
															:error="!application.signature_approved"
															:error-messages="application.signature_approved ? null : `Signature is not approved`"
															class="text-right">
															<template #default>
																<v-spacer></v-spacer>
																<v-btn
																	class="black--text justify-self-end"
																	color="success"
																	:outlined="!application.signature_approved"
																	small
																	elevation="0"
																	:disabled="!isControlable || !application.signature_base64_encoded"
																	@click="toggleSignatureApproved">
																	<v-icon left small>mdi-check</v-icon>
																	{{ application.signature_approved ? 'Approved' : 'Approve' }}
																</v-btn>
															</template>
														</v-input>
													</div>
													<v-sheet
														rounded
														outlined>
														<v-img
															:src="`data:image/jpeg;base64, ${application.signature_base64_encoded}`">
														</v-img>
													</v-sheet>
												</v-col>
											</v-row>
										</v-col>
									</v-row>
								</v-container>
						</v-card>
					</v-form>
				</div>

				<div id="application-app-form"
					v-if="isPhysical || (!isPhysical && showApplicationForm)">
					<application-form
						v-model="application.scan_base64_encoded">
					</application-form>
				</div>

				<div id="application-history">
					<v-card
						elevation="0"
						outlined>
						<v-card-title class="has-border-bottom">
							Previous History
						</v-card-title>
						<v-container>
							<v-data-table
								:headers="applicationHistoryHeaders"
								:items="applicationHistory"
								hide-default-footer
								fixed-header
								:items-per-page="-1"
								height="12.6em"
								dense>

								<template #item.takeover="{ item }">
									<v-simple-checkbox
										:value="compareTakeover(item)"
										@input="(e) => takeoverApplication(e, item)">
									</v-simple-checkbox>
								</template>

								<template #item.first_full_name="{ item }">
									{{ item.first_full_name }} {{ item.second_full_name }}
								</template>

								<template #item.previous_client="{ item }">
									{{ item.applicant_name ? 'Yes' : '-' }}
								</template>

								<template #item.applicant_name="{ item }">
									{{ item.applicant_name || '-' }}
								</template>

							</v-data-table>
						</v-container>
					</v-card>
				</div>

				<div id="application-comments">
					<comments-card
						:items="notes"
						@create="createNote">
					</comments-card>
				</div>
			</div>

			<v-dialog
				v-model="rejectDialog"
				max-width="500">
				<v-card
					outlined>
					<v-form
						v-model="rejectFormValid">
						<v-card-title
							class="has-border-bottom justify-center error--text">
							Reject
						</v-card-title>
						<v-container
							class="pa-4">
							<v-row
								class="justify-center">
								<v-col
									cols="8">
									<p>Please select the reason for rejecting this application:</p>
									<v-select
										v-model="application.reject_reason_id"
										:items="rejectReasons"
										item-value="id"
										item-text="name"
										:rules="[v => !!v || 'Reason is required']"
										:width="270"
										required
										outlined
										hide-details
										dense>
									</v-select>
								</v-col>
							</v-row>
						</v-container>
						<v-card-actions
							class="pa-5">
							<v-btn
								color="success"
								outlined
								@click="rejectApplication(application)"
								:disabled="!rejectFormValid">
								Reject
							</v-btn>
							<v-spacer></v-spacer>
							<v-btn
								v-if="isAdmin"
								color="error"
								outlined
								@click="fullyRejectApplication(application)"
								:disabled="!rejectFormValid">
								Fully Reject
							</v-btn>
							<v-spacer></v-spacer>
							<v-btn
								color="primary"
								outlined
								@click="rejectDialog = false">
								Cancel
							</v-btn>
						</v-card-actions>
					</v-form>
				</v-card>
			</v-dialog>

			<confirm ref="confirm"></confirm>

			<confirm ref="errorsConfirm">
				<template #default>
					<application-errors
						:errors="applicationErrors">
					</application-errors>
				</template>
			</confirm>

		</v-container>
		<v-container
			v-else
			class="text-center">
			<h2 class="grey--text">Nothing to show</h2>
		</v-container>

		<application-create-form
			v-model="isApplicationCreateForm"
			@create="loadCaseInfo">
		</application-create-form>

		<v-overlay :value="loading">
			<v-progress-circular
				:size="70"
				:width="7"
				color="primary"
				indeterminate>
			</v-progress-circular>
		</v-overlay>

	</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { apiFactory } from '../../api/apiFactory'
import { isEqual, cloneDeep, debounce } from 'lodash'

import Confirm from '../../components/Confirm'
import VMaskInput from '../../components/VMaskInput'
import RollInfoOnline from '../../components/Applications/RollInfoOnline'
import RollInfoPhysical from '../../components/Applications/RollInfoPhysical'
import ApplicationForm from '../../components/Applications/ApplicationForm'
import CommentsCard from '../../components/Applications/CommentsCard'
import ExistClientAlert from '../../components/Applications/ExistClientAlert'
import ApplicationErrors from '../../components/Applications/ApplicationErrors'
import ApplicationCreateForm from '../../components/Applications/ApplicationCreateForm'
import CopyPaymentLink from '../../components/Applications/CopyPaymentLink'

import countyFilter from '../../mixins/countyFilter'

const applicationsApi = apiFactory.get('applications')
const applicationNotesApi = apiFactory.get('application-notes')
const applicationHistoryApi = apiFactory.get('application-history')
const propertiesApi = apiFactory.get('properties')
const takeoversApi = apiFactory.get('takeovers')

export default {
	components: {
		Confirm,
		VMaskInput,
		RollInfoOnline,
		RollInfoPhysical,
		ApplicationForm,
		CommentsCard,
		ExistClientAlert,
		ApplicationErrors,
		ApplicationCreateForm,
		CopyPaymentLink,
	},
	props: {
		status: {
			type: String,
			required: true,
		},
		id: {
			type: Number,
			required: true,
		},
	}, 
	mixins: [
		countyFilter,
	],
	data: () => ({
		VUE_APP_CUSTOMER_SITE_URL: process.env.VUE_APP_CUSTOMER_SITE_URL,
		tab: 0,
		application: {},
		applicationOriginal: {},
		notes: [],
		applicationHistory: [],
		rejectDialog: false,
		rejectFormValid: true,
		scanViewLocked: false,
		isFindPropertyLoading: false,
		loading: false,
		showApplicationForm: false,
		isApplicationValid: false,
		isAppRepairLoading: false,
		phoneRulesRequired: [
			v => (v ? v.length === 10 : true) || 'Please use valid phone number',
			v => !!v || 'Phone number is required',
		],
		phoneRules: [
			v => (v ? v.length === 10 : true) || 'Please use valid phone number',
		],
		isApplicationCreateForm: false,
	}),
	computed: {
		...mapGetters('auth', [
			'isAdmin',
			'isMember',
		]),
		...mapGetters('applications', [
			'statuses',
		]),
		...mapGetters('counties', [
			'counties',
		]),
		...mapGetters('applicationTypes', [
			'applicationTypes',
		]),
		...mapGetters('paymentTypes', [
			'paymentTypes',
		]),
		...mapGetters('paymentStatuses', [
			'paymentStatuses',
		]),
		...mapGetters('marketingCodes', [
			'marketingCodes',
		]),
		...mapGetters('rejectReasons', [
			'rejectReasons',
		]),
		filteredStatuses() {
			return this.statuses.filter(item => item.show)
		},
		isEditable() {
			return (this.isAdmin || this.isMember) && this.applicationStatus?.show
		},
		isControlable() {
			return this.applicationStatus?.show
		},
		applicationStatus() {
			return this.statuses.find(item => item.key === this.status)
		},
		applications() {
			return this.applicationStatus?.applications || {}
		},
		applicationIndex() {
			return this.applications.indexOf(this.id)
		},
		applicationNumber: {
			get() {
				return this.applicationIndex + 1
			},
			set(val) {
				return this.bouncedRouteToApplication(val - 1)
			},
		},
		applicationChanged() {
			return !isEqual(this.application, this.applicationOriginal)
		},
		prevApplication() {
			return this.applications[this.applicationIndex - 1]
		},
		nextApplication() {
			return this.applications[this.applicationIndex + 1]
		},
		assessment() {
			return this.application?.assessment || {}
		},
		property() {
			return this.application?.property || {}
		},
		client() {
			return this.application?.client || {}
		},
		isExistingClient() {
			return this.client?.type_id === 2
		},
		lastOwners() {
			return this.property?.owners?.[0] || {}
		},
		lastOwnersNames() {
			const lastOwnersNames = [ this.lastOwners?.first_full_name, this.lastOwners?.second_full_name ]
			return lastOwnersNames || []
		},
		applicantFirstNameMatch() {
			const regex = new RegExp('\\b' + this.application?.first_name + '\\b', 'gi')
			return this.lastOwnersNames?.some(name => name?.match(regex)) || false
		},
		applicantLastNameMatch() {
			const regex = new RegExp('\\b' + this.application?.last_name + '\\b', 'gi')
			return this.lastOwnersNames?.some(name => name?.match(regex)) || false
		},
		applicantInitialsMatch() {
			const chars = this.application?.initials?.split('')
			const searchString = chars?.map(char => `(${char}\\w*\\s*?\\b)`).join('')
			const fullName = `${this.application.first_name} ${this.application.last_name}`
			const regex = new RegExp(searchString, 'gi')
			return fullName.match(regex) || false
		},
		applicantAddressLine1Match() {
			const regex = new RegExp('\\b' + this.application?.address_line1 + '\\b', 'gi')
			return this.property?.address_line_1?.match(regex) || false
		},
		applicantAddressLine2Match() {
			const appData = this.application?.address_line2
			const propData = this.property?.address_line_2
			if(appData && propData) {
				const regex = new RegExp('^' + appData + '$', 'gi')
				return propData?.match(regex) || false
			}
			return true
		},
		applicantAddressCityMatch() {
			const regex = new RegExp('\\b' + this.application?.address_city + '\\b', 'gi')
			return this.property?.town?.match(regex) || false
		},
		applicantAddressStateMatch() {
			const regex = new RegExp('\\b' + this.application?.address_state + '\\b', 'gi')
			return this.property?.state?.match(regex) || false
		},
		applicantAddressZipMatch() {
			const regex = new RegExp('\\b' + this.application?.address_zip + '\\b', 'gi')
			return String(this.property?.zip)?.match(regex) || false
		},
		applicationFirstNameRules() {
			return [
				value => !!value || 'Applicant first name can\'t be empty',
				() => !!this.applicantFirstNameMatch || 'Applicant first name do not match',
			]
		},
		applicationLastNameRules() {
			return [
				value => !!value || 'Applicant last name can\'t be empty',
				() => !!this.applicantLastNameMatch || 'Applicant last name do not match',
			]
		},
		applicationInitialsRules() {
			return [
				value => !!value || 'Application initials can\'t be empty',
				() => !!this.applicantInitialsMatch || 'Application initials do not match',
			]
		},
		applicationAddressLine1Rules() {
			return [
				value => !!value || 'Applicant address line 1 can\'t be empty',
				() => !!this.applicantAddressLine1Match || 'Applicant address line 1 do not match',
			]
		},
		applicationAddressLine2Rules() {
			return [
				() => !!this.applicantAddressLine2Match || 'Applicant address line 2 do not match',
			]
		},
		applicationCityRules() {
			return [
				value => !!value || 'Application city can\t be empty',
				() => !!this.applicantAddressCityMatch || 'Applicant city do not match',
			]
		},
		applicationStateRules() {
			return [
				value => !!value || 'Application state can\t be empty',
				() => !!this.applicantAddressStateMatch || 'Applicant state do not match',
			]
		},
		applicationZipRules() {
			return [
				value => !!value || 'Application zip can\t be empty',
				() => !!this.applicantAddressZipMatch || 'Applicant zip do not match',
			]
		},
		applicationEmailRules() {
			const failedAt = this.application?.email?.failed_at
			return [
				() => {
					return 	!failedAt
						|| `Email Delivery Bounced at ${this.$options.filters.date(failedAt)}`
				},
			]
		},
		isPhysical() {
			return this.application?.source?.id === 1
		},
		isTakeover() {
			return this.application?.application_type_id === 3
		},
		applicationHistoryHeaders() {
			return [
				...(
					this.isTakeover ? 
					[{
						text: '',
						value: 'takeover',
					}] : []
				),
				{
					text: 'Tax Year',
					value: 'tax_year',
				},
				{
					text: 'Previous Owner',
					value: 'first_full_name',
				},
				{
					text: 'Previous Client?',
					value: 'previous_client',
				},
				{
					text: 'Applicant Name',
					value: 'applicant_name',
				},
			]
		},
		showBillingAmount() {
			const paymentType = this.application.payment_type_id
			const paymentStatus = this.application.payment_status_id
			return (paymentType === 2 || paymentType === 3) && paymentStatus === 3
		},
		applicationErrors() {
			const errors = this.$refs.applicationInfo?.inputs?.map(input => {
				const [ msg ] = input?.errorBucket
				return msg
			}).filter(Boolean)
			return errors || []
		},
	},
	methods: {
		...mapActions('sidebar', {
			toggleSidebar: 'toggle',
		}),
		...mapActions('notification', [
			'notify',
		]),
		...mapActions('loader', {
			setLoader: 'set',
		}),
		...mapActions('applications', [
			'loadCaseInfo',
		]),
		...mapActions('counties', [
			'loadCounties',
		]),
		...mapActions('applicationTypes', [
			'loadApplicationTypes',
		]),
		...mapActions('paymentTypes', [
			'loadPaymentTypes',
		]),
		...mapActions('paymentStatuses', [
			'loadPaymentStatuses',
		]),
		...mapActions('marketingCodes', [
			'loadMarketingCodes',
		]),
		...mapActions('rejectReasons', [
			'loadRejectReasons',
		]),
		async loadApplication(id) {
			try {
				this.setLoader(true)
				const { data } = await applicationsApi.get(id)
				this.application = data
				this.applicationOriginal = cloneDeep(data)
				this.$nextTick(() => this.$refs.applicationInfo?.validate())
			} catch(error) {
				this.notify({
					text: 'Can not load Application',
					color: 'error'
				}, { root: true })
			} finally {
				this.setLoader(false)
			}
		},
		async updateApplication(application) {
			try {
				const { data } = await applicationsApi.update(application)
				this.application = data
				this.applicationOriginal = cloneDeep(data)
				this.$nextTick(() => this.$refs.applicationInfo?.validate())
				this.notify({
					text: 'Application updated',
					color: 'success'
				}, { root: true })
			} catch(error) {
				this.notify({
					text: 'Can not update Application',
					color: 'error'
				}, { root: true })
			}
		},
		async reviewApplication(application) {
			try {
				this.setLoader(true)
				if(!this.isApplicationValid) {
					const confirm = await this.$refs.errorsConfirm.open(
						'Save Application changes',
						'Some fields do not match, are you sure to review',
						{ color: 'error' })
					if (!confirm) {
						return this.setLoader(false)
					}
				}
				await applicationsApi.review(application)
				
				await this.goToNextPage()

				this.notify({
					text: 'Application Moved to Review',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not review Application',
					color: 'error'
				}, { root: true })
			} finally {
				await this.loadCaseInfo()
			}
		},
		async approveApplication(application) {
			try {
				this.setLoader(true)
				if(!this.isApplicationValid) {
					const confirm = await this.$refs.errorsConfirm.open(
						'Save Application changes',
						'Some fields do not match, are you sure to approve',
						{ color: 'error' })
					if (!confirm) {
						return this.setLoader(false)
					}
				}
				await applicationsApi.approve(application)

				await this.goToNextPage()

				this.notify({
					text: 'Application approved',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not approve Application',
					color: 'error'
				}, { root: true })
			} finally {
				await this.loadCaseInfo()
			}
		},
		async rejectApplication(application) {
			try {
				this.setLoader(true)
				const { data } = await applicationsApi.reject(application)
				this.application = data
				this.applicationOriginal = cloneDeep(data)

				this.rejectDialog = false

				await this.goToNextPage()

				this.notify({
					text: 'Application rejected',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not reject Application',
					color: 'error'
				}, { root: true })
			} finally {
				await this.loadCaseInfo()
			}
		},
		async fullyRejectApplication(application) {
			try {
				this.setLoader(true)
				const { data } = await applicationsApi.fullyReject(application)
				this.application = data
				this.applicationOriginal = cloneDeep(data)

				this.rejectDialog = false

				await this.goToNextPage()
				
				this.notify({
					text: 'Application fully rejected',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not fully reject Application',
					color: 'error'
				}, { root: true })
			} finally {
				await this.loadCaseInfo()
			}
		},

		/**
		 * Async load all Application's data
		 */
		loadApplicationData() {
			return Promise.all([
				this.loadApplication(this.id),
				this.loadNotes(this.id),
				this.loadApplicationHistory(this.id),
			])
		},

		async goToNextPage() {
			const id = this.nextApplication || this.prevApplication
			if(id) {
				// Go to next/prev application if exists
				return await this.$router.push({
					name: this.$route.name,
					params: {
						...this.$route.params,
						id,
					},
				})
			} else {
				// If no more applications in current queue
				// redirect to main applications page
				return await this.$router.push({
					name: 'applications',
				})
			}
		},

		/**
		 * Generate Application Repair token and open repair link
		 * @param {Number} id Application model id
		 */
		async genAppRepairLink(id) {
			try {
				this.isAppRepairLoading = true
				const { data } = await applicationsApi.repair(id)
				const { token } = data
				return token
			} catch(error) {
				this.notify({
					text: 'Can not get Application Token',
					color: 'error'
				}, { root: true })
			} finally {
				this.isAppRepairLoading = false
			}
		},

		/**
		 * Copy Application Repair link to Clipboard
		 * @param {Number} id Application model id
		 */
		async copyAppRepairLink(id) {
			const token = await this.genAppRepairLink(id)
			const url = `${this.VUE_APP_CUSTOMER_SITE_URL}repair-application-form?token=${token}`

			// Create dummy input and copy text to clipboard
			var dummy = document.createElement('textarea')
			document.body.appendChild(dummy)
			dummy.value = url
			dummy.select()
			document.execCommand('copy')
			document.body.removeChild(dummy)

			this.notify({
				text: 'Repair Link Copied',
				color: 'black'
			}, { root: true })
		},

		/**
		 * Open new Mail with Application Repair link
		 * @param {Number} id Application model id
		 */
		async sendMailAppRepairLink(id) {
			const token = await this.genAppRepairLink(id)
			const { email } = this.application
			const url = `${this.VUE_APP_CUSTOMER_SITE_URL}repair-application-form?token=${token}`
			const href = `mailto:${email.email_address}?body=${url}`
			window.open(href, '_self')
		},

		/**
		 * Send Sign Email to Client
		 * @param {Number} id Application model id
		 */
		async sendSignEmail(id) {
			try {
				if(this.application?.sign_email_sent_at) {
					const confirm = await this.$refs.confirm.open(
						'A Sign Email was already sent',
						'Are you sure to send a new one?',
						{
							color: 'primary',
							width: 400,
						})
					if (!confirm) {
						return this.setLoader(false)
					}
				}
				await applicationsApi.sendSignEmail(id)
				this.loadApplication(this.id)
				this.notify({
					text: 'Sign Email sent to Client',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not send Sign Email to Client',
					color: 'error'
				}, { root: true })
			}
		},

		/**
		 * Route to application by index
		 * Search for application id in current applications list
		 * @param {Number} index
		 */
		routeToApplication(index = 0) {
			const id = this.applications[index]
			this.$router.push({
				name: this.$route.name,
				params: {
					...this.$route.params,
					id,
				},
			})
		},

		/**
		 * Bounced route to application by index
		 * @param {Number} index
		 */
		bouncedRouteToApplication: debounce(function(index) {
			return this.routeToApplication(index)
		}, 1000),

		async loadNotes(applicationId) {
			try {
				const { data } = await applicationNotesApi.getAll(applicationId)
				this.notes = data
			} catch(error) {
				this.notify({
					text: 'Can not load Application Notes',
					color: 'error'
				}, { root: true })
			}
		},
		async createNote(note) {
			try {
				const { data } = await applicationNotesApi.create(this.application?.id, note)
				this.notes.unshift(data)
				this.notify({
					text: 'Note added',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not create note',
					color: 'error'
				}, { root: true })
			}
		},
		async loadApplicationHistory(applicationId) {
			try {
				const { data } = await applicationHistoryApi.getByApplication(applicationId)
				this.applicationHistory = data
			} catch(error) {
				this.notify({
					text: 'Can not load Application History',
					color: 'error'
				}, { root: true })
			}
		},
		resetApplication() {
			this.application = cloneDeep(this.applicationOriginal)
		},
		async saveApplication() {
			if(this.applicationChanged) {
				const confirm = await this.$refs.confirm.open('Save Application changes', 'Are you sure you want to do this?', { color: 'primary' })
				if(confirm) {
					this.updateApplication(this.application)
				}
			}
		},
		async showRejectDialog() {
			await this.saveApplication()
			this.rejectDialog = true
		},

		/**
		 * Compare takeover objects
		 * @param {Object} item
		 */
		compareTakeover(item) {
			return this.application?.takeovers?.some(takeover => {
				return item.client_id === takeover.client_id
					&& item.tax_year === takeover.year
			})
		},

		/**
		 * Update application's data if application is takeover
		 * @param {Boolean} val
		 * @param {Object} item
		 */
		takeoverApplication(val, item = Object) {
			const takeover = {
				application_id: item.application_id,
				client_id: item.client_id,
				year: item.tax_year,
			}
			if(val) {
				this.addTakeover(takeover)
			} else {
				this.deleteTakeover(takeover)
			}
		},

		/**
		 * Create takeover and add to application
		 * @param {Object} takeover
		 */
		async addTakeover(takeover) {
			try {
				const { data } = await takeoversApi.create(takeover)
				const takeovers = this.application?.takeovers
				takeovers.push(data)
				this.$set(this.application, 'takeovers', takeovers)
				this.notify({
					text: 'Takeover added',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not add takeover',
					color: 'error'
				}, { root: true })
			}
		},

		/**
		 * Delete takeover and remove from application
		 * @param {Object} takeover
		 */
		async deleteTakeover(takeover) {
			try {
				const takeoverIndex = this.application?.takeovers.findIndex(item => {
					return item.client_id === takeover.client_id
						&& item.year === takeover.year
				})
				takeover = this.application?.takeovers[takeoverIndex]
				await takeoversApi.delete(takeover)
				this.$delete(this.application.takeovers, takeoverIndex)
				this.notify({
					text: 'Takeover deleted',
					color: 'success'
				}, { root: true })
			} catch (error) {
				this.notify({
					text: 'Can not add takeover',
					color: 'error'
				}, { root: true })
			}
		},

		/**
		 * Find property by address, apn and PLSS
		 */
		async findProperty() { 
			const {
				county,
				address_line1,
				address_line2,
				address_city,
				address_state,
				address_zip,
				district,
				section,
				block,
				lot,
				apn,
			} = this.application

			const params = {
				county,
				district,
				section,
				block,
				lot,
				address_line_1: address_line1,
				address_line_2: address_line2,
				state: address_state,
				city: address_city,
				zip: address_zip,
				apn,
			}

			try {
				this.isFindPropertyLoading = true
				const { data } = await propertiesApi.getAll(params)
				// TODO: handle multiple results
				const property = data[0]

				if(property) {
					this.application.property = property
					this.application.property_id = property.id
					this.notify({
						text: `Property with id ${property.id} founded`,
						color: 'success'
					}, { root: true })
				} else {
					this.notify({
						text: 'No property found',
						color: 'error'
					}, { root: true })
				}
			} catch(error) {
				this.notify({
					text: 'Can not load properties',
					color: 'error'
				}, { root: true })
			} finally {
				this.isFindPropertyLoading = false
			}
		},

		toggleSignatureApproved() {
			const signature_approved = this.application.signature_approved || false
			this.$set(this.application, 'signature_approved', !signature_approved)
		},
	},
	watch: {
		/**
		 * Load new application on id change
		 */
		'id': {
			immediate: true,
			handler: async function(newVal) {
				if(newVal && this.application.id !== this.id) {
					this.setLoader(true)
					await this.loadApplicationData()
					this.setLoader(false)
				}
			},
		},
		/**
		 * Update Tabs Slider width on case info loaded
		 * to prevent underline being displayed incorrectly when loading
		 */
		'statuses': {
			immediate: true,
			deep: true,
			handler() {
				this.$refs.tabs?.callSlider()
			},
		},
	},
	mounted() {
		this.loadCounties()
		this.loadApplicationTypes()
		this.loadPaymentTypes()
		this.loadPaymentStatuses()
		this.loadMarketingCodes()
		this.loadRejectReasons()
	},
	async beforeRouteUpdate(to, from, next) {
		if(this.applicationChanged) {
			// Ask to save changes before go to next application
			const confirm = await this.$refs.confirm.open(
				'Save Application changes',
				'Do you want to save the changes you made?',
				{ color: 'error' })
			if (confirm) {
				await this.updateApplication(this.application)
				next()
			} else {
				next()
			}
		} else {
			next()
		}
	},
}
</script>

<style>
.application-grid {
	display: grid;
	grid-template-columns: repeat(12, minmax(0, 1fr));
	grid-auto-rows: minmax(min-content, max-content);
	gap: 0.5em;
	grid-template-areas: 
        "nav 		nav 		nav 		nav 		nav 		nav 		nav 		app-form	app-form	app-form	app-form	app-form"
        "roll-info 	roll-info 	roll-info 	app-info 	app-info 	app-info 	app-info	app-form	app-form	app-form	app-form	app-form"
        "history	history		history		history		history		history		history		comments	comments	comments	comments	comments";
}

.application-grid-online {
	grid-template-columns: repeat(8, minmax(0, 1fr));
	grid-template-areas: 
        "nav 		nav 		nav 		nav			nav			-	 		toggle-form toggle-form"
        "roll-info 	roll-info 	roll-info 	roll-info 	app-info	app-info 	app-info 	app-info"
        "history	history		history		history		comments	comments	comments	comments";
}

.application-grid-online--open {
	grid-template-columns: repeat(12, minmax(0, 1fr));
	grid-template-areas: 
        "nav 		nav 		nav 		nav			nav			nav 		toggle-form toggle-form app-form	app-form	app-form	app-form"
        "roll-info 	roll-info 	roll-info 	roll-info 	app-info	app-info 	app-info 	app-info	app-form	app-form	app-form	app-form"
        "history	history		history		history		comments	comments	comments	comments	app-form	app-form	app-form	app-form";
}

#application-nav {
	grid-area: nav;
}

#application-toggle-form {
	grid-area: toggle-form;
}

#application-roll-info {
	grid-area: roll-info;
}

#application-app-info {
	grid-area: app-info;
}

#application-app-form {
	grid-area: app-form;
	height: 100%;
}

#application-history {
	grid-area: history;
}

#application-comments {
	grid-area: comments;
}

.v-input.application-number-input {
	color: #9ca6af;
}

.v-input.application-number-input .v-input__control {
	border-radius: 8px;
}

.v-input.application-number-input fieldset {
	border-width: 2px;
	border-color: #e8ecee;
}
</style>