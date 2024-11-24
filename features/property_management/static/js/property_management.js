document.addEventListener("DOMContentLoaded", async function() {
    try {
        const propertyTableEl = document.getElementById("property-table");

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
                console.log(modal.formEl);
                if (modal.formEl) {
                    modal.formEl.submit();
                }
            });

            // Intercept delete button clicks on the property to show the confirmation modal
            propertyTableEl.addEventListener("click", async (event) => {
                // Check if the clicked element is a button with the specific name
                const deleteButton = event.target.closest(`button.delete-property-button`);
                if (deleteButton) {
                    event.preventDefault(); // Prevent forms submission
                    const itemName = deleteButton.dataset.itemName;
                    modal.textEl.textContent = `Are you sure you want to delete ${itemName}?`;
                    modal.formEl = deleteButton.closest("form.delete-property-form");
                }
            });
        });

    } catch (error) {
        console.error(error);
    }
});
