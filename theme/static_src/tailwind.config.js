module.exports = {
    content: [
        "../templates/**/*.html",
        "../../templates/**/*.html",
        "../../**/templates/**/*.html",
        "./node_modules/flowbite/**/*.js"
    ],
    darkMode: 'class',
    theme: {
        extend: {
            screens: {
                sm: '640px',  // Small screens (mobile)
                md: '768px',  // Medium screens (tablet)
                lg: '1024px', // Large screens (laptop)
                xl: '1280px', // Extra-large screens (desktop)                
            },
            colors: {
                primary: {
                    "50": "#eff6ff",
                    "100": "#dbeafe",
                    "200": "#bfdbfe",
                    "300": "#93c5fd",
                    "400": "#60a5fa",
                    "500": "#3b82f6",
                    "600": "#2563eb",
                    "700": "#1d4ed8",
                    "800": "#1e40af",
                    "900": "#1e3a8a",
                    "950": "#172554"
                }
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
                body: [
                    'Inter', 
                    'ui-sans-serif', 
                    'system-ui', 
                    '-apple-system', 
                    'system-ui', 
                    'Segoe UI', 
                    'Roboto', 
                    'Helvetica Neue', 
                    'Arial', 
                    'Noto Sans', 
                    'sans-serif', 
                    'Apple Color Emoji', 
                    'Segoe UI Emoji', 
                    'Segoe UI Symbol', 
                    'Noto Color Emoji'
                ]
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
            keyframes: {
                fadeIn: {
                  '0%': { opacity: 0 },
                  '100%': { opacity: 1 },
                },
            },
            animation: {
                fadeIn: 'fadeIn 1s ease-in-out',
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
