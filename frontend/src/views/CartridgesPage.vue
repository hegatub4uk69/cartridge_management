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
            <v-btn class="float-end" color="green" prepend-icon="mdi-plus" variant="outlined">НОВЫЙ</v-btn>
          </v-col>
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

  export default {
    name: 'CartridgesPage',
    data () {
      return {
        table_cartridges_search: '',
        cartridgeHeaders: [
          { title: '№', align: 'start', key: 'id' },
          { title: 'Наименование', key: 'model' },
          { title: 'Местоположение', key: 'department' },
          { title: 'Действия', key: 'actions', sortable: false },
        ],
        loadingCartridgesTable: true,
        cartridges: [],
      }
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
