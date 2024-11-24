import { initAddressInputListeners, SimpleImageUploader } from "./huntify.js";

document.addEventListener("DOMContentLoaded", async function() {
    try {
        window.addEventListener("load", () => {
            const successModal = window.FlowbiteInstances.getInstance("Modal", "success-modal");
            if (successModal) {
                successModal.show();
            }
        });

        // Image uploader initialization
        const imageUploaderConfig = {
            maxImages: 5,
            renderPreview: (file, src) => {
                const previewDiv = document.createElement("div");
                previewDiv.classList.add("preview", "relative", "p-2", "text-2xl", "bg-gray-100", "rounded-lg", "dark:bg-gray-700");

                previewDiv.innerHTML = `
                    <img src="${src}" class="h-64 w-full object-cover" alt="Image Preview">
                    <button type="button" class="text-red-600 dark:text-red-500 hover:text-red-500 dark:hover:text-red-400" data-preview-action="remove">
                        <i class="fa-solid fa-square-minus"></i>
                        <span class="sr-only">Remove image</span>
                    </button>
                    <button type="button" class="text-blue-600 dark:text-blue-500 hover:text-blue-500 dark:hover:text-blue-400" data-preview-action="replace">
                        <i class="fa-solid fa-file-arrow-up"></i>
                        <span class="sr-only">Replace image</span>
                    </button>
                `;

                return previewDiv;
            }
        };

        new SimpleImageUploader(`[data-target-input="images"]`, `.image-preview-container`, imageUploaderConfig);

        // Address input listeners initialization
        initAddressInputListeners(`[data-target-input="province"]`, `[data-target-input="municipality"]`, `[data-target-input="barangay"]`, "#map-iframe");
    } catch (error) {
        console.error(error);
    }
});
