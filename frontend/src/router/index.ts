import {createRouter, createWebHistory} from 'vue-router'

import {useUserStore} from '../store/user.ts'

import AboutView from '../views/AboutView.vue'
import HomeRouterView from '../views/HomeRouterView.vue'
import LoginView from '../views/LoginView.vue'
import CreateAccountView from '../views/CreateAccountView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: '/',
			name: 'home',
			component: HomeRouterView,
		},
		{
			path: '/about',
			name: 'about',
			component: AboutView,
		},
		{
			path: '/login',
			name: 'login',
			component: LoginView,
		},
		{
			path: '/create-account',
			name: 'create-account',
			component: CreateAccountView,
		},
		{
			path: '/profile',
			name: 'profile',
			component: ProfileView,
			meta: {requiresAuth: true},
		},
	],
})

router.beforeEach(async (to) => {
	const userStore = useUserStore()

	if (!userStore.initialized) {
		await userStore.initialize()
	}

	if (to.meta.requiresAuth && !userStore.authenticated) {
		return {
			name: "login",
			query: {
				redirect: to.fullPath,
			},
		}
	}
})

export default router
