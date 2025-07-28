<template>
  <v-container>

    <h1 class="primary--text">Rule "{{ ruleSet.rule_name }}" Settings</h1>

    <v-btn
        :to="{
				name: 'rule-set',
				params: {
					id: ruleSet.parent,
				}
			}"
        color="primary"
        class="my-4">
      Parent Property {{ ruleSet.parent }}
    </v-btn>

    <v-card>
      <v-container>
        <v-select
            v-model="ruleSet.county"
            :items="counties"
            label="County"
            :disabled="!counties[0] || isFieldsDisabled"
            placeholder="Select county"
            item-value="id"
            item-text="name"
            readonly>
        </v-select>
        <v-select
            v-model="ruleSet.year"
            :items="years"
            label="Year"
            placeholder="Select year">
        </v-select>
        <v-select
            v-model="ruleSet.town"
            :items="towns"
            label="Township"
            placeholder="Select township"
            :disabled="isFieldsDisabled"
            item-text="name"
            item-value="name">
        </v-select>
        <v-select
            v-model="ruleSet.village"
            :items="villages"
            label="Village"
            placeholder="Select village"
            :disabled="isFieldsDisabled"
            item-text="name"
            item-value="name">
        </v-select>

        <v-select
            v-model="ruleSet.adjustments_all"
            :items="adjustments"
            multiple
            chips
            label="ALL Adjustments"
            :disabled="isFieldsDisabled"
            item-text="key"
            item-value="key">
        </v-select>

        <v-select
            v-model="ruleSet.adjustments_required"
            :items="adjustments"
            multiple
            chips
            label="Required for Mass CMA Adjustments"
            :disabled="isFieldsDisabled"
            item-text="key"
            item-value="key">
        </v-select>

        <a-date
            v-model="ruleSet.subject_sales_from"
            :disabled="isFieldsDisabled"
            label="Subject Sales from">
        </a-date>

        <v-autonumeric
            v-model.number="ruleSet.cost_of_sale"
            suffix="%"
            :disabled="isFieldsDisabled"
            label="Cost of Sale">
        </v-autonumeric>

        <v-autonumeric
            v-model.number="ruleSet.water"
            suffix="%"
            :disabled="isFieldsDisabled"
            label="Water">
        </v-autonumeric>

        <v-autonumeric
            v-model.number="ruleSet.age"
            suffix="%"
            :disabled="isFieldsDisabled"
            label="Age">
        </v-autonumeric>
      </v-container>

      <v-card-actions
          v-if="isAdmin">
        <v-btn
            color="success"
            depressed
            @click="updateRuleSet(ruleSet)">
          Save
        </v-btn>
        <v-btn
            color="success"
            depressed
            :to="{ name: 'rule-sets' }">
          Cancel
        </v-btn>
        <v-btn
            color="error"
            depressed
            @click="deleteRuleSet(ruleSet)">
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card class="my-5">
      <v-container>
        <v-row>
          <v-col>
            <h2>Add / Edit Selection</h2>
          </v-col>
          <v-col
              v-if="isAdmin">
            <v-btn
                depressed
                class="mx-1"
                @click="loadSelectionRule(ruleSet.selection_rules)">
              Discard
            </v-btn>
            <v-btn
                depressed
                class="mx-1"
                color="success"
                @click="saveSelectionRules(selectionRule)">
              Save Selection Rule
            </v-btn>
          </v-col>
        </v-row>

        <v-divider></v-divider>

        <v-row>
          <v-col>
            Description
          </v-col>
          <v-col>
            Value
          </v-col>
          <v-col>
            Inherit
          </v-col>
        </v-row>
        <v-row
            v-for="(field, key) in selectionRulesFields"
            :key="key"
            class="align-center">
          <v-col class="primary--text text--darken-2 font-weight-bold">
            {{ field.label }}
          </v-col>
          <v-col>
            <v-checkbox
                v-if="field.type === 'boolean'"
                v-model="selectionRule[field.model]"
                :disabled="isFieldsDisabled">
            </v-checkbox>

            <v-autonumeric
                v-else-if="field.type === 'numeric'"
                v-model.number="selectionRule[field.model]"
                :suffix="field.suffix"
                :disabled="isFieldsDisabled">
            </v-autonumeric>

            <a-date
                v-else-if="field.type === 'date'"
                v-model="selectionRule[field.model]"
                :disabled="isFieldsDisabled">
            </a-date>

            <v-text-field
                v-else
                v-model.number="selectionRule[field.model]"
                :suffix="field.suffix"
                :disabled="isFieldsDisabled">
            </v-text-field>
          </v-col>
          <v-col>
            <v-checkbox>
            </v-checkbox>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <v-card class="my-5">
      <v-container>
        <h2>Chart of Inventory Adjustments Values</h2>
        <a-table
            ref="inventoryTable"
            :items="inventoryRules"
            :headers="inventoryRulesHeaders"
            @delete="deleteInventoryRule">

          <template
              v-for="(header, key) in inventoryRulesHeaders"
              v-slot:[`item.${header.value}`]="{ item }">
            <!-- Input for complex values -->
            <v-autonumeric
                v-if="header.index"
                :key="key"
                v-model.number="item[header.value.split('[')[0]][header.index]"
                single-line
                hide-details
                placeholder="0"
                :an-options="{
								currencySymbol: '$',
							}"
                class="align-right"
                :disabled="isFieldsDisabled">
            </v-autonumeric>

            <!-- Input for simple values -->
            <v-autonumeric
                v-else
                :key="key"
                v-model.number="item[header.value]"
                single-line
                hide-details
                placeholder="0"
                :an-options="{
								currencySymbol: '$',
							}"
                class="align-right"
                :disabled="isFieldsDisabled">
            </v-autonumeric>
          </template>

          <template #item.actions="{ item }">
            <v-icon
                small
                color="red"
                @click="$refs.inventoryTable.deleteItem(item)">
              mdi-delete
            </v-icon>
          </template>

        </a-table>
      </v-container>

      <v-card-actions
          v-if="isAdmin">
        <v-btn
            color="success"
            depressed
            @click="addInventoryRule">
          Add new row
        </v-btn>
        <v-btn
            color="success"
            depressed
            @click="saveInventoryRules(inventoryRules)">
          Save inventory rules
        </v-btn>
        <v-btn
            color="success"
            depressed
            @click="loadInventoryRules(id)">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-card class="my-5">
      <v-container>
        <h2>Add / Edit Obsolescence Adjustment</h2>
        <v-divider></v-divider>

        <v-row
            v-for="(field, key) in obsolescencesRulesFields"
            :key="key"
            class="align-center">
          <v-col class="primary--text text--darken-2 font-weight-bold">
            {{ field.rule_name }}
          </v-col>
          <v-col>
            <v-text-field
                v-model.number="ruleSet.obsolescence_rules[field.rule_index]"
                suffix="%"
                :disabled="isFieldsDisabled">
            </v-text-field>
          </v-col>
        </v-row>
      </v-container>

      <v-card-actions
          v-if="isAdmin">
        <v-btn
            color="success"
            depressed
            @click="updateRuleSet(ruleSet)">
          Save Obsolescence
        </v-btn>
        <v-btn
            color="success"
            depressed
            @click="loadRuleSet(id)">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>

    <confirm ref="confirm"></confirm>

  </v-container>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
