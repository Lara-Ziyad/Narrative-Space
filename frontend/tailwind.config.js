module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        deepTeal: '#1C3334',
        forestDark: '#212A25',
        sunrose: '#D98571',
        amberwood: '#D98C2B',
        dustblue: '#4F7E8A',
        phosGreen: '#4FD170',
        cream: '#f0e9dc',
      },
      fontFamily: {
        modern: ['"IBM Plex Sans"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
