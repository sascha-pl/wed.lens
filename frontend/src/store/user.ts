import {defineStore} from "pinia"
import {ref} from "vue"

interface AppUser {
	name: string
	email: string
}

interface InitializeResponse {
	authenticated: boolean
	user: AppUser | null
}

export const useUserStore = defineStore("user", () => {
	const initialized = ref(false)
	const authenticated = ref(false)
	const user = ref<AppUser | null>(null)
	const error = ref(false)

	async function initialize() {
		try {
			const response = await fetch("/api/initialize", {
				credentials: "include",
			})

			if (!response.ok) {
				error.value = true
				return
			}

			const data: InitializeResponse = await response.json()

			authenticated.value = data.authenticated
			user.value = data.user
		} catch {
			error.value = true
		} finally {
			initialized.value = true
		}
	}

	function clear() {
		initialized.value = true
		authenticated.value = false
		user.value = null
		error.value = false
	}

	return {
		initialized,
		authenticated,
		user,
		error,
		initialize,
		clear,
	}
})