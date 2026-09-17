import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        char: "hsl(var(--char))",
        brick: {
          DEFAULT: "hsl(var(--brick))",
          dark: "hsl(var(--brick-dark))",
        },
        crust: "hsl(var(--crust))",
        basil: "hsl(var(--basil))",
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "serif"],
        body: ["var(--font-body)", "sans-serif"],
      },
      borderRadius: {
        sm: "0.25rem",
        DEFAULT: "0.5rem",
        lg: "0.75rem",
      },
      maxWidth: {
        content: "72rem",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
