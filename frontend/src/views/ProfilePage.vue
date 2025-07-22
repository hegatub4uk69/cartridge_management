<template>
  <v-container fluid="">
    <v-row align="center" justify="center">
      <v-col>
        <v-container fluid="">
          <v-row dense>
            <v-col>
              <v-card elevation="5">
                <v-expansion-panels v-model="panel" variant="accordion">
                  <v-expansion-panel value="user">
                    <template #title>
                      <v-icon icon="mdi-card-account-details-outline" size="35px" style="margin-right: 5px" />
                      <h3>Информация о пользователе</h3>
                    </template>
                    <v-expansion-panel-text>
                      <div class="d-flex flex-no-wrap">
                        <v-avatar
                          class="ma-3"
                          rounded="0"
                          size="160"
                        >
                          <v-card-text>
                            <v-img class="mb-2" src="/free-icon-avatar-8727604.png" />
                            <v-card elevation="2">
                              {{ user_data.post }}
                            </v-card>
                          </v-card-text>
                        </v-avatar>
                        <v-card-text>
                          <v-card-title>Личная информация</v-card-title>
                          <v-divider style="padding-bottom: 20px" />
                          <v-text-field
                            label="Фамилия Имя Отчество"
                            :model-value="user_data.staff_full_name"
                            readonly=""
                          >
                            <template #prepend-inner>
                              <v-icon
                                icon="mdi-card-account-details-outline"
                                style="margin-left: 3px; margin-right: 10px"
                              />
                            </template>
                          </v-text-field>
                          <v-text-field
                            label="Подразделение"
                            :model-value="user_data.department_name"
                            readonly=""
                          >
                            <template #prepend-inner>
                              <v-icon
                                icon="mdi-alpha-p-box-outline"
                                style="margin-left: 3px; margin-right: 10px"
                              />
                            </template>
                          </v-text-field>
                        </v-card-text>
                        <v-card-text>
                          <v-card-title>Статистика по картриджам</v-card-title>
                          <v-divider style="padding-bottom: 20px" />
                          <v-text-field
                            class="text-black"
                            :model-value="'Количество выданных картриджей: ' + orders_count.orders_in"
                            readonly=""
                          >
                            <template #prepend-inner>
                              <v-icon
                                icon="mdi-clipboard-text-clock-outline"
                                style="margin-left: 3px; margin-right: 10px"
                              />
                            </template>
                          </v-text-field>
                          <v-text-field
                            class="text-black"
                            :model-value="'Количество списанных картриджей: ' + orders_count.orders_done"
                            readonly=""
                          >
                            <template #prepend-inner>
                              <v-icon
                                icon="mdi-toolbox-outline"
                                style="margin-left: 3px; margin-right: 10px"
                              />
                            </template>
                          </v-text-field>
                        </v-card-text>
                      </div>
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-card>
            </v-col></v-row></v-container>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

  import { mapState } from 'vuex';
  // import API from '@/axios';

  export default {
    name: 'ProfilePage',

    computed: {
      ...mapState(['user_data']),
      staff_id () {
        return this.$store.state.user_data.uid
      },
    },

    data () {
      return {
        panel: ['user'],
        orders_count: {
          orders_in: null,
          orders_done: null,
          orders_out: null,
        },
      }
    },

    // watch: {
    //   staff_id (val) {
    //     this.ordersStat(val)
    //   },
    // },
    //
    // mounted () {
    //   if (this.staff_id) {
    //     this.ordersStat(this.staff_id)
    //   }
    // },
    //
    // methods: {
    //   ordersStat (staff_id) {
    //     setTimeout(() => {
    //       API.post('get-my-orders-count', { staff_id })
    //         .then(response => {
    //           this.orders_count.orders_in = response.data.result.orders_in
    //           this.orders_count.orders_done = response.data.result.orders_done
    //           this.orders_count.orders_out = response.data.result.orders_out
    //         })
    //     }, 2000)
    //
    //   },
    // },

  }

</script>
