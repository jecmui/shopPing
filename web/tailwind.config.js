/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'beige': '#D9D9D9',
        'white': '#F0F8FF',
        'black': '#1B1B1B',
        'blue': '#93B7BE',
        'green': '#215841',
        'red': '#C00F0C',
      }
    },
  },
  plugins: [],
}