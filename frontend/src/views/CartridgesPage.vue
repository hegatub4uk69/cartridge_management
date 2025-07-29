<template>
  <v-container class="pb-0" fluid>
    <v-card>
      <v-row align="center" dense style="padding: 10px">
        <v-col cols="3">
          <div class="d-flex flex-column">
            <v-btn class="mb-1 text-truncate" color="primary" size="x-large" variant="tonal">Списание картриджей</v-btn>
            <v-btn
              class="text-truncate"
              color="primary"
              size="x-large"
              variant="tonal"
              @click="openDialogCartridgeActions('issuance')"
            >Выдача картриджей</v-btn>
          </div>
        </v-col>
        <v-col cols="3">
          <div class="d-flex flex-column">
            <v-btn class="mb-1 text-truncate" color="primary" size="x-large" variant="tonal">Отправка на заправку</v-btn>
            <v-btn class="text-truncate" color="primary" size="x-large" variant="tonal">Необходима заправка</v-btn>
          </div>
        </v-col>
        <v-col>
          <v-checkbox
            v-model="decommissioned_filter"
            color="primary"
            hide-details
            label="Отображение списка исключительно списанных картриджей"
          />
          <div class="d-flex flex-nowrap">
            <v-autocomplete
              v-model="cartridge_model_filter"
              class="pr-2"
              density="comfortable"
              hide-details
              item-title="name"
              item-value="id"
              :items="cartridge_models"
              label="Модель картриджа"
            />
            <v-autocomplete
              v-model="department_filter"
              class="pr-2"
              density="comfortable"
              hide-details
              item-title="name"
              item-value="id"
              :items="departments"
              label="Местоположение"
            />
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
  <v-container class="pt-3" fluid>
    <!--Таблица вывода информации о картриджах-->
    <v-data-table
      class="elevation-1 table"
      :headers="cartridgeHeaders"
      item-value="id"
      :items="cartridges"
      :loading="loadingCartridgesTable"
      :search="table_cartridges_search"
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
            >НОВЫЙ
            </v-btn>
          </v-col>

          <!--Диалоговое окно добавления нового картриджа-->
          <v-dialog
            v-model="dialog_new_cartridge"
            max-width="700px"
          >
            <v-card title="Добавление нового картриджа">
              <template #prepend>
                <v-icon
                  color="primary"
                  icon="mdi-new-box"
                  size="x-large"
                />
              </template>
              <template #append>
                <v-icon
                  color="red"
                  icon="mdi-close-outline"
                  size="large"
                  @click="dialog_new_cartridge = false"
                />
              </template>
              <v-form v-model="validation_new_cartridge" @submit.prevent="addNewCartridge">
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-autocomplete
                        v-model="new_cartridge_data.model_id"
                        density="comfortable"
                        item-title="name"
                        item-value="id"
                        :items="cartridge_models"
                        label="Модель картриджа"
                      />
                    </v-row>
                    <v-row>
                      <v-autocomplete
                        v-model="new_cartridge_data.department_id"
                        density="comfortable"
                        item-title="name"
                        item-value="id"
                        :items="departments"
                        label="Отдел/отделение"
                      />
                    </v-row>
                    <v-row>
                      <v-textarea
                        v-model="new_cartridge_data.description"
                        density="comfortable"
                        label="Описание"
                      />
                    </v-row>
                    <v-row>
                      <v-card class="mx-auto" width="700px">
                        <v-toolbar>
                          <v-btn
                            class="mx-auto"
                            :disabled="!new_cartridge_data.model_id || !new_cartridge_data.department_id"
                            prepend-icon="mdi-plus"
                            text="Добавить новый элемент"
                            variant="tonal"
                            @click="addNewCartridgeToList"
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
                    @click="dialog_new_cartridge = false"
                  />
                  <v-btn
                    color="blue-darken-1"
                    :disabled="isNewCartridgesListEmpty"
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
          @click="generatePDF(item.model, item.id)"
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
          @click="openDialogEditCartridgeData(item.id)"
        />
      </template>
    </v-data-table>
    <!--Диалоговое окно изменения информации о картридже-->
    <EditCartridgeInfo
      v-model="dialog_edit_cartridge_data"
      :cartridge_id="cartridge_id_to_edit"
      @close-dialog="onCloseEditCartridgeData"
      @confirm="onConfirmEditCartridgeData"
    />
    <CartridgeActions
      v-model="dialog_cartridge_actions"
      :option="cartridge_actions_option"
      @close-dialog="onCloseCartridgeActions"
      @confirm="onConfirmCartridgeActions"
    />
  </v-container>
</template>

