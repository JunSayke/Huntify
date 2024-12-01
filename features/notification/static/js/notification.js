import { fetchAndLoadNotifications } from "./huntify.js"

document.addEventListener("DOMContentLoaded", function () {
	fetchAndLoadNotifications("#notification-dropdown")
})
