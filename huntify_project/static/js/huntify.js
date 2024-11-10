import "../node_modules/flowbite/dist/flowbite.js";
import { DataTable } from "../node_modules/simple-datatables/dist/module.js";

console.log("huntify.js is being used");

export function test() {
}

function toTitleCase(str) {
    return str.toLocaleLowerCase().replace(/\b\w/g, function(char) {
        return char.toUpperCase();
    });
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

export function initDataTable(tableTag, searchInputTag) {
    const defaultTable = tableTag;
    if (defaultTable && typeof DataTable !== "undefined") {
        const dataTable = new DataTable(defaultTable, {
            searchable: false, perPage: 5, perPageSelect: false
        });
        const tableSearch = searchInputTag;
        if (tableSearch) {
            tableSearch.addEventListener("input", function() {
                dataTable.search(this.value);
            });
        }
    }
}

export function imageInputPreview(fileInputTag, previewImageTags) {
    fileInputTag.addEventListener("change", function(e) {
        const files = this.files;

        for (let i = 0; i < files.length && i < previewImageTags.length; i++) {
            const file = files[i];
            const reader = new FileReader();
            reader.onload = function(event) {
                previewImageTags[i].src = event.target.result;
                previewImageTags[i].classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        }
    });
}

export class AddressProcessor {
    constructor() {
        this.PROVINCES_ENDPOINT = "/ajax/provinces/";
        this.MUNICIPALITIES_ENDPOINT = (provinceId) => `/ajax/provinces/${provinceId}/municipalities/`;
        this.BARANGAYS_ENDPOINT = (municipalityId) => `/ajax/municipalities/${municipalityId}/barangays/`;
    }

    showAddressOnMap(provinceSelectTag, municipalitySelectTag, barangaySelectTag, mapIframeTag) {
        provinceSelectTag.addEventListener("change", () => {
            const province = provinceSelectTag.options[provinceSelectTag.selectedIndex].text;
            mapIframeTag.src = generateMapIframe(province);
        });

        municipalitySelectTag.addEventListener("change", () => {
            const province = provinceSelectTag.options[provinceSelectTag.selectedIndex].text;
            const municipality = municipalitySelectTag.options[municipalitySelectTag.selectedIndex].text;
            mapIframeTag.src = generateMapIframe(province, municipality);
        });

        barangaySelectTag.addEventListener("change", () => {
            const province = provinceSelectTag.options[provinceSelectTag.selectedIndex].text;
            const municipality = municipalitySelectTag.options[municipalitySelectTag.selectedIndex].text;
            const barangay = barangaySelectTag.options[barangaySelectTag.selectedIndex].text;
            mapIframeTag.src = generateMapIframe(province, municipality, barangay);
        });
    }

    loadProvinces(provinceSelectTag) {
        fetch(this.PROVINCES_ENDPOINT)
            .then(response => response.json())
            .then(data => {
                provinceSelectTag.innerHTML = "<option disabled selected value=\"\">Choose a province</option>";
                data.forEach(province => {
                    const option = document.createElement("option");
                    option.value = province.id;
                    option.textContent = toTitleCase(province.name);
                    provinceSelectTag.appendChild(option);
                });
            });
    }

    loadMunicipalitiesOnProvince(provinceSelectTag, municipalitySelectTag) {
        provinceSelectTag.addEventListener("change", () => {
            const provinceId = provinceSelectTag.value;
            const defaultOption = "<option disabled selected value=\"\">Choose a municipality</option>";
            fetch(this.MUNICIPALITIES_ENDPOINT(provinceId))
                .then(response => response.json())
                .then(data => {
                    municipalitySelectTag.innerHTML = defaultOption;
                    data.forEach(municipality => {
                        const option = document.createElement("option");
                        option.value = municipality.id;
                        option.textContent = toTitleCase(municipality.name);
                        municipalitySelectTag.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("Error fetching municipalities:", error);
                    municipalitySelectTag.innerHTML = defaultOption;
                });
        });
    }

    loadBarangaysOnMunicipality(municipalitySelectTag, barangaySelectTag) {
        municipalitySelectTag.addEventListener("change", () => {
            const municipalityId = municipalitySelectTag.value;
            const defaultOption = "<option disabled selected value=\"\">Choose a barangay</option>";
            fetch(this.BARANGAYS_ENDPOINT(municipalityId))
                .then(response => response.json())
                .then(data => {
                    barangaySelectTag.innerHTML = defaultOption;
                    data.forEach(barangay => {
                        const option = document.createElement("option");
                        option.value = barangay.id;
                        option.textContent = toTitleCase(barangay.name);
                        barangaySelectTag.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("Error fetching barangays:", error);
                    municipalitySelectTag.innerHTML = defaultOption;
                });
        });
    }
}