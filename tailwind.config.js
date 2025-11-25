/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // all Jinja templates
    "./templates/**/*.jinja", // if you use .jinja
    "./static/**/*.js", // optional if you use JS files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
