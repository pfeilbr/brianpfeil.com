/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./layouts/**/*.html", "./content/**/*.{md,html}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', "system-ui", "sans-serif"],
      },
      colors: {
        brand: "#0d7ea8",
      },
    },
  },
  plugins: [],
};
