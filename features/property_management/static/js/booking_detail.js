document.addEventListener("DOMContentLoaded", async function() {
    try {
        const approveBookingForm = document.querySelector("form#approve-booking-form");
        const rejectBookingForm = document.querySelector("form#reject-booking-form");
        const completeBookingForm = document.querySelector("form#complete-booking-form");
        const deleteBookingForm = document.querySelector("form#delete-booking-form");

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

            if (approveBookingForm) {
                approveBookingForm.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    modal.textEl.textContent = `Are you sure you want to approve this booking? This cannot be undone.`;
                    modal.formEl = approveBookingForm;
                });
            }

            if (rejectBookingForm) {
                rejectBookingForm.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    modal.textEl.textContent = `Are you sure you want to reject this booking? This cannot be undone.`;
                    modal.formEl = rejectBookingForm;
                });
            }

            if (completeBookingForm) {
                completeBookingForm.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    modal.textEl.textContent = `Are you sure you want to check-in this booking? This cannot be undone.`;
                    modal.formEl = completeBookingForm;
                });
            }

            if (deleteBookingForm) {
                deleteBookingForm.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    modal.textEl.textContent = `Are you sure you want to delete this booking? This cannot be undone.`;
                    modal.formEl = deleteBookingForm;
                });
            }
        });

    } catch (error) {
        console.error(error);
    }
});