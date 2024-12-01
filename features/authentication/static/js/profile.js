import { initAddressInputListeners } from "./huntify.js"
import { markAsRead, deleteNotification } from "./notification.js"

document.addEventListener("DOMContentLoaded", function () {
	const form1El = document.getElementById("update-user_address_form")
	const form2El = document.getElementById("update-user_contact_form")

	// Wait for the window to load before initializing the modals
	window.addEventListener("load", () => {
		// Modal display on forms error
		if (form1El.querySelector(".error")) {
			window.FlowbiteInstances.getInstance("Modal", "edit-address-modal").show()
		} else if (form2El.querySelector(".error")) {
			window.FlowbiteInstances.getInstance("Modal", "edit-contact-modal").show()
		}
	})

	// Address input listeners initialization
	initAddressInputListeners(
		`#update-user_address_form [data-target-input="province"]`,
		`#update-user_address_form [data-target-input="municipality"]`,
		`#update-user_address_form [data-target-input="barangay"]`
	)

	// Attach event listeners to the container
	const notificationContainer = document.getElementById(
		"notification-container"
	)

	notificationContainer.addEventListener("click", function (event) {
		if (event.target) {
			// Check if the clicked element is the "Mark as Read" button
			if (event.target.dataset.actionButton == "mark-read-notification") {
				const notificationId = event.target.dataset.id
				markAsRead(notificationId)
			}

			// Check if the clicked element is the "Delete" button
			if (event.target.dataset.actionButton == "delete-notification") {
				const notificationId = event.target.dataset.id
				deleteNotification(notificationId)
			}
		}
	})
})
