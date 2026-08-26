import router from "../router"

import {useUserStore} from "../store/user"
import {useModal} from "./modal"

export function useAuth() {
	const userStore = useUserStore()
	const modal = useModal()

	async function login(email: string, password: string) {
		const response = await fetch("/api/login", {
			method: "POST",
			credentials: "include",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				email,
				password,
			}),
		})

		const data = await response.json()

		if (!response.ok || !data.authenticated) {
			modal.show("Invalid email or password")
			return
		}

		await userStore.initialize()

		await router.push("/")
	}

	async function logout() {
		try {
			const response = await fetch("/api/logout", {
				method: "POST",
				credentials: "include",
			})

			if (!response.ok) {
				modal.show("Logout failed")
				return
			}
		} catch {
			modal.show("Logout failed")
			return
		}

		// Only clear local state after successful logout.
		userStore.clear()

		await router.push("/")
	}

	return {
		login,
		logout,
	}
}