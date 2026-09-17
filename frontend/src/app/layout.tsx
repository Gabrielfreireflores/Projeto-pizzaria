import type { Metadata } from "next";
import { Fraunces, Public_Sans } from "next/font/google";
import "./globals.css";

const fraunces = Fraunces({
  subsets: ["latin"],
  weight: ["500", "600", "700"],
  variable: "--font-display",
  display: "swap",
});

const publicSans = Public_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-body",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Pizzaria do Barriga | Jardinópolis-SP",
  description:
    "Pizzas artesanais assadas em forno a lenha, feitas com carinho em Jardinópolis-SP. Peça a sua pelo cardápio online.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR" className={`${fraunces.variable} ${publicSans.variable}`}>
      <body>{children}</body>
    </html>
  );
}