<script>
  import API from '@/axios.js';
  import { createToast } from 'mosha-vue-toastify';
  import { store } from '@/store.js';
  import EditCartridgeInfo from '@/dialogs/EditCartridgeInfo.vue';
  import CartridgeActions from '@/dialogs/CartridgeActions.vue';

  export default {
    name: 'CartridgesPage',
    components: {
      EditCartridgeInfo,
      CartridgeActions,
    },
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
        cartridge_models: [
          {
            id: null,
            name: 'Все',
          },
        ],
        cartridges: [],
        departments: [
          {
            id: null,
            name: 'Все',
          },
        ],
        validation_new_cartridge: false,
        dialog_edit_cartridge_data: false,
        dialog_cartridge_actions: false,
        cartridge_actions_option: 'issuance',
        cartridge_id_to_edit: null,
        dialog_new_cartridge: false,
        new_cartridge_data: {
          model_id: null,
          department_id: null,
          description: '',
          count: null,
        },
        new_cartridges: [],
        decommissioned_filter: false,
        cartridge_model_filter: null,
        department_filter: store.state.user_data.department_id,
      }
    },

    computed: {
      isNewCartridgesListEmpty () {
        return this.new_cartridges.length === 0
      },
    },

    watch: {
      cartridge_model_filter () {
        this.loadCartridgesData()
      },
      department_filter () {
        this.loadCartridgesData()
      },
      dialog_new_cartridge () {
        if (!this.dialog_new_cartridge) {
          this.closeAddNewCartridge()
        } else {
          this.loadDepartments()
          this.loadCartridgeModels()
        }
      },
    },

    created () {
      this.loadCartridgeModels('main')
      this.loadDepartments('main')
      this.loadCartridgesData()
    },

    methods: {
      loadCartridgesData () {
        this.loadingCartridgesTable = true
        API.post('get-cartridges-data', {
          model_id: this.cartridge_model_filter,
          department_id: this.department_filter,
        })
          .then(response => {
            this.cartridges = response.data.result
            this.loadingCartridgesTable = false
          })
      },

      loadCartridgeModels (option=null) {
        API.post('get-cartridge-models')
          .then(response => {
            if (option === 'main') {
              for (const item of response.data.result) {
                this.cartridge_models.push(item)
              }
            }
            if (option === null) {
              this.cartridge_models = response.data.result
            }
          })
      },

      loadDepartments (option=null) {
        API.post('get-departments')
          .then(response => {
            if (option === 'main') {
              for (const item of response.data.result) {
                this.departments.push(item)
              }
            }
            if (option === null) {
              this.departments = response.data.result
            }
          })
      },
      updateMainData () {
        this.departments = [{ id: null, name: 'Все' }]
        this.cartridge_models = [{ id: null, name: 'Все' }]
        this.new_cartridge_data = {}
        this.new_cartridges = []

        const current_cartridge_model = this.cartridge_model_filter
        this.loadCartridgeModels('main')
        this.cartridge_model_filter = current_cartridge_model
        const current_department = this.department_filter
        this.loadDepartments('main')
        this.department_filter = current_department

        this.loadCartridgesData()
      },

      openDialogEditCartridgeData (id) {
        this.cartridge_id_to_edit = id
        this.dialog_edit_cartridge_data = true
      },
      onConfirmEditCartridgeData (value) {
        this.dialog_edit_cartridge_data = false
        createToast(value, {
          showIcon: 'true',
          showCloseButton: false,
          type: 'success',
          position: 'top-center',
          timeout: 3000,
          toastBackgroundColor: '#4caf50',
        })
        this.updateMainData()
      },
      onCloseEditCartridgeData () {
        this.dialog_edit_cartridge_data = false
        this.updateMainData()
      },

      openDialogCartridgeActions (option) {
        this.cartridge_actions_option = option
        this.dialog_cartridge_actions = true
      },
      onConfirmCartridgeActions () {
        this.dialog_cartridge_actions = false
        this.updateMainData()
      },
      onCloseCartridgeActions () {
        this.dialog_cartridge_actions = false
        this.updateMainData()
      },

      openDialogAddNewCartridge () {
        this.dialog_new_cartridge = true
      },
      closeAddNewCartridge () {
        this.dialog_new_cartridge = false
        this.updateMainData()
      },
      addNewCartridgeToList () {
        if (this.new_cartridge_data.model_id && this.new_cartridge_data.department_id) {
          const newItem = {
            ...this.new_cartridge_data,
            count: 1,
          }
          this.new_cartridges.push(newItem)
        }
      },
      removeNewCartridgeItem (index) {
        this.new_cartridges.splice(index, 1)
      },
      addNewCartridge () {
        API.post('add-new-cartridge', this.new_cartridges)
          .then(response => {
            createToast(response.data.result, {
              showIcon: 'true',
              showCloseButton: false,
              type: 'success',
              position: 'top-center',
              timeout: 3000,
              toastBackgroundColor: '#4caf50',
            })
            this.dialog_new_cartridge = false
          })
      },

      getCartridgeItemById (id) {
        return this.cartridge_models.find(item => item.id === id)
      },
      getDepartmentItemById (id) {
        return this.departments.find(item => item.id === id)
      },

      async generatePDF (cartridge_model, cartridge_id) {
        try {
          const response = await API.post('generate-barcode-pdf', {
            model: cartridge_model,
            id: cartridge_id.toString(),
          }, {
            responseType: 'blob', // Важно для получения бинарных данных
          });

          // Создаем URL для blob
          const blob = new Blob([response.data], { type: 'application/pdf' });
          const url = window.URL.createObjectURL(blob)
          window.open(url, '_blank')
          setTimeout(() => {
            window.URL.revokeObjectURL(url)
          }, 1000)

        } catch (error) {
          console.error('Ошибка при генерации PDF:', error);
        }
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
