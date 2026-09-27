import { Instagram, Facebook, Phone, MapPin } from "lucide-react";

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer id="contato" className="border-t border-border bg-char text-background/80">
      <div className="mx-auto grid max-w-content gap-8 px-4 py-12 sm:px-6 md:grid-cols-3 lg:px-8">
        <div>
          <p className="font-display text-lg font-semibold text-background">
            Pizzaria do Barriga
          </p>
          <p className="mt-2 flex items-center gap-2 text-sm">
            <MapPin className="h-4 w-4" />
            Jardinópolis-SP
          </p>
        </div>

        <div>
          <p className="text-sm font-medium text-background">Contato</p>
          <p className="mt-2 flex items-center gap-2 text-sm">
            <Phone className="h-4 w-4" />
            (16) 0000-0000
          </p>
          <p className="mt-1 text-sm">contato@pizzariadobarriga.com.br</p>
        </div>

        <div>
          <p className="text-sm font-medium text-background">Redes sociais</p>
          <div className="mt-2 flex items-center gap-4">
            <a href="#" aria-label="Instagram" className="hover:text-background">
              <Instagram className="h-5 w-5" />
            </a>
            <a href="#" aria-label="Facebook" className="hover:text-background">
              <Facebook className="h-5 w-5" />
            </a>
          </div>
        </div>
      </div>

      <div className="border-t border-background/10 py-4 text-center text-xs text-background/60">
        © {year} Pizzaria do Barriga. Todos os direitos reservados.
      </div>
    </footer>
  );
}