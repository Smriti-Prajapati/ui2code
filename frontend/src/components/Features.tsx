'use client'

import { motion } from 'framer-motion'

const FEATURES = [
  {
    title: 'OCR Text Extraction',
    desc: 'EasyOCR captures every text element — headings, labels, buttons, captions — preserving semantic roles so code stays accurate.',
    icon: '🔤',
    accent: '#6366f1',
    tag: 'EasyOCR',
  },
  {
    title: 'Component Detection',
    desc: 'Buttons, cards, navbars, forms, sidebars, modals — detected with confidence scores using OpenCV + optional YOLOv8.',
    icon: '🧩',
    accent: '#8b5cf6',
    tag: 'OpenCV · YOLO',
  },
  {
    title: 'Layout Intelligence',
    desc: 'Converts absolute pixel positions into semantic flex and grid layouts by reading spacing, alignment, and nesting depth.',
    icon: '📐',
    accent: '#06b6d4',
    tag: 'Spatial analysis',
  },
  {
    title: 'Design System Extraction',
    desc: 'K-means color clustering extracts your palette. Typography scale, spacing, border radii, and shadows become CSS tokens.',
    icon: '🎨',
    accent: '#10b981',
    tag: 'sklearn KMeans',
  },
  {
    title: 'Multi-Framework Output',
    desc: 'Next.js + Tailwind, React + Tailwind, or HTML/CSS/JS — all from one screenshot, packaged as a runnable project ZIP.',
    icon: '⚡',
    accent: '#f59e0b',
    tag: 'React · Next.js · HTML',
  },
  {
    title: 'Accessibility Built-in',
    desc: 'Generated components ship with ARIA roles, labels, and semantic HTML — so your code starts accessible by default.',
    icon: '♿',
    accent: '#ec4899',
    tag: 'WCAG ready',
  },
  {
    title: 'AI Semantic Reasoning',
    desc: 'Rule-based or GPT-4 powered naming gives components names like HeroSection, CTAButton, NavigationBar — ready to ship.',
    icon: '🤖',
    accent: '#a855f7',
    tag: 'GPT-4 · Rule-based',
  },
  {
    title: 'Visual Similarity Score',
    desc: 'Heuristic evaluation metrics give you component detection accuracy, OCR confidence, layout quality, and code score.',
    icon: '📊',
    accent: '#3b82f6',
    tag: 'Evaluation engine',
  },
  {
    title: 'One-Click Download',
    desc: 'Download a complete ZIP with your generated project, static HTML fallback, analysis JSON, and original screenshot.',
    icon: '📦',
    accent: '#14b8a6',
    tag: 'ZIP bundle',
  },
]

export default function Features() {
  return (
    <section id="features" className="py-28 px-6 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-violet-950/10 to-transparent pointer-events-none" aria-hidden="true" />

      <div className="relative z-10 max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mb-14"
        >
          <span className="inline-flex items-center gap-2 px-3 py-1.5 mb-5 rounded-full border border-violet-500/30 bg-violet-500/10 text-violet-300 text-xs font-semibold tracking-wide uppercase">
            <span className="w-1.5 h-1.5 rounded-full bg-violet-400" />
            Capabilities
          </span>
          <h2 className="text-4xl lg:text-5xl font-black text-white tracking-[-0.03em] mb-4">
            Everything a frontend engineer<br />
            <span className="gradient-text-warm">needs — automated</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-xl">
            From pixel-perfect detection to accessible, production-ready code — in one shot.
          </p>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {FEATURES.map((f, i) => (
            <motion.article
              key={f.title}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ duration: 0.5, delay: i * 0.06 }}
              whileHover={{ y: -5, transition: { duration: 0.2 } }}
              className="group glass rounded-2xl p-5 hover:border-white/[0.14] transition-all duration-300 cursor-default"
            >
              {/* Icon */}
              <div
                className="w-11 h-11 rounded-xl flex items-center justify-center text-xl mb-4 border"
                style={{
                  background: `${f.accent}18`,
                  borderColor: `${f.accent}30`,
                  boxShadow: `0 4px 16px ${f.accent}20`,
                }}
              >
                {f.icon}
              </div>

              <h3 className="text-white font-bold text-[15px] mb-1.5 group-hover:text-indigo-300 transition-colors">
                {f.title}
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-3">{f.desc}</p>

              {/* Tag */}
              <span
                className="inline-flex text-[11px] font-semibold px-2 py-0.5 rounded-full border"
                style={{
                  color: f.accent,
                  borderColor: `${f.accent}30`,
                  background: `${f.accent}12`,
                }}
              >
                {f.tag}
              </span>
            </motion.article>
          ))}
        </div>
      </div>
    </section>
  )
}
