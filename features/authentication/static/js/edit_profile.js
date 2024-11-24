import { imageInputPreview, initAddressInputListeners } from "./huntify.js";

document.addEventListener("DOMContentLoaded", function() {
    const form1El = document.getElementById("update-user_profile_form");
    const form2El = document.getElementById("update-user_address_form");
    const form3El = document.getElementById("update-user_contact_form");

    // Wait for the window to load before initializing the modals
    window.addEventListener("load", () => {
        // Modal display on forms error
        if (form2El.querySelector(".error")) {
            window.FlowbiteInstances.getInstance("Modal", "edit-address-modal").show();
        } else if (form3El.querySelector(".error")) {
            window.FlowbiteInstances.getInstance("Modal", "edit-contact-modal").show();
        }
    });

    const profilePictureEl = form1El.querySelector(`[data-target-input="profile-pic"]`);
    const profilePicturePreviewEl = form1El.querySelector("#profile-pic-preview");

    imageInputPreview(profilePictureEl, [profilePicturePreviewEl]);

    // Address input listeners initialization
    const [form2ProvinceEl, form2MunicipalityEl, form2BarangayEl] = [
        form2El.querySelector(`[data-target-input="province"]`),
        form2El.querySelector(`[data-target-input="municipality"]`),
        form2El.querySelector(`[data-target-input="barangay"]`)
    ];

    initAddressInputListeners(form2ProvinceEl, form2MunicipalityEl, form2BarangayEl);
});