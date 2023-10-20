/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: [
    "./unitrack/templates/**/*.{html,htm}",
    "./unitrack/static/**/*.js",
  ],
  theme: {
    fontFamily: {
      display: ['"Mochiy Pop P One"'],
      body: ["Inter"],
    },
    extend: {
      colors: {
        primary: {
          50: "#e0eaff",
          100: "#b0c4ff",
          200: "#81a0ff",
          300: "#4f80fc",
          400: "#1f64f9",
          500: "#0652e0",
          600: "#0034af",
          700: "#001c7e",
          800: "#000b4f",
          900: "#000120",
        },
        secondary: {
          50: "#daf8ff",
          100: "#b2e9fb",
          200: "#86ddf4",
          300: "#59d5ef",
          400: "#2fcfea",
          500: "#15a9d0",
          600: "#0278a3",
          700: "#004e75",
          800: "#002a48",
          900: "#000d1c",
        },
      },
    },
  },
  plugins: [],
};
