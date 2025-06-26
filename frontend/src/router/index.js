/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { store } from '@/store';
// import { routes } from 'vue-router/auto-routes'

const routes = [
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/components/Err404NotFound.vue'),
  },
  {
    path: '/',
    name: 'main',
    redirect: () => {
      return '/login'
    },
  },
  {
    path: '/login',
    name: 'login',
    meta: {
      notLogin: true,
    },
    component: () => import('@/views/LoginPage.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    meta: {
      requiresLogin: true,
    },
    component: () => import('@/views/ProfilePage.vue'),
  },
  {
    path: '/cartridges',
    name: 'cartridges',
    meta: {
      requiresLogin: true,
    },
    component: () => import('@/views/CartridgesPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

function getAuthStatus () {
  return new Promise(resolve => {
    if (store.state.isAuthenticated === undefined) {
      const unwatch = store.watch(
        () => store.state.isAuthenticated,
        value => {
          unwatch()
          resolve(value)
        }
      )
    } else {
      resolve(store.state.isAuthenticated)
    }
  })
}

function getStaffPost () {
  return new Promise(resolve => {
    if (store.state.isAuthenticated === true) {
      if (store.state.user_data.post === null) {
        const unwatch = store.watch(
          () => store.state.user_data.post,
          value => {
            unwatch()
            resolve(value)
          }
        )
      } else {
        resolve(store.state.user_data.post)
      }
    } else {
      resolve(false)
    }
  })
}

router.beforeEach(async (to, from, next) => {

  const UserAuthenticated = await getAuthStatus()
  const StaffPost = await getStaffPost()

  if (to.name === 'login' && !UserAuthenticated) {
    // Если пользователь не авторизован и открывается страница входа
    // то не проверяем другие варианты
    next();
  } else if (to.name !== 'login' && !to.matched.some(record => record.meta.notLogin) && !UserAuthenticated) {
    // Если пользователь не авторизован и страница требует авторизации,
    // то идём на страницу входа
    next({ name: 'login' });
  } else if (to.name === 'login' && UserAuthenticated) {
    // Если пользователь авторизован и открывается страница входа,
    // то открываем страницу из ?next=<адрес>
    next({ name: 'profile' });
  } else if (to.name === 'admin' && UserAuthenticated && !StaffPost.includes('Администратор')) {
    next({ name: 'profile' })
  } else if (to.name === 'logs' && UserAuthenticated && !StaffPost.includes('Администратор')) {
    next({ name: 'profile' })
  } else {
    next();
  }

});

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
