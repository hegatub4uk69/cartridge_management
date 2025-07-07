<template>
  <v-dialog v-model="dialog" max-width="700px">
    <v-card title="Изменение информации о картридже">
      <template #prepend>
        <v-icon
          color="primary"
          icon="mdi-lead-pencil"
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
      <v-form v-model="validation" @submit.prevent="editData">
        <v-card-text>
          <v-container>
            <v-row>
              <v-autocomplete
                v-model="new_cartridge_data_to_edit.model_id"
                density="comfortable"
                item-title="name"
                item-value="id"
                :items="cartridge_models"
                label="Модель картриджа"
                :rules="[required]"
              />
            </v-row>
            <v-row>
              <v-autocomplete
                v-model="new_cartridge_data_to_edit.department_id"
                density="comfortable"
                item-title="name"
                item-value="id"
                :items="departments"
                label="Отдел/отделение"
                :rules="[required]"
              />
            </v-row>
            <v-row>
              <v-textarea
                v-model="new_cartridge_data_to_edit.description"
                density="comfortable"
                label="Описание"
              />
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
            :disabled="!validation"
            text="Добавить"
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
    name: 'EditCartridgeInfo',
    props: {
      cartridge_id: {
        type: BigInt,
        default: null,
      },
    },

    data () {
      return {
        dialog: undefined,
        validation: false,
        new_cartridge_data_to_edit: {
          id: null,
          model_id: null,
          department_id: null,
          description: '',
        },
        cartridge_models: [],
        departments: [],
      }
    },

    watch: {
      cartridge_id (newVal) {
        if (newVal) {
          this.getCartridgeModels()
          this.getDepartments()
          this.getCartridgeDataToEdit(newVal)
        }
      },
    },

    methods: {
      editData () {
        this.new_cartridge_data_to_edit.id = this.cartridge_id
        API.post('update-cartridge-data', this.new_cartridge_data_to_edit)
          .then(response => {
            this.$emit('confirm', response.data.result)
          })
      },
      close_dialog () {
        this.$emit('close-dialog')
      },

      getCartridgeDataToEdit (id) {
        API.post('get-cartridge-data-to-edit', { id })
          .then(response => {
            this.new_cartridge_data_to_edit.model_id = response.data.result[0]['model_id']
            this.new_cartridge_data_to_edit.department_id = response.data.result[0]['department_id']
            this.new_cartridge_data_to_edit.description = response.data.result[0]['description']
          })
      },
      getCartridgeModels () {
        API.post('get-cartridge-models')
          .then(response => {
            this.cartridge_models = response.data.result
          })
      },
      getDepartments () {
        API.post('get-departments')
          .then(response => {
            this.departments = response.data.result
          })
      },

      required (value) {
        return !!value || 'Поле обязательно для заполнения'
      },
    },
  }
</script>

<style scoped>

</style>
