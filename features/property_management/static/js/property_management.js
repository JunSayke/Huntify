import { imageInputPreview, initAddressInputListeners } from "./huntify.js";

console.log("property_management.js loaded");

document.addEventListener("DOMContentLoaded", async function() {
    try {
        const form1El = document.getElementById("create-boarding_house");
        const form2El = document.getElementById("create-boarding_room");
        const propertyTableEl = document.getElementById("property-table");

        // Wait for the window to load before initializing the modals
        window.addEventListener("load", () => {
            // Modal display on form error
            if (form1El.querySelector(".error")) {
                window.FlowbiteInstances.getInstance("Modal", "add-boarding-house-modal").show();
            } else if (form2El.querySelector(".error")) {
                window.FlowbiteInstances.getInstance("Modal", "add-boarding-room-modal").show();
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
            propertyTableEl.addEventListener("click", async (event) => {
                // Check if the clicked element is a button with the specific name
                const deleteButton = event.target.closest(`button.delete-property-button`);
                if (deleteButton) {
                    event.preventDefault(); // Prevent form submission
                    const itemName = deleteButton.dataset.itemName;
                    modal.textEl.textContent = `Are you sure you want to delete ${itemName}?`;
                    modal.formEl = deleteButton.closest("form.delete-property-form");
                }
            });
        });


        // Image preview functionality for form fields
        const initImagePreview = (formEl) => {
            const imagesEl = formEl.querySelector(`[data-target-input="images"]`);
            const imagePreviews = formEl.getElementsByClassName("image-preview");
            imageInputPreview(imagesEl, imagePreviews);
        };

        initImagePreview(form1El);
        initImagePreview(form2El);

        // Address input listeners initialization
        const [form1ProvinceEl, form1MunicipalityEl, form1BarangayEl, form1MapIframeEl] = [
            document.querySelector(`[data-target-input="province"]`),
            document.querySelector(`[data-target-input="municipality"]`),
            document.querySelector(`[data-target-input="barangay"]`),
            document.getElementById("map-iframe")
        ];
        initAddressInputListeners(form1ProvinceEl, form1MunicipalityEl, form1BarangayEl, form1MapIframeEl);
    } catch (error) {
        console.error(error);
    }
});
