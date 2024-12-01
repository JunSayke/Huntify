import { fetchAndLoadNotifications } from "./huntify.js"

document.addEventListener("DOMContentLoaded", function () {
	fetchAndLoadNotifications("#notification-dropdown ul")
})

export async function markAsRead(id) {
	const response = await fetch(`/notification/${id}/mark-as-read/`, {
		method: "POST",
	})

	if (response.ok) {
		const notificationItem = document.getElementById(`notification-${id}`)
		const button = notificationItem.querySelector(
			`[data-action-button="mark-read-notification"]`
		)
		button.remove() // Remove the button from the DOM
	} else {
		console.error("Failed to mark notification as read")
	}
}

export async function deleteNotification(id) {
	const response = await fetch(`/notification/${id}/delete/`, {
		method: "DELETE",
	})

	if (response.ok) {
		const notificationItem = document.getElementById(`notification-${id}`)
		notificationItem.remove() // Remove the notification from the DOM
		if ()
	} else {
		console.error("Failed to delete notification")
	}
}
