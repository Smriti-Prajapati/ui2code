'use client'

import { motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'

const TYPING_LINES = [
  '<Navigation className="sticky top-0" />',
  '<HeroSection headline={data.title} />',
  '<FeatureGrid items={features} />',
  '<CTAButton variant="primary">Get Started</CTAButton>',
  '<Footer links={footerLinks} />',
]

function TypingEffect() {
  const [displayed, setDisplayed] = useState('')
  const [lineIdx, setLineIdx] = useState(0)
  const [charIdx, setCharIdx] = useState(0)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    const current = TYPING_LINES[lineIdx]
    let timeout: ReturnType<typeof setTimeout>

    if (!deleting && charIdx <= current.length) {
      timeout = setTimeout(() => {
        setDisplayed(current.slice(0, charIdx))
        setCharIdx(charIdx + 1)
      }, 38)
    } else if (!deleting && charIdx > current.length) {
      timeout = setTimeout(() => setDeleting(true), 1800)
    } else if (deleting && charIdx > 0) {
      timeout = setTimeout(() => {
        setDisplayed(current.slice(0, charIdx - 1))
        setCharIdx(charIdx - 1)
      }, 18)
    } else {
      setDeleting(false)
      setLineIdx((lineIdx + 1) % TYPING_LINES.length)
    }
    return () => clearTimeout(timeout)
  }, [charIdx, deleting, lineIdx])

  return (
    <div className="font-mono text-sm text-emerald-400 whitespace-nowrap overflow-hidden">
      {displayed}
      <span className="cursor-blink text-violet-400">|</span>
    </div>
  )
}

