/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: ["./ssis/templates/**/*.{html,htm}"],
  theme: {
    fontFamily: {
      display: ['"Mochiy Pop P One"'],
      body: ["Inter"],
    },
    extend: {},
  },
  plugins: [],
};
