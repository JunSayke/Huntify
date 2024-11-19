document.addEventListener('DOMContentLoaded', function() {
    const boardingRoomImagesEl = document.getElementsByClassName('boarding-room-image');
    const boardingRoomImageModalEl = document.getElementById('image-modal');
    const boardingRoomImageModalContentEl = boardingRoomImageModalEl.querySelector('#image-modal-content');

    Array.from(boardingRoomImagesEl).forEach((boardingRoomImageEl) => {
        boardingRoomImageEl.addEventListener('click', function() {
            boardingRoomImageModalContentEl.src = this.src;
        });
    });
});