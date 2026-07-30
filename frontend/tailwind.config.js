/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // "ink" is the base dark surface scale - not pure black, has a
        // slight blue tint so it doesn't feel like a generic #000 dark mode.
        ink: {
          950: "#0F1218",
          900: "#161A22",
          800: "#1E2430",
          700: "#2A3140",
          600: "#3B4456",
        },
        // "signal" is the single accent color - a cyan-teal that reads as
        // "connection / live link" rather than a generic brand blue.
        signal: {
          400: "#5EEAD4",
          500: "#2DD4BF",
          600: "#14B8A6",
        },
        // Warm accent reserved only for destructive actions, so it never
        // competes with "signal" as a second brand color.
        danger: {
          400: "#FB7185",
          500: "#F43F5E",
        },
      },
      fontFamily: {
        // Display face: geometric, slightly technical - used sparingly for
        // headings only.
        display: ["'Space Grotesk'", "system-ui", "sans-serif"],
        // Body face: neutral, highly legible for UI text.
        sans: ["'Inter'", "system-ui", "sans-serif"],
        // Utility face: short codes, URLs, timestamps - anything that is
        // literally "data" gets monospace treatment to read as a value,
        // not prose.
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};
