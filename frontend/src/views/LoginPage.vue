<template>
  <v-card class="fill-height">
    <v-container class="fill-height" fluid="">
      <v-row align="center" dense="" justify="center">
        <v-col cols="12" lg="4" md="4" sm="8">
          <v-form
            v-model="form"
            align="center"
            @submit.prevent="onSubmit"
          >
            <v-avatar
              class="ma-3"
              rounded="0"
              size="200"
            >
              <v-img src="/komp-servis.png" />
            </v-avatar>
            <v-card-text>
              <v-text-field
                v-model="username"
                clearable="true"
                color="primary"
                hint="Введите логин для доступа к сайту"
                label="Имя пользователя"
                prepend-inner-icon="mdi-account-circle-outline"
                :readonly="loading"
                :rules="[required]"
              />
              <v-text-field
                v-model="password"
                :append-inner-icon="showPassword ? 'mdi-eye-outline' : 'mdi-eye-off-outline' "
                clearable="true"
                color="primary"
                hint="Введите пароль для доступа к сайту"
                label="Пароль"
                prepend-inner-icon="mdi-lock-outline"
                :readonly="loading"
                :rules="[required]"
                :type="showPassword ? 'text' : 'Password'"
                @click:append-inner="showPassword = !showPassword"
              />
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                v-model="authorize"
                color="success"
                :disabled="!form"
                :loading="loading"
                size="large"
                type="submit"
                variant="elevated"
                @click="login"
              >{{ log_btn_name }}
              </v-btn>
              <v-spacer />
            </v-card-actions>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
  import { createToast } from 'mosha-vue-toastify';
  import 'mosha-vue-toastify/dist/style.css'

  export default {
    name: 'LoginPage',
    data: () => ({
      showPassword: false,
      form: false,
      username: null,
      password: null,
      incorrectAuth: false,
      loading: false,
      authorize: false,
      log_btn_name: 'Авторизация',
    }),

    methods: {
      login () {
        this.$store.dispatch('userLogin', {
          username: this.username,
          password: this.password,
        })
          .then(() => {
            // doesn't work before login
            this.$store.dispatch('userData')
          })
          .catch(function (err) {
            if (err.response) {
              createToast('Неверные аутентификационные данные!', {
                showIcon: 'true',
                showCloseButton: false,
                type: 'danger',
                position: 'top-center',
                timeout: 3000,
                toastBackgroundColor: '#ff5252',
              })
            }
          })
      },
      onSubmit () {
        if (!this.form) return
        this.loading = true
        setTimeout(() => (this.loading = false), 2000)
      },
      required (value) {
        return !!value || 'Поле обязательно для заполнения'
      },
    },
  }
</script>
