import { initAddressInputListeners } from "./huntify.js";

document.addEventListener("DOMContentLoaded", function() {
    const form1El = document.getElementById("update-user_address_form");
    const form2El = document.getElementById("update-user_contact_form");

    // Wait for the window to load before initializing the modals
    window.addEventListener("load", () => {
        // Modal display on forms error
        if (form1El.querySelector(".error")) {
            window.FlowbiteInstances.getInstance("Modal", "edit-address-modal").show();
        } else if (form2El.querySelector(".error")) {
            window.FlowbiteInstances.getInstance("Modal", "edit-contact-modal").show();
        }
    });

    // Address input listeners initialization
    initAddressInputListeners(`#update-user_address_form [data-target-input="province"]`, `#update-user_address_form [data-target-input="municipality"]`, `#update-user_address_form [data-target-input="barangay"]`);
});