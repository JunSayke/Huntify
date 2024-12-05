module.exports = {
    content: [
        "../templates/**/*.html",
        "../../templates/**/*.html",
        "../../**/templates/**/*.html",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        extend: {
            screens: {
                sm: '640px',  // Small screens (mobile)
                md: '768px',  // Medium screens (tablet)
                lg: '1024px', // Large screens (laptop)
                xl: '1280px', // Extra-large screens (desktop)
            },
            fontFamily: {
                sans: ['Inter', 'Roboto', 'ui-sans-serif', 'system-ui', 'sans-serif'], // Added Roboto
                serif: ['Lora', 'Merriweather', 'Georgia', 'serif'], // Added Lora and Merriweather
                poppins: ['Poppins', 'sans-serif'], // Optional if you also use Poppins
                montserrat: ['Montserrat', 'sans-serif'], // Added Montserrat
                oswald: ['Oswald', 'sans-serif'], // Added Oswald
                raleway: ['Raleway', 'sans-serif'], // Added Raleway
                playfair: ['Playfair Display', 'serif'], // Added Playfair Display
                sourceSans: ['Source Sans Pro', 'sans-serif'], // Added Source Sans Pro
            },
            width: {
                'minmax': '1240px'
            },
            minWidth: {
                'minmax': '1240px'
            },
            maxWidth: {
                'minmax': '1240px'
            },
        }
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/aspect-ratio"),
        require("flowbite/plugin")({
            datatables: true
        })
    ]
};
