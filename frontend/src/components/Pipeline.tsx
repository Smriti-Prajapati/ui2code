'use client'

import { motion } from 'framer-motion'
import { useRef } from 'react'

const STEPS = [
  {
    num: '01',
    title: 'Screenshot Upload',
    desc: 'Upload any UI — websites, dashboards, mobile apps, Figma frames, or wireframes. PNG, JPG, WEBP up to 10MB.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6">
        <rect x="3" y="3" width="18" height="18" rx="2" /><path d="M3 9h18M9 21V9" />
      </svg>
    ),
    color: 'from-indigo-500 to-blue-600',
    glow: 'rgba(99,102,241,0.3)',
  },
  {
    num: '02',
    title: 'OCR Text Extraction',
    desc: 'EasyOCR reads every visible text element and classifies it — headings, subheadings, button text, labels, captions.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6">
        <path d="M4 6h16M4 12h8M4 18h12" />
      </svg>
    ),
    color: 'from-violet-500 to-purple-600',
    glow: 'rgba(139,92,246,0.3)',
  },
  {
    num: '03',
    title: 'Component Detection',
    desc: 'OpenCV contour analysis + optional YOLOv8 finds buttons, cards, navbars, forms, images, sidebars, and modals.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6">
        <rect x="2" y="3" width="6" height="6" rx="1" /><rect x="9" y="3" width="6" height="6" rx="1" /><rect x="16" y="3" width="6" height="6" rx="1" />
        <rect x="2" y="10" width="6" height="11" rx="1" /><rect x="9" y="10" width="13" height="5" rx="1" /><rect x="9" y="16" width="13" height="5" rx="1" />
      </svg>
    ),
    color: 'from-cyan-500 to-teal-600',
    glow: 'rgba(6,182,212,0.3)',
  },
  {
    num: '04',
    title: 'Layout Intelligence',
    desc: 'Spacing, alignment, grids, and flex relationships are inferred from pixel positions into semantic layout patterns.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
      </svg>
    ),
    color: 'from-emerald-500 to-green-600',
    glow: 'rgba(16,185,129,0.3)',
  },
  {
    num: '05',
    title: 'AI Reasoning',
    desc: 'Components get semantic names, ARIA labels, responsive breakpoints, and accessibility roles — via rules or GPT-4.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6">
        <circle cx="12" cy="12" r="3" /><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83" />
      </svg>
    ),
    color: 'from-amber-500 to-orange-600',
    glow: 'rgba(245,158,11,0.3)',
  },
  {
    num: '06',
    title: 'Code Generation',
    desc: 'Output as a full Next.js + Tailwind project, React app, or vanilla HTML/CSS/JS — packaged as a runnable ZIP.',
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6">
        <polyline points="16 18 22 12 16 6" /><polyline points="8 6 2 12 8 18" />
      </svg>
    ),
    color: 'from-pink-500 to-rose-600',
    glow: 'rgba(236,72,153,0.3)',
  },
]

export default function Pipeline() {
  return (
    <section id="pipeline" className="py-28 px-6 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-indigo-950/10 to-transparent pointer-events-none" aria-hidden="true" />

      <div className="relative z-10 max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-flex items-center gap-2 px-3 py-1.5 mb-5 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-300 text-xs font-semibold tracking-wide uppercase">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
            The Pipeline
          </span>
          <h2 className="text-4xl lg:text-5xl font-black text-white tracking-[-0.03em] mb-4">
            From screenshot to code<br />
            <span className="gradient-text">in one intelligent pipeline</span>
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Every stage builds on the last — giving you accurate, structured, production-ready frontend output.
          </p>
        </motion.div>

        {/* Steps grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {STEPS.map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.5, delay: i * 0.08 }}
              whileHover={{ y: -6, transition: { duration: 0.2 } }}
              className="group glass rounded-2xl p-6 hover:border-white/[0.15] transition-all duration-300"
              style={{ '--step-glow': step.glow } as React.CSSProperties}
            >
              {/* Step number */}
              <div className="flex items-start justify-between mb-5">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${step.color} flex items-center justify-center text-white shadow-lg`}
                  style={{ boxShadow: `0 8px 24px ${step.glow}` }}>
                  {step.icon}
                </div>
                <span className="text-3xl font-black text-white/[0.06] leading-none font-mono">{step.num}</span>
              </div>

              <h3 className="text-white font-bold text-lg mb-2 group-hover:text-indigo-300 transition-colors">{step.title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{step.desc}</p>

              {/* Connector line (not last row) */}
              {i < STEPS.length - 1 && (
                <div className="mt-5 h-px bg-gradient-to-r from-white/[0.06] to-transparent" />
              )}
            </motion.div>
          ))}
        </div>

        {/* Connecting arrow */}
        <motion.div
          initial={{ opacity: 0, scaleX: 0 }}
          whileInView={{ opacity: 1, scaleX: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="mt-14 flex items-center justify-center gap-3 text-slate-500"
        >
          <div className="h-px flex-1 max-w-xs bg-gradient-to-r from-transparent to-indigo-500/40" />
          <div className="flex items-center gap-2 px-4 py-2 glass rounded-full text-sm">
            <span className="text-indigo-400">⚡</span>
            <span>End-to-end in seconds</span>
          </div>
          <div className="h-px flex-1 max-w-xs bg-gradient-to-l from-transparent to-indigo-500/40" />
        </motion.div>
      </div>
    </section>
  )
}
