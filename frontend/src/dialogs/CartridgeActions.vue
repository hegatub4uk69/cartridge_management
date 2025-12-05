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
                v-if="option === 'issuance'"
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
              <v-text-field
                v-model="cartridge_id_to_search"
                clearable
                density="comfortable"
                hide-details
                item-title="name"
                item-value="id"
                :loading="search_field_loading"
                menu-icon=""
                placeholder="Введите номер картриджа"
                prepend-inner-icon="mdi-magnify"
                theme="light"
                variant="solo"
              >
                <template #append-inner>
                  <v-btn
                    color="primary"
                    @click="performSearch(cartridge_id_to_search)"
                  >Поиск
                  </v-btn>
                </template>
              </v-text-field>
            </v-row>
          </v-container>
          <v-container fluid>
            <v-card>
              <v-card-text>
                <v-text-field
                  :model-value="this.cartridge_info.id"
                  :readonly="true"
                  prepend-inner-icon="mdi-ticket-confirmation-outline"
                  label="Номер картриджа"
                />
                <v-text-field
                  :model-value="this.cartridge_info.model"
                  :readonly="true"
                  prepend-inner-icon="mdi-card-text-outline"
                  label="Модель картриджа"
                />
                <v-text-field
                  :model-value="cartridge_info.department"
                  :readonly="true"
                  prepend-inner-icon="mdi-bank-outline"
                  label="Местоположение"
                />
                <v-text-field
                  :model-value="this.cartridge_info.department_date"
                  :readonly="true"
                  prepend-inner-icon="mdi-calendar-clock-outline"
                  label="Дата местоположения"
                />
              </v-card-text>
            </v-card>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
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
import {createToast} from "mosha-vue-toastify";

export default {
  'name': 'CartridgeActions',
  props: {
    option: {
      type: String,
      default: 'issuance',
    },
  },

  data() {
    return {
      search_field_loading: false,
      cartridge_info: {
        id: null,
        model: null,
        department: null,
        department_date: null
      },
      department_id: null,
      departments: [],
      cartridge_id_to_search: null,
      found_records: [],
      timeout: null,
    }
  },

  computed: {
    dialogTitle() {
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
    option() {
      this.getDepartments()
    },
  },

  methods: {
    performSearch(query) {
      this.search_field_loading = true

      if (this.timeout) clearTimeout(this.timeout)

      this.timeout = setTimeout(async () => {
        API.post('get-cartridge-info', {id: query})
          .then(response => {
            this.cartridge_info.id = response.data['id']
            this.cartridge_info.model = response.data['model']
            this.cartridge_info.department = response.data['department']
            this.cartridge_info.department_date = response.data['department_date']
            this.search_field_loading = false
          })
          .catch(err => {
              createToast(err.data.error, {
                showIcon: 'true',
                showCloseButton: false,
                type: 'danger',
                position: 'top-center',
                timeout: 3000,
                toastBackgroundColor: '#ff5252',
              });
              this.search_field_loading = false
            }
          )
      }, 5)
    },

    getDepartments() {
      API.post('get-departments')
        .then(response => {
          this.departments = response.data.result
        })
    },
    close_dialog() {
      this.$emit('close-dialog')
    },
  },
}
</script>

<style scoped>

</style>
