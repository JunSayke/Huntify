document.addEventListener("DOMContentLoaded", async function() {
    try {
        const bookingTableEl = document.getElementById("booking-table");

        // Wait for the window to load before initializing the modals
        window.addEventListener("load", () => {
            const successModal = window.FlowbiteInstances.getInstance("Modal", "success-modal");
            if (successModal) {
                successModal.show();
            }

            // Modal confirmation for delete buttons
            const modal = window.FlowbiteInstances.getInstance("Modal", "confirmation-modal");
            modal.textEl = document.querySelector("#confirmation-modal #confirmation-text");
            modal.confirmButtonEl = document.querySelector("#confirmation-modal #confirmation-confirm-button");

            modal.updateOnHide = () => {
                modal.textEl.textContent = "";
                modal.formEl = null;
            };

            modal.confirmButtonEl.addEventListener("click", async () => {
                if (modal.formEl) {
                    modal.formEl.submit();
                }
            });

            // Intercept delete button clicks on the property to show the confirmation modal
            bookingTableEl.addEventListener("click", async (event) => {
                // Check if the clicked element is a button with the specific name

                const button = event.target;
                switch (button.dataset.actionButton) {
                    case "complete-booking":
                        event.preventDefault();
                        modal.textEl.textContent = `Are you sure you want to check-in this booking? This cannot be undone.`;
                        modal.formEl = button.closest("form.complete-booking-form");
                        break;
                    case "approve-booking":
                        event.preventDefault();
                        modal.textEl.textContent = `Are you sure you want to approve this booking? This cannot be undone.`;
                        modal.formEl = button.closest("form.approve-booking-form");
                        break;
                    case "reject-booking":
                        event.preventDefault();
                        modal.textEl.textContent = `Are you sure you want to reject this booking? This cannot be undone.`;
                        modal.formEl = button.closest("form.reject-booking-form");
                        break;
                    case "delete-booking":
                        event.preventDefault();
                        modal.textEl.textContent = `Are you sure you want to delete this booking? This cannot be undone.`;
                        modal.formEl = button.closest("form.delete-booking-form");
                        break;
                    default:
                        break;
                }
            });
        });

    } catch (error) {
        console.error(error);
    }
});
