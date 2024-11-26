export function toTitleCase(str) {
    return str.toLocaleLowerCase().replace(/\b\w/g, function(char) {
        return char.toUpperCase();
    });
}

export function generateMapIframe({ province, municipality = "", barangay = "" }) {
    let query = `${province}, Philippines`;
    if (municipality) {
        query = `${municipality}, ${province}, Philippines`;
    }
    if (barangay) {
        query = `${barangay}, ${municipality}, ${province}, Philippines`;
    }
    return `https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3916.579073073073!2d123.8707!3d10.3053!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33a9991b1b1b1b1b%3A0x1b1b1b1b1b1b1b1b!2s${encodeURIComponent(query)}!5e0!3m2!1sen!2sph!4v1698765432100!5m2!1sen!2sph`;
}

export function initAddressInputListeners(provinceSelectQuery, municipalitySelectQuery, barangaySelectQuery, mapIframeQuery = null) {
    const addressProcessor = new AddressProcessor({
        provinceSelectQuery,
        municipalitySelectQuery,
        barangaySelectQuery
    });

    const mapIframeEl = mapIframeQuery ? document.querySelector(mapIframeQuery) : null;
    addressProcessor.loadProvinces(provinceSelectQuery);

    // Handle province changes
    addressProcessor.provinceSelectEl.addEventListener("change", () => {
        addressProcessor.loadMunicipalities();
        addressProcessor.resetSelectOptions(addressProcessor.municipalitySelectEl, "Choose a municipality");
        addressProcessor.resetSelectOptions(addressProcessor.barangaySelectEl, "Choose a barangay");

        if (mapIframeEl) {
            mapIframeEl.src = generateMapIframe(addressProcessor.getAddresses()); // Update the map iframe
        }
    });

    // Handle municipality changes
    addressProcessor.municipalitySelectEl.addEventListener("change", () => {
        addressProcessor.loadBarangays();
        if (mapIframeEl) {
            mapIframeEl.src = generateMapIframe(addressProcessor.getAddresses()); // Update the map iframe
        }
    });

    // Handle barangay changes
    addressProcessor.barangaySelectEl.addEventListener("change", () => {
        if (mapIframeEl) {
            mapIframeEl.src = generateMapIframe(addressProcessor.getAddresses()); // Update the map iframe
        }
    });

    // Check if all inputs have values initially and update the map
    if (
        addressProcessor.provinceSelectEl.value &&
        addressProcessor.municipalitySelectEl.value &&
        addressProcessor.barangaySelectEl.value &&
        mapIframeEl
    ) {
        mapIframeEl.src = generateMapIframe(addressProcessor.getAddresses()); // Update the map iframe
    }
}

export class AddressProcessor {
    constructor({ provinceSelectQuery, municipalitySelectQuery, barangaySelectQuery }) {
        this.PROVINCES_ENDPOINT = "/ajax/provinces/";
        this.MUNICIPALITIES_ENDPOINT = (provinceId) => `/ajax/provinces/${provinceId}/municipalities/`;
        this.BARANGAYS_ENDPOINT = (municipalityId) => `/ajax/municipalities/${municipalityId}/barangays/`;

        // Preload elements based on the provided query selectors
        this.provinceSelectEl = document.querySelector(provinceSelectQuery);
        this.municipalitySelectEl = document.querySelector(municipalitySelectQuery);
        this.barangaySelectEl = document.querySelector(barangaySelectQuery);
    }

    getAddresses() {
        const getText = (selectEl) => selectEl.value ? selectEl.options[selectEl.selectedIndex].text : null;
        return {
            province: getText(this.provinceSelectEl),
            municipality: getText(this.municipalitySelectEl),
            barangay: getText(this.barangaySelectEl)
        };
    }

    resetSelectOptions(selectEl, placeholderText) {
        selectEl.innerHTML = `<option disabled selected value="">${placeholderText}</option>`;
        selectEl.value = ""; // Clear the value of the select input
    }

    loadProvinces() {
        const currentValue = this.provinceSelectEl.value; // Save the current selected value

        fetch(this.PROVINCES_ENDPOINT)
            .then((response) => response.json())
            .then((data) => {
                this.resetSelectOptions(this.provinceSelectEl, "Choose a province");

                data.forEach((province) => {
                    const option = document.createElement("option");
                    option.value = province.id;
                    option.textContent = toTitleCase(province.name);
                    this.provinceSelectEl.appendChild(option);
                });

                // Restore the previously selected value if it still exists
                if (currentValue) {
                    const optionExists = Array.from(this.provinceSelectEl.options).some(
                        (option) => option.value === currentValue
                    );
                    if (optionExists) {
                        this.provinceSelectEl.value = currentValue;
                    }
                }
            })
            .catch((error) => console.error("Error fetching provinces:", error));
    }

