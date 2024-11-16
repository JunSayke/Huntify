import { DataTable } from "../node_modules/simple-datatables/dist/module.js";

console.log("huntify.js is being used");

export function toTitleCase(str) {
    return str.toLocaleLowerCase().replace(/\b\w/g, function(char) {
        return char.toUpperCase();
    });
}

export function isFunction(functionToCheck) {
    return functionToCheck && {}.toString.call(functionToCheck) === "[object Function]";
}

export function updateURL(param, value) {
    const newUrl = new URL(window.location);
    newUrl.searchParams.set(param, value);
    window.history.pushState({}, "", newUrl);
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