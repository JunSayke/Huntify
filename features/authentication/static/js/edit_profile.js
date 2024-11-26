import { SimpleImageUploader, initAddressInputListeners } from "./huntify.js";

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

    new SimpleImageUploader(`#update-user_profile_form [data-target-input="profile-pic"]`, `#update-user_profile_form .image-preview-container`, {
        renderPreview: (file, src) => {
            const previewDiv = document.createElement("div");
            previewDiv.classList.add("preview");
            previewDiv.classList.add("size-full");

            previewDiv.innerHTML = `
            <img src="${src}" class="relative z-20 size-full object-cover" alt="Image Preview">
        `;

            return previewDiv;
        },
        fileInputListener: function() {
            console.log(this)
            const file = this.fileInput.files[0];

            if (file) {
                const reader = new FileReader();
                reader.onload = () => {
                    const previewElement = this.renderPreview(file, reader.result);
                    this.previewContainer.innerHTML = ""; // Clear existing previews
                    this.previewContainer.appendChild(previewElement);
                    alert("File uploaded successfully!");
                    this.currentFiles = [file]; // Replace current files with the new file
                    this.updateFileInput();
                };
                reader.readAsDataURL(file);
            }
        }.bind(this)
    });

    // Address input listeners initialization
    initAddressInputListeners(`#update-user_address_form [data-target-input="province"]`, `#update-user_address_form [data-target-input="municipality"]`, `#update-user_address_form [data-target-input="barangay"]`);
});