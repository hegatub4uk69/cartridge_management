<template>
  <v-container fluid>
    <v-card>
      <v-row align="center" dense justify="center" style="padding: 10px">
        <div class="d-flex">
          <v-col>
            <v-btn class="mr-2" color="primary" size="x-large" variant="tonal">Выдача картриджей</v-btn>
            <v-btn class="mr-2" color="primary" size="x-large" variant="tonal">Отправка на заправку</v-btn>
            <v-btn color="primary" size="x-large" variant="tonal">Списание картриджей</v-btn>
          </v-col>
        </div>
        <v-col>
          <div class="d-flex flex-nowrap">
            <v-select class="pr-2" hide-details />
            <v-select hide-details />
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
  <v-container fluid>
    <!--Таблица вывода информации о картриджах-->
    <v-data-table
      class="elevation-1 table"
      :headers="cartridgeHeaders"
      item-value="id"
      :items="cartridges"
      :loading="loadingCartridgesTable"
      :search="table_cartridges_search"
      @update:options="loadCartridgesData"
    >
      <template #top>
        <v-toolbar class="table_toolbar" color="white" flat>
          <v-col>
            <v-toolbar-title style="font-size: 25px">
              <v-icon class="mb-1" icon="mdi-book-open-outline" />
              Картриджи
            </v-toolbar-title>
          </v-col>
          <v-col>
            <v-text-field
              v-model="table_cartridges_search"
              density="compact"
              flat
              hide-details
              label="Введите поисковое значение"
              prepend-inner-icon="mdi-table-search"
              single-line
              variant="solo-filled"
            />
          </v-col>
          <v-col>
            <v-btn
              class="float-end"
              color="green"
              prepend-icon="mdi-plus"
              variant="outlined"
              @click="openDialogAddNewCartridge"
            >НОВЫЙ</v-btn>
          </v-col>
          <!--Диалоговое окно добавления нового картриджа-->
          <v-dialog
            v-model="dialog_new_cartridge"
            max-width="700px"
          >
            <v-card title="Добавление нового картриджа">
              <template #prepend>
                <v-icon
                  icon="mdi-new-box"
                  color="primary"
                  size="x-large"
                />
              </template>
              <template #append>
                <v-icon
                  icon="mdi-close-outline"
                  size="large"
                  color="red"
                  @click="closeAddNewCartridge"
                />
              </template>
              <v-form v-model="validation_new_cartridge" @submit.prevent="addNewCartridge">
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-text-field
                        v-model="new_cartridge_data.model"
                        label="Модель картриджа"
                        :rules="[required]"
                      />
                    </v-row>
                    <v-row>
                      <v-select
                        v-model="new_cartridge_data.department_id"
                        item-title="name"
                        item-value="id"
                        :items="departments"
                        label="Отдел/отделение"
                        :rules="[required]"
                      />
                    </v-row>
                    <v-row>
                      <v-textarea
                        v-model="new_cartridge_data.description"
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
                    @click="closeAddNewCartridge"
                  />
                  <v-btn
                    color="blue-darken-1"
                    :disabled="!validation_new_cartridge"
                    text="Добавить"
                    type="submit"
                    variant="text"
                  />
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>

        </v-toolbar>
        <v-divider />
      </template>
      <template #[`item.actions`]="{ item }">
        <v-icon
          class="mr-2"
          color="purple"
          icon="mdi-barcode-scan"
          size="large"
        />
        <v-icon
          class="mr-2"
          color="info"
          icon="mdi-information-outline"
          size="large"
        />
        <v-icon
          class="mr-2"
          color="orange"
          icon="mdi-pencil"
        />
        <v-icon
          class="mr-0"
          color="red"
          icon="mdi-delete-outline"
        />
      </template>
    </v-data-table>

  </v-container>
  <v-container>
    <!--    -->
  </v-container>
  <!--#-->
</template>

<script>
  import API from '@/axios.js';
  import { createToast } from 'mosha-vue-toastify';

  export default {
    name: 'CartridgesPage',
    data () {
      return {
        table_cartridges_search: '',
        cartridgeHeaders: [
          { title: '№', align: 'start', key: 'id' },
          { title: 'Наименование', key: 'model' },
          { title: 'Местоположение', key: 'department' },
          { title: 'Дата местоположения', key: 'date_of_last_location' },
          { title: 'Действия', key: 'actions', sortable: false },
        ],
        loadingCartridgesTable: true,
        cartridges: [],
        departments: [],
        validation_new_cartridge: false,
        dialog_new_cartridge: false,
        new_cartridge_data: {
          model: '',
          department_id: null,
          description: '',
        },
      }
    },

    watch: {
      dialog_new_cartridge () {
        if (!this.dialog_new_cartridge) {
          this.closeAddNewCartridge()
        } else {
          this.loadDepartments()
        }
      },
    },

    methods: {
      loadCartridgesData () {
        this.loadingCartridgesTable = true
        API.post('get-cartridges-data')
          .then(response => {
            this.cartridges = response.data.result
            this.loadingCartridgesTable = false
          })
      },

      loadDepartments () {
        API.post('get-departments')
          .then(response => {
            this.departments = response.data.result
          })
      },

      openDialogAddNewCartridge () {
        this.dialog_new_cartridge = true
      },
      closeAddNewCartridge () {
        this.dialog_new_cartridge = false
        this.departments = []
        this.new_cartridge_data = {}
      },
      addNewCartridge () {
        API.post('add-new-cartridge', this.new_cartridge_data)
          .then(response => {
            createToast(response.data.result, {
              showIcon: 'true',
              showCloseButton: false,
              type: 'success',
              position: 'top-center',
              timeout: 3000,
              toastBackgroundColor: '#4caf50',
            })
            this.loadCartridgesData()
          })
        this.closeAddNewCartridge()
      },

      required (value) {
        return !!value || 'Поле обязательно для заполнения'
      },
    },
  }
</script>

<style scoped>
.table {
  background: #fff;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  font-size: 16px;
}
.table_toolbar {
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
}
</style>
