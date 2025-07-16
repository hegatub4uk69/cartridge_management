<template>
  <v-dialog max-width="700px">
    <v-card :title="dialogTitle">
      <template #prepend>
        <v-icon
          color="primary"
          icon="mdi-cog-box"
          size="x-large"
        />
      </template>
      <template #append>
        <v-icon
          color="red"
          icon="mdi-close-outline"
          size="large"
          @click="close_dialog"
        />
      </template>
      <v-form>
        <v-card-text>
          <v-container>
            <v-row>
              <v-autocomplete
                v-model="department_id"
                class="pb-4"
                density="comfortable"
                hide-details
                item-title="name"
                item-value="id"
                :items="departments"
                label="Отдел/отделение"
              />
            </v-row>
            <v-row>
              <v-card class="mx-auto" width="700px">
                <v-toolbar>
                  <v-autocomplete
                    v-model="founded_value_id"
                    class="ma-3"
                    clearable
                    density="comfortable"
                    hide-details
                    item-title="name"
                    item-value="id"
                    :items="found_records"
                    :loading="search_field_loading"
                    menu-icon=""
                    placeholder="Введите номер картриджа"
                    prepend-inner-icon="mdi-magnify"
                    theme="light"
                    variant="solo"
                  />
                </v-toolbar>
                <v-list
                  id="list"
                  class="overflow-y-auto"
                  clearable="true"
                  density="compact"
                  lines="two"
                  nav
                  style="max-height: 450px"
                >
                  <v-list-item
                    v-for="(item, i) in new_cartridges"
                    :key="i"
                    color="primary"
                    :value="item"
                  >
                    <template #prepend>
                      <v-icon
                        icon="mdi-text-box-outline"
                        style="font-size: 40px"
                      />
                    </template>
                    <template #title>
                      <v-list-item-title style="font-size: 18px">{{
                        getCartridgeItemById(item.model_id).name
                      }}
                      </v-list-item-title>
                    </template>
                    <template #subtitle>
                      <v-list-item-subtitle style="font-size: 15px">{{
                        getDepartmentItemById(item.department_id).name
                      }}
                      </v-list-item-subtitle>
                    </template>
                    <template #append>
                      <v-list-item-action class="flex-column align-end">
                        <v-spacer />
                        <v-row>
                          <v-number-input
                            v-model="item.count"
                            control-variant="stacked"
                            density="compact"
                            hide-details
                            :min="1"
                            :model-value="item.count"
                            @click.stop
                          />
                          <v-icon
                            class="my-auto mx-2"
                            color="red"
                            icon="mdi-close-outline"
                            size="x-large"
                            @click.stop="removeNewCartridgeItem(i)"
                          />
                        </v-row>
                      </v-list-item-action>
                    </template>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue-darken-1"
            text="Закрыть"
            variant="text"
            @click="close_dialog"
          />
          <v-btn
            color="blue-darken-1"
            text="Подтвердить"
            type="submit"
            variant="text"
          />
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
  import API from '@/axios.js';

  export default {
    'name': 'CartridgeActions',
    props: {
      option: {
        type: String,
        default: 'issuance',
      },
    },

    data () {
      return {
        search_field_loading: false,
        department_id: null,
        departments: [],
        founded_value_id: null,
        found_records: [],
        timeout: null,
      }
    },

    computed: {
      dialogTitle () {
        if (this.option === 'issuance') {
          return 'Выдача картриджей'
        } else if (this.option === 'need_refill') {
          return 'Пометка необходимости в заправке'
        } else if (this.option === 'decommissioning') {
          return 'Списание картриджей'
        }
      },
    },

    watch: {
      option () {
        this.getDepartments()
      },
    },

    methods: {
      performSearch (query) {
        this.search_field_loading = true

        if (this.timeout) clearTimeout(this.timeout)

        this.timeout = setTimeout(async () => {
          const response = API.post('get')
        })
      },

      getDepartments () {
        API.post('get-departments')
          .then(response => {
            this.departments = response.data.result
          })
      },
      close_dialog () {
        this.$emit('close-dialog')
      },
    },
  }
</script>

<style scoped>

</style>
