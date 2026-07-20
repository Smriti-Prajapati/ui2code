'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

const Logo = () => (
  <svg width="28" height="28" viewBox="0 0 36 36" fill="none" aria-hidden="true">
    <rect width="36" height="36" rx="10" fill="url(#fLg)" />
    <path d="M12 13L8 18l4 5" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M24 13l4 5-4 5" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M20 11l-4 14" stroke="rgba(255,255,255,0.55)" strokeWidth="2" strokeLinecap="round" />
    <defs>
      <linearGradient id="fLg" x1="0" y1="0" x2="36" y2="36" gradientUnits="userSpaceOnUse">
        <stop stopColor="#6366f1" />
        <stop offset="1" stopColor="#8b5cf6" />
      </linearGradient>
    </defs>
  </svg>
)

const TECH_STACK = [
  'React', 'Next.js', 'Tailwind CSS', 'TypeScript',
  'Python', 'Flask', 'OpenCV', 'EasyOCR',
  'YOLOv8', 'Framer Motion', 'WebGL',
]

export default function Footer() {
  return (
    <footer className="relative border-t border-white/[0.06] mt-8">
      {/* Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-px bg-gradient-to-r from-transparent via-indigo-500/40 to-transparent" aria-hidden="true" />

      <div className="max-w-6xl mx-auto px-6 py-16">
        {/* Top */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="grid md:grid-cols-3 gap-10 mb-12"
        >
          {/* Brand column */}
          <div>
            <Link href="/" className="flex items-center gap-2.5 font-bold text-white mb-4 hover:opacity-80 transition-opacity w-fit">
              <Logo />
              <span className="text-lg">ui2code</span>
            </Link>
            <p className="text-slate-500 text-sm leading-relaxed mb-4">
              AI-powered screenshot-to-frontend platform. Upload any UI screenshot, get production-ready React, Next.js, and Tailwind code.
            </p>
            <p className="text-slate-600 text-sm">
              Built by{' '}
              <span className="text-indigo-400 font-medium">Smriti Prajapati</span>
            </p>
          </div>

          {/* Tech stack */}
          <div>
            <h3 className="text-white font-semibold text-sm mb-4 tracking-wide">Tech Stack</h3>
            <div className="flex flex-wrap gap-2">
              {TECH_STACK.map((t) => (
                <span key={t} className="text-xs px-2.5 py-1 rounded-lg glass text-slate-400 border border-white/[0.06]">
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-white font-semibold text-sm mb-4 tracking-wide">Links</h3>
            <ul className="space-y-2.5">
              {[
                { label: 'Features', href: '#features' },
                { label: 'How it works', href: '#pipeline' },
                { label: 'Upload Studio', href: '#studio' },
                { label: 'GitHub', href: 'https://github.com' },
              ].map((l) => (
                <li key={l.label}>
                  <a href={l.href} className="text-sm text-slate-500 hover:text-white transition-colors flex items-center gap-1.5 w-fit">
                    <span className="w-1 h-1 rounded-full bg-indigo-500/50" />
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </motion.div>

        {/* Divider */}
        <div className="h-px bg-white/[0.05] mb-8" />

        {/* Bottom */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-600">
          <p>© 2025 ui2code · Open source · MIT License</p>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            <span>Flask backend · Next.js frontend</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
