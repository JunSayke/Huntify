import { initAddressInputListeners } from "./huntify.js";

document.addEventListener('DOMContentLoaded', function() {
        const form1El = document.getElementById("update-user_address_form");
        const form2El = document.getElementById("update-user_contact_form");

        // Wait for the window to load before initializing the modals
        window.addEventListener("load", () => {
            // Modal display on form error
            if (form1El.querySelector(".error")) {
                window.FlowbiteInstances.getInstance("Modal", "edit-address-modal").show();
            } else if (form2El.querySelector(".error")) {
                window.FlowbiteInstances.getInstance("Modal", "edit-contact-modal").show();
            }
        });

        // Address input listeners initialization
        const [form1ProvinceEl, form1MunicipalityEl, form1BarangayEl] = [
            form1El.querySelector(`[data-target-input="province"]`),
            form1El.querySelector(`[data-target-input="municipality"]`),
            form1El.querySelector(`[data-target-input="barangay"]`)
        ];

        initAddressInputListeners(form1ProvinceEl, form1MunicipalityEl, form1BarangayEl);
});