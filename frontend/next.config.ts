import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  async rewrites() {
    // In dev: proxy to local Flask (5000)
    // In prod (Vercel): NEXT_PUBLIC_API_URL points to HF Spaces
    const flaskBase =
      process.env.FLASK_API_URL ||        // server-side only (dev)
      process.env.NEXT_PUBLIC_API_URL ||  // used in prod when FLASK_API_URL not set
      'http://127.0.0.1:5000'

    return [
      { source: '/api/:path*',       destination: `${flaskBase}/api/:path*` },
      { source: '/upload',           destination: `${flaskBase}/upload` },
      { source: '/uploads/:path*',   destination: `${flaskBase}/uploads/:path*` },
      { source: '/download/:path*',  destination: `${flaskBase}/download/:path*` },
      { source: '/health',           destination: `${flaskBase}/health` },
    ]
  },

  images: {
    remotePatterns: [
      { protocol: 'http',  hostname: '127.0.0.1', port: '5000' },
      { protocol: 'http',  hostname: 'localhost',  port: '5000' },
      { protocol: 'https', hostname: '*.hf.space' },
    ],
  },

  allowedDevOrigins: [
    'http://127.0.0.1:5000',
    'http://localhost:5000',
  ],
}

export default nextConfig
