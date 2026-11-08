import assert from 'node:assert/strict';
import { test } from 'node:test';

let sequence = 0;
async function config(env) {
  const previous = { VERCEL: process.env.VERCEL, BACKEND_URL: process.env.BACKEND_URL,
    NEXT_PUBLIC_BLOB_HOST: process.env.NEXT_PUBLIC_BLOB_HOST };
  for (const key of Object.keys(previous)) {
    if (env[key] === undefined) delete process.env[key];
    else process.env[key] = env[key];
  }
  try {
    return (await import(`../next.config.mjs?test=${sequence++}`)).default;
  } finally {
    for (const [key, value] of Object.entries(previous)) {
      if (value === undefined) delete process.env[key];
      else process.env[key] = value;
    }
  }
}

test('desenvolvimento mantém o proxy local', async () => {
  const next = await config({});
  assert.equal((await next.rewrites())[0].destination, 'http://127.0.0.1:5000/api/:path*');
});

test('Vercel exige origem HTTPS explícita e sem credenciais', async () => {
  for (const url of [undefined, 'http://backend.example', 'https://localhost',
    'https://127.0.0.1', 'https://user:password@backend.example', 'https://backend.example/api']) {
    await assert.rejects(config({ VERCEL: '1', BACKEND_URL: url }));
  }
});

test('backend HTTPS preserva caminhos da API e dos uploads', async () => {
  const next = await config({ VERCEL: '1', BACKEND_URL: 'https://backend.example/' });
  assert.deepEqual(await next.rewrites(), [
    { source: '/api/:path*', destination: 'https://backend.example/api/:path*' },
    { source: '/static/uploads/produtos/:path*', destination: 'https://backend.example/static/uploads/produtos/:path*' },
  ]);
});

test('Blob permite apenas o store configurado e mantém imagens anteriores', async () => {
  const next = await config({ NEXT_PUBLIC_BLOB_HOST: 'teststore.public.blob.vercel-storage.com' });
  assert.deepEqual(next.images.remotePatterns, [
    { protocol: 'https', hostname: 'images.unsplash.com' },
    { protocol: 'https', hostname: 'teststore.public.blob.vercel-storage.com', pathname: '/pizzaria/produtos/**' },
  ]);
  await assert.rejects(config({ NEXT_PUBLIC_BLOB_HOST: 'evil.example' }));
});
