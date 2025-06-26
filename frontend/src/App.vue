<template>
  <v-app>

    <v-app-bar
      app
      color="primary"
    >
      <template #prepend>
        <v-avatar
          rounded="0"
          size="54"
        >
          <v-img src="/komp-servis.png" />
        </v-avatar>
      </template>
      <v-app-bar-title>
        <h3 class="text-h4 white--text">{{ app_name }}</h3>
      </v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer
      v-if="isAuthenticated !== false"
      expand-on-hover=""
      image="/nav_drawer_back.jpg"
      permanent=""
      rail=""
    >
      <v-list>
        <v-list-item
          base-color="white"
          prepend-avatar="/free-icon-avatar-8727604.png"
          :subtitle="user_data.post"
          :title="user_data.staff_full_name"
        />
      </v-list>

      <v-divider />

      <v-list density="compact" nav="">
        <v-list-item
          base-color="white"
          color="red"
          prepend-icon="mdi-account-circle-outline"
          :title="nav_menu.btn_lk"
          :to="links.profile"
          value="lk"
          variant=""
        />
        <v-list-item
          v-if="user_data.post === 'Администратор'"
          base-color="white"
          color="red"
          prepend-icon="mdi-cog-box"
          :title="nav_menu.btn_admin"
          :to="links.admin"
          value="adm_panel"
          variant=""
        />
        <v-list-item
          base-color="white"
          color="red"
          prepend-icon="mdi-warehouse"
          :title="nav_menu.btn_cartridges"
          :to="links.cartridges"
          value="crt"
          variant=""
        />
        <v-list-item
          base-color="white"
          color="red"
          prepend-icon="mdi-clipboard-text-clock-outline"
          :title="nav_menu.btn_cartridges_history"
          :to="links.cartridges_history"
          value="crt_hist"
          variant=""
        />
        <v-list-item
          v-if="user_data.post === 'Администратор'"
          base-color="white"
          color="red"
          prepend-icon="mdi-table-large"
          :title="nav_menu.btn_logs"
          :to="links.logs"
          value="logs"
          variant=""
        />
        <v-list-item
          base-color="white"
          color="red"
          prepend-icon="mdi-logout"
          :title="nav_menu.btn_logout"
          value="logout"
          variant=""
          @click="logout"
        />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

  </v-app>
</template>

<script>
  import router from '@/router';
  import { mapState } from 'vuex';
  import 'mosha-vue-toastify/dist/style.css'

  export default {
    name: 'App',
    computed: mapState(['isAuthenticated', 'user_data']),

    data: () => ({
      app_name: 'Сервисный центр',
      user: {
        fullName: 'Test Test',
        post: 'Test',
      },
      nav_menu: {
        btn_lk: 'Личный кабинет',
        btn_admin: 'Панель администратора',
        btn_logs: 'Журнал действий',
        btn_cartridges: 'Картриджи',
        btn_cartridges_history: 'История картриджей',
        btn_logout: 'Выход',
      },
      links: {
        main: '/',
        log: '/login',
        profile: '/profile',
        cartridges: '/cartridges',
        cartridges_history: '/cartridges_history',
        admin: '/admin',
        logs: '/logs',
      },
    }),

    created () {
      this.$store.dispatch('verifyUser')
    },

    methods: {
      logout () {
        this.$store.dispatch('userLogout')
          .then(() => {
            router.push({ name: 'login' })
            window.location.reload()
          })
          .catch(err => {
            router.push({ name: 'login' })
            console.log(err)
          })
      },
    },
  }
</script>
