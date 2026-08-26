import {ref} from "vue"

const isOpen = ref(false)
const message = ref("")

export function useModal() {
	function show(text: string) {
		message.value = text
		isOpen.value = true
	}

	function close() {
		isOpen.value = false
		message.value = ""
	}

	return {
		isOpen,
		message,
		show,
		close,
	}
}