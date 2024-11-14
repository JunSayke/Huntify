import { DataTable } from "../node_modules/simple-datatables/dist/module.js";

console.log("huntify.js is being used");

function toTitleCase(str) {
    return str.toLocaleLowerCase().replace(/\b\w/g, function(char) {
        return char.toUpperCase();
    });
}

function isFunction(functionToCheck) {
    return functionToCheck && {}.toString.call(functionToCheck) === "[object Function]";
}


export function generateMapIframe(province, municipality = "", barangay = "") {
    let query = `${province}, Philippines`;
    if (municipality) {
        query = `${municipality}, ${province}, Philippines`;
    }
    if (barangay) {
        query = `${barangay}, ${municipality}, ${province}, Philippines`;
    }
    return `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3916.579073073073!2d123.8707!3d10.3053!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33a9991b1b1b1b1b%3A0x1b1b1b1b1b1b1b1b!2s${encodeURIComponent(query)}!5e0!3m2!1sen!2sph!4v1698765432100!5m2!1sen!2sph`;
}

// TODO: When refreshing the page, the current table page should be retained
export function initDataTable(tableEl, searchInputEl) {
    const defaultTable = tableEl;
    if (defaultTable && typeof DataTable !== "undefined") {
        const dataTable = new DataTable(defaultTable, {
            searchable: false, perPage: 5, perPageSelect: false
        });
        if (searchInputEl) {
            searchInputEl.addEventListener("input", function() {
                dataTable.search(this.value);
            });
        }
        return dataTable;
    }
}