import {apiFactory} from '../../api/apiFactory'
import ATable from '../../components/ATable'
import Confirm from '../../components/Confirm'
import VAutonumeric from '../../components/VAutonumeric'
import ADate from '../../components/ADate'

const constantsApi = apiFactory.get('constants')
const townsApi = apiFactory.get('towns')
const villagesApi = apiFactory.get('villages')
const ruleSetsApi = apiFactory.get('rule-sets')
const selectionRulesApi = apiFactory.get('selection-rules')
const inventoryRulesApi = apiFactory.get('inventory-rules')
const obsolescencesRulesApi = apiFactory.get('obsolescences-rules')
const adjustmentsApi = apiFactory.get('adjustments')

export default {
  components: {
    ATable,
    Confirm,
    VAutonumeric,
    ADate,
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data: () => ({
    constants: {},
    ruleSet: {},
    towns: [],
    villages: [],
    adjustments: [],
    selectionRule: {},
    selectionRulesFields: [
      {
        label: 'Proximity range',
        type: 'numeric',
        model: 'proximity_range',
        suffix: 'Miles',
      },
      {
        label: 'Sale date from',
        type: 'date',
        model: 'sale_date_from',
      },
      {
        label: 'Sale date to',
        type: 'date',
        model: 'sale_date_to',
      },
      {
        label: 'Percent GLA Lower',
        model: 'percent_gla_lower',
        suffix: '%',
      },
      {
        label: 'Percent GLA Higher',
        model: 'percent_gla_higher',
        suffix: '%',
      },
      {
        label: 'Percent Sale Lower',
        model: 'percent_sale_lower',
        suffix: '%',
      },
      {
        label: 'Percent Sale Higher',
        model: 'percent_sale_higher',
        suffix: '%',
      },
      {
        label: 'Percent Lot Size Lower',
        model: 'percent_lot_size_lower',
        suffix: '%',
      },
      {
        label: 'Percent Lot Size Higher',
        model: 'percent_lot_size_higher',
        suffix: '%',
      },
      {
        label: 'Same property class',
        type: 'boolean',
        model: 'same_property_class',
      },
      {
        label: 'Same Family Types',
        type: 'boolean',
        model: 'same_one_family_types',
      },
      {
        label: 'Same school district',
        type: 'boolean',
        model: 'same_school_district',
      },
      {
        label: 'Same town',
        type: 'boolean',
        model: 'same_town'
      },
      {
        label: 'Same street',
        type: 'boolean',
        model: 'same_street',
      },
      {
        label: 'Same property style',
        type: 'boolean',
        model: 'same_property_style',
      },
      {
        label: 'Same building',
        type: 'boolean',
        model: 'same_building',
      },
      {
        label: 'Prioritize same water categories',
        type: 'boolean',
        model: 'prioritize_same_water_categories',
      },
    ],
    inventoryRules: [],
    obsolescencesRulesFields: [],
  }),
  computed: {
    ...mapGetters('auth', [
      'isAdmin',
    ]),
    ...mapGetters('counties', [
      'counties',
    ]),
    ...mapGetters('years', [
      'years',
    ]),
    isFieldsDisabled() {
      return !this.isAdmin
    },
    inventoryRulesHeaders() {
      return [
        {
          text: 'Price Start',
          value: 'price_start',
        },
        {
          text: 'Price End',
          value: 'price_end',
        },
        ...(
            this.ruleSet && this.ruleSet.adjustments_all
                ? this.adjustments.map(item => {
                  if (this.ruleSet.adjustments_all.some(i => i === item.key) && (item.rule_field && item.property_field)) {
                    return {
                      text: item.name,
                      value: item.rule_field,
                      index: item.index,
                    }
                  }
                  return false
                }).filter(Boolean)
                : []
        ),
        {
          text: 'Actions',
          value: 'actions',
        },
      ]
    },
  },
  methods: {
    ...mapActions('notification', [
      'notify',
    ]),
    /**
     * Transform adjusments to use complex inventory rules field (arrays)
     * like BASEMENT etc.
     * @param {Array} adjs list of adjustments models
     */
    transformAdjustments(adjs) {
      const newAdjs = []
      adjs.forEach(item => {
        const map = this.constants[`${item.property_field}_map`]
        if (map) {
          Object.entries(map).forEach(([index, type]) => {
            newAdjs.push({
              ...item,
              name: `${item.name} (${type})`,
              rule_field: `${item.rule_field}[${index}]`,
              index,
            })
          })
        } else {
          newAdjs.push(item)
        }
      })
      return newAdjs
    },
    async loadAdjustments() {
      try {
        const {data} = await adjustmentsApi.getAll()
        this.adjustments = data
      } catch (error) {
        this.notify({
          text: 'Can not load Adjustments',
          color: 'error'
        }, {root: true})
      }
    },
    async loadConstants(county) {
      try {
        const {data} = await constantsApi.getAll(county)
        this.constants = data
      } catch (error) {
        this.notify({
          text: 'Can not load constants',
          color: 'error'
        }, {root: true})
      }
    },
    async loadRuleSet(id) {
      try {
        const {data} = await ruleSetsApi.get(id)
        this.ruleSet = data
        this.selectionRule = data.selection_rules || {}
      } catch (error) {
        this.notify({
          text: 'Can not load Rule Set',
          color: 'error'
        }, {root: true})
      }
    },
    async updateRuleSet(item) {
      try {
        const confirm = await this.$refs.confirm.open('Save changes to Rule Set', 'Are you sure you want to make changes to the Rule Set?', {color: 'success'})
        if (confirm) {
          await ruleSetsApi.update(item)
          this.notify({
            text: 'Rule Set updated',
            color: 'success'
          }, {root: true})
        }
      } catch (error) {
        this.notify({
          text: 'Can not update Rule Set',
          color: 'error'
        }, {root: true})
      }
    },
    async deleteRuleSet(item) {
      try {
        await ruleSetsApi.delete(item)
        this.notify({
          text: 'Rule Set deleted',
          color: 'success'
        }, {root: true})
        this.$router.push({name: 'rule-sets'})
      } catch (error) {
        this.notify({
          text: 'Can not delete Rule Set',
          color: 'error'
        }, {root: true})
      }
    },
    async loadTowns(countyid) {
      try {
        const {data} = await townsApi.getAll(countyid)
        // TODO: Remove this when best API is ready
        this.towns = Object.entries(data).map(([key, val]) => ({
          id: key,
          name: val,
        }))
      } catch (error) {
        this.notify({
          text: 'Can not load towns',
          color: 'error'
        }, {root: true})
      }
    },
    async loadVillages(countyid) {
      try {
        const {data} = await villagesApi.getAll(countyid)
        // TODO: Remove this when best API is ready
        this.villages = Object.entries(data).map(([key, val]) => ({
          id: key,
          name: val,
        }))
      } catch (error) {
        this.notify({
          text: 'Can not load villages',
          color: 'error'
        }, {root: true})
      }
    },
    async loadSelectionRule(ruleid) {
      try {
        const {data} = await selectionRulesApi.get(ruleid)
        this.selectionRule = data
      } catch (error) {
        this.notify({
          text: 'Can not load Selection Rule',
          color: 'error'
        }, {root: true})
      }
    },
    async saveSelectionRules(rule) {
      const confirm = await this.$refs.confirm.open('Save selection rules', 'Are you sure you want to make changes to the selection rules?', {color: 'success'})
      if (confirm) {
        if (rule.id) {
          return this.updateSelectionRule(rule)
        } else {
          rule.parent_id = this.id
          return this.createSelectionRule(rule)
        }
      }

    },
    async createSelectionRule(rule) {
      try {
        await selectionRulesApi.create(rule)
        this.notify({
          text: 'Selection Rule created',
          color: 'success'
        }, {root: true})
      } catch (error) {
        this.notify({
          text: 'Can not create Selection Rule',
          color: 'error'
        }, {root: true})
      }
    },
    async updateSelectionRule(rule) {
      try {
        await selectionRulesApi.update(rule)
        this.notify({
          text: 'Selection Rule updated',
          color: 'success'
        }, {root: true})
      } catch (error) {
        this.notify({
          text: 'Can not update Selection Rule',
          color: 'error'
        }, {root: true})
      }
    },
    async loadInventoryRules(ruleSetid) {
      try {
        const {data} = await inventoryRulesApi.getByParent(ruleSetid)
        this.inventoryRules = data
      } catch (error) {
        this.notify({
          text: 'Can not load Invevtory Rules',
          color: 'error'
        }, {root: true})
      }
    },
    addInventoryRule() {
      this.inventoryRules.push({
        parent: this.id,
        basement_prices: [],
      })
    },
    async saveInventoryRules(rules) {
      try {
        const confirm = await this.$refs.confirm.open('Submit Inventory Rules', 'Are you sure you want to make changes to the Inventory Rules?', {color: 'success'})
        if (confirm) {
          await Promise.all(rules.map(async r => {
            if (r.id) {
              return await this.updateInventoryRule(r)
            } else {
              return await this.createInventoryRule(r)
            }
          }))
          this.notify({
            text: 'Inventory Rules updated',
            color: 'success'
          }, {root: true})
        }
        return
      } catch (error) {
        this.notify({
          text: 'Error while Inventory Rules update',
          color: 'error'
        }, {root: true})
      }
    },
    async createInventoryRule(item) {
      try {
        await inventoryRulesApi.create(item)
        this.notify({
          text: 'Inventory Rule created',
          color: 'success'
        }, {root: true})
      } catch (error) {
        this.notify({
          text: 'Can not create Inventory Rule',
          color: 'error'
        }, {root: true})
      }
    },
    async updateInventoryRule(item) {
      try {
        await inventoryRulesApi.update(item)
        this.notify({
          text: 'Inventory Rule updated',
          color: 'success'
        }, {root: true})
      } catch (error) {
        this.notify({
          text: 'Can not update Inventory Rule',
          color: 'error'
        }, {root: true})
      }
    },
    async deleteInventoryRule(item, index) {
      try {
        await inventoryRulesApi.delete(item)
        this.$delete(this.inventoryRules, index)
        this.notify({
          text: 'Inventory Rule deleted',
          color: 'success'
        }, {root: true})
      } catch (error) {
        this.notify({
          text: 'Can not delete Inventory Rule',
          color: 'error'
        }, {root: true})
      }
    },
    async loadObsolescencesRules(county) {
      try {
        // FIXME: remove to lowercase
        county = county.toLowerCase()
        const {data} = await obsolescencesRulesApi.getAll({county})
        this.obsolescencesRulesFields = data
      } catch (error) {
        this.notify({
          text: 'Can not load Obsolescences Rules',
          color: 'error'
        }, {root: true})
      }
    },
    async loadData() {
      this.loadAdjustments()
      await this.loadRuleSet(this.id)
      if (this.ruleSet.inventory_rules) {
        this.loadInventoryRules(this.id)
        await this.loadConstants({county: this.ruleSet.county})
        this.adjustments = this.transformAdjustments(this.adjustments)
      }
      if (this.ruleSet.obsolescence_rules) {
        this.loadObsolescencesRules(this.ruleSet.county)
      }
    },
  },
  watch: {
    id: {
      immediate: true,
      handler() {
        this.loadData()
      },
    },
    'ruleSet.county'(val) {
      return val && this.loadTowns(val), this.loadVillages(val)
    },
  },
}
</script>