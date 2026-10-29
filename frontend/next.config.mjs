/** @type {import('next').NextConfig} */
// O navegador chama /api/... no próprio Next e ele repassa ao Flask.
// Assim não há CORS e o cookie de sessão (login do funcionário) fica no mesmo domínio.
const BACKEND_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:5000";

const nextConfig = {
  allowedDevOrigins: ["127.0.0.1", "localhost"],
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${BACKEND_URL}/api/:path*` },
      { source: "/static/uploads/produtos/:path*", destination: `${BACKEND_URL}/static/uploads/produtos/:path*` },
    ];
  },
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
    ],
  },
};

export default nextConfig;
