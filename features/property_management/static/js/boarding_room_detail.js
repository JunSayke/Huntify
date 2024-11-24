document.addEventListener("DOMContentLoaded", function() {
    const boardingRoomImagesEl = document.getElementsByClassName("boarding-room-image");
    const boardingRoomImageModalEl = document.getElementById("image-modal");
    const boardingRoomImageModalContentEl = boardingRoomImageModalEl.querySelector("#image-modal-content");

    Array.from(boardingRoomImagesEl).forEach((boardingRoomImageEl) => {
        boardingRoomImageEl.addEventListener("click", function() {
            boardingRoomImageModalContentEl.src = this.src;
        });
    });

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

        const cancelBookingForm = document.getElementById("cancel-booking-form");
        const cancelBookingButton = cancelBookingForm.querySelector("button.cancel-booking-button");

        cancelBookingButton.addEventListener("click", function(event) {
            event.preventDefault();
            modal.textEl.textContent = "Are you sure you want to cancel this booking?";
            modal.formEl = cancelBookingForm;
        });
    });
});