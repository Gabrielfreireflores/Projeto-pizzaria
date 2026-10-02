import { Navbar } from "@/components/shared/navbar";
import { Hero } from "@/components/shared/hero";
import { MenuSection } from "@/components/shared/menu-section";
import { About } from "@/components/shared/about";
import { Footer } from "@/components/shared/footer";

export default function HomePage() {
  return (
    <main>
      <Navbar />
      <Hero />
      <MenuSection />
      <About />
      <Footer />
    </main>
  );
}