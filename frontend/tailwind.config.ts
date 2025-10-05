import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
        poppins: ['var(--font-poppins)', 'sans-serif'],
      },
      colors: {
        'brand-primary': '#9B8BFF',
        'brand-secondary': '#57C5B6',
        'dark-bg': '#1A1A2E',
        'dark-card': '#1F1F3A',
        'dark-input': '#2D2D4A',
      },
    },
  },
  plugins: [],
};
export default config;