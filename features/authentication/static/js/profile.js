import { initAddressInputListeners } from "./huntify.js"

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

		if (document.getElementById("success-modal")) {
			const successModal = window.FlowbiteInstances.getInstance("Modal", "success-modal");
			if (successModal) {
				successModal.show();
			}
		}

		// Modal confirmation for delete button
		if (document.getElementById("confirmation-modal")) {
			const confirmationModal = window.FlowbiteInstances.getInstance("Modal", "confirmation-modal");
			if (confirmationModal) {
				confirmationModal.textEl = document.querySelector("#confirmation-modal #confirmation-text");
				confirmationModal.confirmButtonEl = document.querySelector("#confirmation-modal #confirmation-confirm-button");

				confirmationModal.updateOnHide = () => {
					confirmationModal.textEl.textContent = "";
					confirmationModal.formEl = null;
				};

				confirmationModal.confirmButtonEl.addEventListener("click", async () => {
					if (confirmationModal.formEl) {
						confirmationModal.formEl.submit();
					}
				});

				// Intercept delete button clicks on the object to show the confirmation modal
				const notificationContainer = document.getElementById("notification-container")
				notificationContainer.addEventListener("click", function(event) {
					// Check if the clicked element is a button with the specific name
					const button = event.target.closest(`[data-action-button="delete-notification"]`);

					if (button.dataset.actionButton == "delete-notification") {
						event.preventDefault();
						confirmationModal.textEl.textContent = `Are you sure you want to delete this notification?`;
						confirmationModal.formEl = button.closest("form.delete-notification-form");
					}
				})
			}
		}

		const tabs = window.FlowbiteInstances.getInstance("Tabs", "default-tab")

		// Check for the initial ?tabs= in the search query
        const urlParams = new URLSearchParams(window.location.search);
        const initialTab = urlParams.get('tab');
        if (initialTab) {
            tabs.show(`#${initialTab}`);
        }

		tabs.updateOnShow(
			() => {
				const activeTab = tabs.getActiveTab()
				const tabId = activeTab.id.substring(1); // Trim the # from the element id
				history.pushState(null, '', `?tab=${tabId}`)
			}
		)
	})

	// Address input listeners initialization
	initAddressInputListeners(
		`#update-user_address_form [data-target-input="province"]`,
		`#update-user_address_form [data-target-input="municipality"]`,
		`#update-user_address_form [data-target-input="barangay"]`
	)
})