    loadMunicipalities() {
        const provinceId = this.provinceSelectEl.value;

        fetch(this.MUNICIPALITIES_ENDPOINT(provinceId))
            .then((response) => response.json())
            .then((data) => {
                this.resetSelectOptions(this.municipalitySelectEl, "Choose a municipality");
                data.forEach((municipality) => {
                    const option = document.createElement("option");
                    option.value = municipality.id;
                    option.textContent = toTitleCase(municipality.name);
                    this.municipalitySelectEl.appendChild(option);
                });
            })
            .catch((error) => {
                console.error("Error fetching municipalities:", error);
                this.resetSelectOptions(this.municipalitySelectEl, "Choose a municipality");
            });
    }

    loadBarangays() {
        const municipalityId = this.municipalitySelectEl.value;

        fetch(this.BARANGAYS_ENDPOINT(municipalityId))
            .then((response) => response.json())
            .then((data) => {
                this.resetSelectOptions(this.barangaySelectEl, "Choose a barangay");
                data.forEach((barangay) => {
                    const option = document.createElement("option");
                    option.value = barangay.id;
                    option.textContent = toTitleCase(barangay.name);
                    this.barangaySelectEl.appendChild(option);
                });
            })
            .catch((error) => {
                console.error("Error fetching barangays:", error);
                this.resetSelectOptions(this.barangaySelectEl, "Choose a barangay");
            });
    }
}


export class SimpleImageUploader {
    constructor(fileInputSelector, previewContainerSelector, options = {}) {
        this.fileInput = document.querySelector(fileInputSelector);
        this.previewContainer = document.querySelector(previewContainerSelector);
        this.maxImages = options.maxImages || 1;
        this.currentFiles = [];
        this.renderPreview = options.renderPreview || this.#defaultRenderPreview;
        this.fileInputListener = (options.fileInputListener || this.#defaultFileInputListener).bind(this);

        this.init();
    }

    #defaultFileInputListener = () => this.addImages(this.fileInput.files);

    async init() {
        const existingImages = await Promise.all(
            Array.from(this.previewContainer.querySelectorAll("img.preview.hidden")).map(img =>
                this.urlToFile(img.src)
            )
        );

        this.addImages(existingImages);

        this.fileInput.addEventListener("change", this.fileInputListener);
    }

    async urlToFile(url) {
        const response = await fetch(url);
        const data = await response.blob();
        const contentType = data.type;
        const contentDisposition = response.headers.get("Content-Disposition");

        if (contentDisposition && contentDisposition.includes("filename=")) {
            const match = contentDisposition.match(/filename="?(.+?)"?$/);
            if (match && match[1]) {
                const filename = match[1];
                return new File([data], filename, { type: contentType });
            }
        }

        return null;
    }

    addImages(files) {
        if (!files || files.length === 0) return; // Check if files is empty
        const newFiles = Array.from(files).slice(0, this.maxImages - this.currentFiles.length);
        if (newFiles.length === 0) return alert("Maximum image limit reached.");
        newFiles.forEach(file => {
            const reader = new FileReader();
            reader.onload = () => this.createPreview(file, reader.result);
            reader.readAsDataURL(file);
        });
    }

    createPreview(file, src) {
        const previewElement = this.renderPreview(file, src);
        if (!previewElement) return;

        this.attachPreviewActions(previewElement, file);
        this.previewContainer.appendChild(previewElement);
        this.currentFiles.push(file);
        this.updateFileInput();
    }

    attachPreviewActions(previewElement, file) {
        previewElement.querySelector(`[data-preview-action="remove"]`)?.addEventListener("click", () => this.deleteImage(file, previewElement));
        previewElement.querySelector(`[data-preview-action="replace"]`)?.addEventListener("click", () => this.replaceImage(file, previewElement));
    }

    deleteImage(file, previewElement) {
        this.currentFiles = this.currentFiles.filter(f => f !== file);
        previewElement.remove();
        this.updateFileInput();
    }

    replaceImage(oldFile, previewElement) {
        const newInput = document.createElement("input");
        newInput.type = "file";
        newInput.accept = "image/*";
        newInput.style.display = "none";

        newInput.addEventListener("change", () => {
            const newFile = newInput.files[0];
            if (newFile) {
                const reader = new FileReader();
                reader.onload = () => {
                    this.currentFiles[this.currentFiles.indexOf(oldFile)] = newFile;
                    previewElement.querySelector("img").src = reader.result;
                    this.updateFileInput();
                };
                reader.readAsDataURL(newFile);
            }
        });

        document.body.appendChild(newInput);
        newInput.click();
        document.body.removeChild(newInput);
    }

    updateFileInput() {
        const dataTransfer = new DataTransfer();
        this.currentFiles.forEach(file => dataTransfer.items.add(file));
        this.fileInput.files = dataTransfer.files;
    }

    #defaultRenderPreview(file, src) {
        const previewDiv = document.createElement("div");
        previewDiv.classList.add("preview");

        previewDiv.innerHTML = `
            <img src="${src}" alt="Image Preview">
            <button type="button" data-preview-action="replace">Replace</button>
            <button type="button" data-preview-action="remove">Remove</button>
        `;

        return previewDiv;
    }
}