export function imageInputPreview(fileInputEl, previewImageEls) {
    fileInputEl.addEventListener("change", function(e) {
        const files = this.files;

        for (let i = 0; i < files.length && i < previewImageEls.length; i++) {
            const file = files[i];
            const reader = new FileReader();
            reader.onload = function(event) {
                previewImageEls[i].src = event.target.result;
                previewImageEls[i].classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        }
    });
}

export function initAddressInputListeners(provinceSelectEl, municipalitySelectEl, barangaySelectEl, mapIframeEl = null) {
    const addressProcessor = new AddressProcessor();
    addressProcessor.loadProvinces(provinceSelectEl);
    addressProcessor.loadMunicipalitiesOnProvince(provinceSelectEl, municipalitySelectEl);
    addressProcessor.loadBarangaysOnMunicipality(municipalitySelectEl, barangaySelectEl);

    if (mapIframeEl) {
        addressProcessor.showAddressOnMap(provinceSelectEl, municipalitySelectEl, barangaySelectEl, mapIframeEl);
    }
}

export class AddressProcessor {
    constructor() {
        this.PROVINCES_ENDPOINT = "/ajax/provinces/";
        this.MUNICIPALITIES_ENDPOINT = (provinceId) => `/ajax/provinces/${provinceId}/municipalities/`;
        this.BARANGAYS_ENDPOINT = (municipalityId) => `/ajax/municipalities/${municipalityId}/barangays/`;
    }

    showAddressOnMap(provinceSelectEl, municipalitySelectEl, barangaySelectEl, mapIframeEl) {
        provinceSelectEl.addEventListener("change", () => {
            const province = provinceSelectEl.options[provinceSelectEl.selectedIndex].text;
            mapIframeEl.src = generateMapIframe(province);
        });

        municipalitySelectEl.addEventListener("change", () => {
            const province = provinceSelectEl.options[provinceSelectEl.selectedIndex].text;
            const municipality = municipalitySelectEl.options[municipalitySelectEl.selectedIndex].text;
            mapIframeEl.src = generateMapIframe(province, municipality);
        });

        barangaySelectEl.addEventListener("change", () => {
            const province = provinceSelectEl.options[provinceSelectEl.selectedIndex].text;
            const municipality = municipalitySelectEl.options[municipalitySelectEl.selectedIndex].text;
            const barangay = barangaySelectEl.options[barangaySelectEl.selectedIndex].text;
            mapIframeEl.src = generateMapIframe(province, municipality, barangay);
        });
    }

    loadProvinces(provinceSelectEl) {
        fetch(this.PROVINCES_ENDPOINT)
            .then(response => response.json())
            .then(data => {
                provinceSelectEl.innerHTML = "<option disabled selected value=\"\">Choose a province</option>";
                data.forEach(province => {
                    const option = document.createElement("option");
                    option.value = province.id;
                    option.textContent = toTitleCase(province.name);
                    provinceSelectEl.appendChild(option);
                });
            });
    }

    loadMunicipalitiesOnProvince(provinceSelectEl, municipalitySelectEl) {
        provinceSelectEl.addEventListener("change", () => {
            const provinceId = provinceSelectEl.value;
            const defaultOption = "<option disabled selected value=\"\">Choose a municipality</option>";
            fetch(this.MUNICIPALITIES_ENDPOINT(provinceId))
                .then(response => response.json())
                .then(data => {
                    municipalitySelectEl.innerHTML = defaultOption;
                    data.forEach(municipality => {
                        const option = document.createElement("option");
                        option.value = municipality.id;
                        option.textContent = toTitleCase(municipality.name);
                        municipalitySelectEl.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("Error fetching municipalities:", error);
                    municipalitySelectEl.innerHTML = defaultOption;
                });
        });
    }

    loadBarangaysOnMunicipality(municipalitySelectEl, barangaySelectEl) {
        municipalitySelectEl.addEventListener("change", () => {
            const municipalityId = municipalitySelectEl.value;
            const defaultOption = "<option disabled selected value=\"\">Choose a barangay</option>";
            fetch(this.BARANGAYS_ENDPOINT(municipalityId))
                .then(response => response.json())
                .then(data => {
                    barangaySelectEl.innerHTML = defaultOption;
                    data.forEach(barangay => {
                        const option = document.createElement("option");
                        option.value = barangay.id;
                        option.textContent = toTitleCase(barangay.name);
                        barangaySelectEl.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("Error fetching barangays:", error);
                    municipalitySelectEl.innerHTML = defaultOption;
                });
        });
    }
}

export function renderPropertyTableContent(tableContainerEl, propertyType, {
    searchInputEl = null,
    currentPage = 1
} = {}) {
    return fetch(`/ajax/get-property/${propertyType}/`)
        .then(response => response.text())
        .then(html => {
            tableContainerEl.innerHTML = html;
            const dataTable = initDataTable(
                tableContainerEl.querySelector("table"),
                searchInputEl
            );
            dataTable && dataTable.page(currentPage);
            return dataTable;
        })
        .catch(error => console.error("Error loading table content:", error));
}


/**
 * Initializes the delete confirmation modal.
 *
 * @param {HTMLElement} modalEl - The modal element.
 * @param {NodeList} deleteButtonEl - A NodeList of delete button elements.
 *
 * Datasets:
 * - data-item-name: The name of the item to be deleted, used in the confirmation message.
 * - data-item-id: The ID of the item to be deleted, used to find and remove the item from the DOM.
 * - data-modal-button="confirm": The confirm button inside the modal.
 * - data-modal-button="cancel": The cancel button inside the modal.
 * - data-modal-text: The element inside the modal where the confirmation message is displayed.
 * @param onConfirm - The callback function to be executed
 */
export function initDeleteConfirmationModal(modalEl, deleteButtonEl, onConfirm) {
    const modalConfirmButtonEl = modalEl.querySelector(`[data-modal-button="confirm"]`);
    const modalCancelButtonEl = modalEl.querySelector(`[data-modal-button="cancel"]`);
    const modalTextEl = modalEl.querySelector(`[data-modal-text]`);

    const options = {
        placement: "center-center",
        backdrop: "dynamic",
        closable: true
    };

    const modal = new window.Modal(modalEl, options);
    const modalText = modalTextEl.getAttribute("data-modal-text");

    modalCancelButtonEl.addEventListener("click", () => modal.hide());

    // Attach delete event listener to the delete buttons
    deleteButtonEl.forEach(button => {
        button.addEventListener("click", function() {
            modalTextEl.textContent = modalText.replace("{item}", this.getAttribute("data-item-name"));
            const itemId = this.getAttribute("data-item-id");
            modalConfirmButtonEl.addEventListener("click", () => {
                const listItemEl = this.parentElement.closest(`[data-item-id="${itemId}"]`);
                if (isFunction(onConfirm)) {
                    onConfirm(listItemEl);
                }
                modal.hide();
            }, { once: true });
            modal.show();
        });
    });
}