module.exports = {
  content: ["./src/**/*.{html,js,jsx}"],
  theme: {
    extend: {
      colors: {
        // primary: rgb(24, 33, 109)
        // active: rgb(255, 130, 92)
        // third: rgb(254, 118, 36)
        primary: "#18216d",
        active: "#ff825c",
        third: "#FE7624",
      },

      grayscale: {
        25: "25%",
        50: "50%",
        75: "75%",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