// Mock floating UI cards
function MockCard({ className, style, delay = 0 }: { className?: string; style?: React.CSSProperties; delay?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.7, delay, ease: [0.22, 1, 0.36, 1] }}
      className={`absolute glass rounded-2xl overflow-hidden shadow-2xl ${className}`}
      style={style}
    >
      <div className="flex gap-1.5 p-3 border-b border-white/[0.06]">
        <span className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
        <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
        <span className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
      </div>
      <div className="p-3 space-y-2">
        <div className="h-2 bg-indigo-400/20 rounded-full w-4/5" />
        <div className="h-2 bg-violet-400/20 rounded-full w-3/5" />
        <div className="h-2 bg-indigo-400/20 rounded-full w-4/6" />
        <div className="grid grid-cols-3 gap-2 mt-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-8 rounded-lg bg-violet-500/10 border border-violet-500/20" />
          ))}
        </div>
      </div>
    </motion.div>
  )
}

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center pt-24 pb-20 overflow-hidden" id="hero">
      {/* Background glow orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" aria-hidden="true" />
      <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-violet-600/15 rounded-full blur-[100px] pointer-events-none" aria-hidden="true" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-purple-600/8 rounded-full blur-[140px] pointer-events-none" aria-hidden="true" />

      <div className="relative z-10 max-w-7xl mx-auto px-6 w-full grid lg:grid-cols-2 gap-16 items-center">
        {/* Left: copy */}
        <div>
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-3 py-1.5 mb-8 rounded-full border border-violet-500/30 bg-violet-500/10 text-violet-300 text-xs font-semibold tracking-wide uppercase"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" />
            AI-Powered Design-to-Code
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-5xl lg:text-7xl font-black tracking-[-0.04em] leading-[0.95] text-white mb-6"
          >
            Turn any UI<br />
            <span className="gradient-text">screenshot</span><br />
            into code.
          </motion.h1>

          {/* Sub */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg text-slate-400 leading-relaxed mb-8 max-w-lg"
          >
            ui2code analyzes your screenshot, detects every component, understands the layout, and generates production-ready{' '}
            <span className="text-indigo-400 font-medium">React</span>,{' '}
            <span className="text-violet-400 font-medium">Next.js</span>, and{' '}
            <span className="text-cyan-400 font-medium">Tailwind</span> — in seconds.
          </motion.p>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-wrap gap-3 mb-8"
          >
            <a
              href="#studio"
              className="group flex items-center gap-2.5 px-6 py-3.5 font-semibold text-white rounded-xl bg-indigo-600 hover:bg-indigo-500 transition-all duration-200 shadow-[0_0_30px_rgba(99,102,241,0.45)] hover:shadow-[0_0_40px_rgba(99,102,241,0.6)] hover:-translate-y-0.5"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
              Upload Screenshot
              <span className="group-hover:translate-x-0.5 transition-transform duration-200">→</span>
            </a>
            <a
              href="#pipeline"
              className="flex items-center gap-2 px-6 py-3.5 font-semibold text-slate-300 hover:text-white rounded-xl border border-white/[0.1] hover:border-white/[0.2] bg-white/[0.04] hover:bg-white/[0.08] transition-all duration-200 hover:-translate-y-0.5"
            >
              How it works
            </a>
          </motion.div>

          {/* Trust badges */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="flex flex-wrap gap-3 text-xs text-slate-500"
          >
            {['No sign-up needed', 'React / Next.js / HTML', 'Tailwind output', 'Download as ZIP'].map((t) => (
              <span key={t} className="flex items-center gap-1.5">
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                  <circle cx="6" cy="6" r="5" stroke="#10b981" strokeWidth="1.5" />
                  <path d="M3.5 6l1.5 1.5 3-3" stroke="#10b981" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
                {t}
              </span>
            ))}
          </motion.div>
        </div>

        {/* Right: animated code mockup */}
        <motion.div
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.9, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          className="relative hidden lg:block"
        >
          {/* Main code card */}
          <div className="relative border-gradient rounded-2xl overflow-hidden shadow-2xl">
            <div className="glass-light rounded-2xl overflow-hidden">
              {/* Window chrome */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-white/[0.07] bg-white/[0.02]">
                <div className="flex gap-2">
                  <span className="w-3 h-3 rounded-full bg-red-500/70" />
                  <span className="w-3 h-3 rounded-full bg-yellow-500/70" />
                  <span className="w-3 h-3 rounded-full bg-green-500/70" />
                </div>
                <span className="text-xs text-slate-500 font-mono">App.jsx — Generated</span>
                <div className="w-16" />
              </div>
              {/* Code body */}
              <div className="p-5 font-mono text-sm space-y-1.5 bg-[#0d1117]">
                <div><span className="token-kw">import</span> <span className="text-white">React</span> <span className="token-kw">from</span> <span className="token-str">'react'</span></div>
                <div className="h-1" />
                <div><span className="token-kw">export default function</span> <span className="token-fn">GeneratedApp</span><span className="text-slate-400">()</span> <span className="text-slate-400">&#123;</span></div>
                <div className="pl-6"><span className="token-kw">return</span> <span className="text-slate-400">(</span></div>
                <div className="pl-10"><span className="token-tag">&lt;main</span> <span className="token-attr">className</span><span className="text-slate-400">=</span><span className="token-str">"min-h-screen bg-white"</span><span className="token-tag">&gt;</span></div>
                <div className="pl-14">
                  <span className="token-tag">&lt;Navigation</span>
                  <span className="token-attr"> sticky</span>
                  <span className="token-tag"> /&gt;</span>
                </div>
                <div className="pl-14"><span className="token-tag">&lt;HeroSection</span> <span className="token-attr">data</span><span className="text-slate-400">=&#123;</span><span className="text-orange-400">pageData</span><span className="text-slate-400">&#125;</span> <span className="token-tag">/&gt;</span></div>
                <div className="pl-14"><span className="token-tag">&lt;FeatureGrid</span> <span className="token-attr">items</span><span className="text-slate-400">=&#123;</span><span className="text-orange-400">features</span><span className="text-slate-400">&#125;</span> <span className="token-tag">/&gt;</span></div>
                <div className="pl-14"><span className="token-tag">&lt;Footer</span> <span className="token-tag">/&gt;</span></div>
                <div className="pl-10"><span className="token-tag">&lt;/main&gt;</span></div>
                <div className="pl-6"><span className="text-slate-400">)</span></div>
                <div><span className="text-slate-400">&#125;</span></div>
                <div className="pt-2 border-t border-white/[0.04]">
                  <TypingEffect />
                </div>
              </div>
            </div>
          </div>

          {/* Floating score card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8, x: 30 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className="absolute -right-6 top-16 glass rounded-2xl p-4 shadow-xl w-44"
          >
            <p className="text-xs text-slate-500 mb-3 font-medium">Analysis Score</p>
            {[
              { label: 'Components', val: 94, color: 'bg-indigo-500' },
              { label: 'Layout', val: 88, color: 'bg-violet-500' },
              { label: 'Code Quality', val: 97, color: 'bg-emerald-500' },
            ].map((item) => (
              <div key={item.label} className="mb-2.5">
                <div className="flex justify-between text-[11px] text-slate-400 mb-1">
                  <span>{item.label}</span>
                  <span className="text-white font-semibold">{item.val}%</span>
                </div>
                <div className="h-1.5 bg-white/[0.06] rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${item.val}%` }}
                    transition={{ duration: 1, delay: 1 + 0.15 * [94, 88, 97].indexOf(item.val) }}
                    className={`h-full rounded-full ${item.color}`}
                  />
                </div>
              </div>
            ))}
          </motion.div>

          {/* Floating palette card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8, x: -20, y: 20 }}
            animate={{ opacity: 1, scale: 1, x: 0, y: 0 }}
            transition={{ duration: 0.6, delay: 1 }}
            className="absolute -left-8 bottom-12 glass rounded-2xl p-3.5 shadow-xl"
          >
            <p className="text-xs text-slate-500 mb-2.5 font-medium">Extracted palette</p>
            <div className="flex gap-2">
              {['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ec4899'].map((c) => (
                <div key={c} className="w-6 h-6 rounded-md border border-white/10 shadow" style={{ background: c }} title={c} />
              ))}
            </div>
          </motion.div>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.5 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-slate-600"
      >
        <span className="text-xs tracking-widest uppercase">Scroll</span>
        <motion.div
          animate={{ y: [0, 6, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M12 5v14M5 12l7 7 7-7" />
          </svg>
        </motion.div>
      </motion.div>
    </section>
  )
}
