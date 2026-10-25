/** @type {import('next').NextConfig} */
// O navegador chama /api/... no próprio Next e ele repassa ao Flask.
// Assim não há CORS e o cookie de sessão (login do funcionário) fica no mesmo domínio.
const BACKEND_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:5000";

const nextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${BACKEND_URL}/api/:path*` }];
  },
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
    ],
  },
};

export default nextConfig;
