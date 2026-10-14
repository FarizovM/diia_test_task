/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'diia-dark': '#1C1C1E',
        'diia-light': '#F5F5F7',
        'diia-primary': '#000000',
        'diia-accent': '#C6F150',
      }
    },
  },
  plugins: [],
}