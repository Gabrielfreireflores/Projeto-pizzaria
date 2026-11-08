/** @type {import('next').NextConfig} */
// O navegador chama /api/... no próprio Next e ele repassa ao Flask.
// Assim não há CORS e o cookie de sessão (login do funcionário) fica no mesmo domínio.
const BACKEND_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:5000";
const backend = new URL(BACKEND_URL);
const isVercel = process.env.VERCEL === "1";
if (backend.username || backend.password || backend.search || backend.hash || backend.pathname !== "/"
    || !["http:", "https:"].includes(backend.protocol)
    || (isVercel && (!process.env.BACKEND_URL || backend.protocol !== "https:"
      || ["localhost", "127.0.0.1", "[::1]"].includes(backend.hostname)))) {
  throw new Error("Configure BACKEND_URL com a origem HTTPS do backend para a Vercel.");
}
const backendOrigin = backend.origin;
const blobHost = process.env.NEXT_PUBLIC_BLOB_HOST;
if (blobHost && !/^[a-z0-9_-]+\.public\.blob\.vercel-storage\.com$/.test(blobHost)) {
  throw new Error('Host público do Blob inválido.');
}

const nextConfig = {
  allowedDevOrigins: ["127.0.0.1", "localhost"],
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${backendOrigin}/api/:path*` },
      { source: "/static/uploads/produtos/:path*", destination: `${backendOrigin}/static/uploads/produtos/:path*` },
    ];
  },
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
      ...(blobHost ? [{ protocol: "https", hostname: blobHost,
        pathname: '/pizzaria/produtos/**' }] : []),
    ],
  },
};

export default nextConfig;
