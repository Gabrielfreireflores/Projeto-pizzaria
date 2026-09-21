import { Navbar } from "@/components/shared/navbar";
import { Hero } from "@/components/shared/hero";
import { MenuSection } from "@/components/shared/menu-section";

export default function HomePage() {
  return (
    <main>
      <Navbar />
      <Hero />
      <MenuSection />
    </main>
  );
}