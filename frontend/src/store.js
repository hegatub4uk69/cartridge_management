import { createStore } from 'vuex';
import API from '@/axios';
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css'
import router from '@/router';


export const store = createStore({
  state: {
    isAuthenticated: undefined,
    uid: null,
    user_data: {
      staff_full_name: null,
      post: null,
      login: null,
      department_id: null,
      department_name: null,
    },
  },
  mutations: {
    removeUserData (state) {
      state.uid = null
      state.user_data.staff_full_name = null
      state.user_data.post = null
      state.user_data.login = null
      state.user_data.department_id = null
      state.user_data.department_name = null
    },
    setUserData (state, { login, uid }) {
      state.user_data.login = login
      state.uid = uid
    },
    setStaffData (state, { staff_full_name, post, department_id, department_name }) {
      state.user_data.staff_full_name = staff_full_name
      state.user_data.post = post
      state.user_data.department_id = department_id
      state.user_data.department_name = department_name
    },
    setAuthStatus (state, { status }) {
      state.isAuthenticated = status
    },
  },
  getters: {
    loggedIn (state) {
      return state.isAuthenticated !== false
    },
    staffId (state) {
      return state.uid
    },
    staffDataExist (state) {
      return state.user_data.login != null
    },
    getStaffPost (state) {
      return state.user_data.post
    },
  },
  actions: {
    verifyUser (context) {
      return new Promise((resolve, reject) => {
        API.post('user-verify', {}).then(response => {
          context.commit('setAuthStatus', { status: true })
          if (response.data.result === 'true') {
            context.dispatch('userData')
          }
          resolve()
        }).catch(err => {
          context.commit('setAuthStatus', { status: false })
          reject(err)
        })
      })
    },
    userLogout (context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve, reject) => {
          API.post('logout-user', {})
            .then(() => {
              context.commit('removeUserData')
              resolve()
            })
            .catch(err => {
              context.commit('removeUserData')
              reject(err)
            })
        })
      }
    },
    userLogin (context, user_credentials) {
      return new Promise((resolve, reject) => {
        API.post('http://localhost:8000/authorize', {
          username: user_credentials.username,
          password: user_credentials.password,
        }).then(response => {
          createToast(response.data.result, {
            showIcon: 'true',
            showCloseButton: false,
            type: 'success',
            position: 'top-center',
            timeout: 3000,
            toastBackgroundColor: '#4caf50',
          })
          context.commit('setAuthStatus', { status: true })
          router.push({ name: 'profile' })
          context.dispatch('userData')
        }).catch(err => {
          reject(err)
          context.commit('setAuthStatus', { status: false })
        })
      })
    },
    userData (context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve, reject) => {
          API.post('get-user-data', {}).then(response => {
            const resp = response.data.result
            /*console.log(resp)*/
            context.commit('setUserData', { login: resp[0]['login'], uid: resp[0]['uid'] })
            context.commit('setStaffData', {
              staff_full_name: resp[0]['full_name'], post: resp[0]['post'],
              department_id: resp[0]['department_id'], department_name: resp[0]['department_name'],
            })
            resolve()
          }).catch(err => {
            reject(err)
          })
        })
      }
    },
  },
})
