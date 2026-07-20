'use client'

import { useState, useEffect, useCallback, use } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import { analyzeImage, downloadUrl, imageUrl, type AnalysisResult } from '@/lib/api'

// ── Logo ──────────────────────────────────────────────────────────────────────
const Logo = () => (
  <svg width="28" height="28" viewBox="0 0 36 36" fill="none" aria-hidden="true">
    <rect width="36" height="36" rx="10" fill="url(#sLg)" />
    <path d="M12 13L8 18l4 5" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M24 13l4 5-4 5" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M20 11l-4 14" stroke="rgba(255,255,255,0.55)" strokeWidth="2" strokeLinecap="round" />
    <defs>
      <linearGradient id="sLg" x1="0" y1="0" x2="36" y2="36" gradientUnits="userSpaceOnUse">
        <stop stopColor="#6366f1" /><stop offset="1" stopColor="#8b5cf6" />
      </linearGradient>
    </defs>
  </svg>
)

// ── Metric card ───────────────────────────────────────────────────────────────
function MetricCard({ label, value, color }: { label: string; value: number | null; color: string }) {
  const pct = value !== null ? Math.round(value * 100) : null
  return (
    <div className="glass rounded-xl p-4 flex flex-col gap-2">
      <span className="text-xs text-slate-500 font-medium">{label}</span>
      <strong className="text-2xl font-black text-white leading-none">
        {pct !== null ? `${pct}%` : '—'}
      </strong>
      {pct !== null && (
        <div className="h-1 bg-white/[0.06] rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            className="h-full rounded-full"
            style={{ background: color }}
          />
        </div>
      )}
    </div>
  )
}

// ── Code block ────────────────────────────────────────────────────────────────
function CodeBlock({ content, placeholder }: { content: string; placeholder: string }) {
  const [copied, setCopied] = useState(false)
  const copy = useCallback(async () => {
    if (!content) return
    await navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }, [content])

  return (
    <div className="relative group">
      <button
        onClick={copy}
        className="absolute top-3 right-3 z-10 px-2.5 py-1 text-xs rounded-lg bg-white/[0.06] hover:bg-white/[0.12] text-slate-400 hover:text-white border border-white/[0.08] transition-all opacity-0 group-hover:opacity-100"
      >
        {copied ? '✓ Copied' : 'Copy'}
      </button>
      <pre className="bg-[#0d1117] rounded-xl border border-white/[0.07] p-4 text-sm font-mono text-slate-300 overflow-auto max-h-[480px] leading-6 whitespace-pre-wrap">
        {content || <span className="text-slate-600 italic">{placeholder}</span>}
      </pre>
    </div>
  )
}

// ── Palette strip ─────────────────────────────────────────────────────────────
function PaletteStrip({ colors }: { colors: Array<{ hex: string; type: string }> }) {
  if (!colors.length) return null
  return (
    <div className="flex flex-wrap gap-2 mb-4">
      {colors.map((c) => (
        <div
          key={c.hex}
          title={`${c.hex} (${c.type})`}
          className="flex items-center gap-2 px-2.5 py-1.5 glass rounded-lg border border-white/[0.06] cursor-pointer hover:border-white/[0.14] transition-colors"
          onClick={() => navigator.clipboard.writeText(c.hex)}
        >
          <span className="w-4 h-4 rounded-md border border-white/20 flex-shrink-0" style={{ background: c.hex }} />
          <span className="text-xs font-mono text-slate-400">{c.hex}</span>
        </div>
      ))}
    </div>
  )
}

// ── Code file viewer ──────────────────────────────────────────────────────────
function FileViewer({ files }: { files: Record<string, string> }) {
  const keys = Object.keys(files)
  const [active, setActive] = useState(keys[0] || '')
  const [copied, setCopied] = useState(false)

  const copy = useCallback(async () => {
    const c = files[active]
    if (!c) return
    await navigator.clipboard.writeText(c)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }, [files, active])

  if (!keys.length) return <p className="text-slate-600 italic text-sm">No files generated yet.</p>

  return (
    <div className="flex flex-col gap-0 rounded-xl overflow-hidden border border-white/[0.08]">
      {/* Tab bar */}
      <div className="flex items-center gap-1 px-3 py-2 bg-[#0d1117] border-b border-white/[0.06] overflow-x-auto">
        {keys.map((k) => (
          <button
            key={k}
            onClick={() => setActive(k)}
            className={`px-3 py-1.5 text-[11px] font-mono rounded-md whitespace-nowrap transition-colors ${
              active === k
                ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            {k}
          </button>
        ))}
        <div className="flex-1" />
        <button
          onClick={copy}
          className="px-2.5 py-1 text-[11px] rounded-md bg-white/[0.06] hover:bg-white/[0.12] text-slate-400 hover:text-white border border-white/[0.08] transition-all flex-shrink-0"
        >
          {copied ? '✓' : 'Copy'}
        </button>
      </div>
      {/* Code */}
      <pre className="bg-[#0a0d13] text-slate-300 font-mono text-xs leading-6 p-4 overflow-auto max-h-[520px] whitespace-pre">
        {files[active] || ''}
      </pre>
    </div>
  )
}

// ── Tab definitions ───────────────────────────────────────────────────────────
const TABS = [
  { id: 'hierarchy', label: 'Hierarchy' },
  { id: 'design', label: 'Design System' },
  { id: 'layout', label: 'Layout' },
  { id: 'code', label: 'Code' },
  { id: 'raw', label: 'JSON' },
]

const METRIC_CONFIG = [
  { key: 'component_detection_accuracy', label: 'Components', color: '#6366f1' },
  { key: 'ocr_accuracy', label: 'OCR', color: '#8b5cf6' },
  { key: 'layout_reconstruction_accuracy', label: 'Layout', color: '#06b6d4' },
  { key: 'visual_similarity_score', label: 'Visual', color: '#10b981' },
  { key: 'code_quality_score', label: 'Code', color: '#f59e0b' },
  { key: 'overall_score', label: 'Overall', color: '#ec4899' },
]

// ── Main studio page ──────────────────────────────────────────────────────────
export default function StudioPage({ params }: { params: Promise<{ filename: string }> }) {
  const { filename } = use(params)
  const decodedFilename = decodeURIComponent(filename)

  const [framework, setFramework] = useState('nextjs')
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [status, setStatus] = useState('Ready to analyze')
  const [activeTab, setActiveTab] = useState('hierarchy')
  const [stagePill, setStagePill] = useState<'idle' | 'running' | 'complete' | 'error'>('idle')

  const isValidFilename = decodedFilename && !decodedFilename.includes('{')

  const handleAnalyze = useCallback(async () => {
    if (!isValidFilename || loading) return
    setLoading(true)
    setError(null)
    setStagePill('running')
    setStatus('Running visual understanding, OCR, layout analysis, reasoning, and code generation…')
    try {
      const data = await analyzeImage(decodedFilename, framework)
      setResult(data)
      setStagePill('complete')
      setStatus(`Complete · ${data.visual_understanding.component_count} components · ${data.ocr_semantics.text_elements.length} text blocks`)
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Analysis failed'
      setError(msg)
      setStatus(msg)
      setStagePill('error')
    } finally {
      setLoading(false)
    }
  }, [isValidFilename, loading, decodedFilename, framework])

  // Show warning if opened without server
  useEffect(() => {
    if (!isValidFilename) {
      setStatus('Open via http://127.0.0.1:5000 to load screenshots and run analysis.')
      setStagePill('error')
    }
  }, [isValidFilename])

  const pillStyle = {
    idle: 'text-slate-400 bg-white/[0.04] border-white/[0.08]',
    running: 'text-amber-300 bg-amber-500/10 border-amber-500/30',
    complete: 'text-emerald-300 bg-emerald-500/10 border-emerald-500/30',
    error: 'text-red-300 bg-red-500/10 border-red-500/30',
  }

  return (
    <div className="min-h-screen bg-[#09090b] flex flex-col">
      {/* Top bar */}
      <header className="h-14 flex items-center justify-between px-5 border-b border-white/[0.06] bg-[#09090b]/80 backdrop-blur-xl sticky top-0 z-30">
        <Link href="/" className="flex items-center gap-2 font-bold text-white hover:opacity-80 transition-opacity">
          <Logo />
          <span className="text-[15px]">ui2code</span>
          <span className="text-slate-600">/</span>
          <span className="text-slate-400 font-normal text-sm truncate max-w-[200px]">{decodedFilename}</span>
        </Link>
        <div className="flex items-center gap-2">
          <Link href="/" className="px-3 py-1.5 text-sm text-slate-400 hover:text-white border border-white/[0.08] hover:border-white/[0.16] rounded-lg transition-all">
            ← New upload
          </Link>
        </div>
      </header>

      {/* Main split */}
      <div className="flex-1 flex overflow-hidden" style={{ height: 'calc(100vh - 56px)' }}>

        {/* LEFT PANE */}
        <aside className="w-[360px] lg:w-[400px] flex-shrink-0 flex flex-col border-r border-white/[0.06] overflow-y-auto bg-[#0c0c0e]">
          {/* Screenshot */}
          <div className="p-4 border-b border-white/[0.06]">
            <div className="flex items-center justify-between mb-3">
              <div>
                <p className="text-[10px] font-semibold text-indigo-400 tracking-widest uppercase mb-0.5">Source screenshot</p>
                <h2 className="text-base font-bold text-white">Visual input</h2>
              </div>
              <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${pillStyle[stagePill]}`}>
                <span className={`w-1.5 h-1.5 rounded-full ${stagePill === 'running' ? 'animate-pulse bg-amber-400' : stagePill === 'complete' ? 'bg-emerald-400' : stagePill === 'error' ? 'bg-red-400' : 'bg-slate-500'}`} />
                {stagePill === 'idle' ? 'Idle' : stagePill === 'running' ? 'Analyzing' : stagePill === 'complete' ? 'Complete' : 'Error'}
              </div>
            </div>

            {isValidFilename ? (
              <div className="rounded-xl overflow-hidden border border-white/[0.08] bg-black">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={imageUrl(decodedFilename)}
                  alt="Uploaded UI screenshot"
                  className="w-full object-contain max-h-[280px]"
                />
              </div>
            ) : (
              <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-400">
                Open via the Flask server to load screenshots.
              </div>
            )}
          </div>

          {/* Controls */}
          <div className="p-4 space-y-3 border-b border-white/[0.06]">
            <div>
              <label htmlFor="frameworkSelect" className="block text-xs text-slate-500 font-medium mb-1.5">
                Output framework
              </label>
              <select
                id="frameworkSelect"
                value={framework}
                onChange={(e) => setFramework(e.target.value)}
                disabled={loading}
                className="w-full bg-white/[0.04] border border-white/[0.1] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500/50 disabled:opacity-50"
              >
                <option value="nextjs">Next.js + Tailwind</option>
                <option value="react">React + Tailwind</option>
                <option value="html">HTML / CSS / JS</option>
              </select>
            </div>

            <motion.button
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleAnalyze}
              disabled={!isValidFilename || loading}
              className="w-full flex items-center justify-center gap-2.5 py-3 rounded-xl font-bold text-white text-sm bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 transition-all duration-200 shadow-[0_0_20px_rgba(99,102,241,0.35)] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                    <path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10" strokeLinecap="round" />
                  </svg>
                  Analyzing…
                </>
              ) : (
                <>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <circle cx="12" cy="12" r="3" /><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83" />
                  </svg>
                  Analyze Screenshot
                </>
              )}
            </motion.button>

            <a
              href={downloadUrl(decodedFilename, framework)}
              download
              className="w-full flex items-center justify-center gap-2.5 py-3 rounded-xl font-bold text-white text-sm bg-white/[0.06] hover:bg-white/[0.1] border border-white/[0.1] hover:border-white/[0.18] transition-all duration-200"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              Download ZIP
            </a>
          </div>

          {/* Status bar */}
          <div className="p-4">
            <p className="text-xs text-slate-500 leading-relaxed" role="status" aria-live="polite">{status}</p>
            <AnimatePresence>
              {error && (
                <motion.p
                  initial={{ opacity: 0, y: -6 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="mt-2 text-xs text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2"
                  role="alert"
                >
                  {error}
                </motion.p>
              )}
            </AnimatePresence>
          </div>
        </aside>

        {/* RIGHT PANE */}
        <section className="flex-1 min-w-0 flex flex-col overflow-hidden">
          {/* Inspector header */}
          <div className="px-6 pt-6 pb-4 border-b border-white/[0.06] bg-[#0c0c0e]">
            <p className="text-[10px] font-semibold text-indigo-400 tracking-widest uppercase mb-1">Intermediate Representation</p>
            <h1 className="text-2xl font-black text-white tracking-tight">Reasoned UI system</h1>
          </div>

          {/* Metrics row */}
          <div className="px-6 py-4 border-b border-white/[0.06] bg-[#0c0c0e]">
            <div className="grid grid-cols-3 lg:grid-cols-6 gap-3">
              {METRIC_CONFIG.map((m) => (
                <MetricCard
                  key={m.key}
                  label={m.label}
                  value={result?.evaluation?.[m.key as keyof typeof result.evaluation] as number | null ?? null}
                  color={m.color}
                />
              ))}
            </div>
          </div>

          {/* Tabs */}
          <div className="flex items-center gap-1 px-6 py-3 border-b border-white/[0.06] bg-[#0c0c0e] overflow-x-auto">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 text-sm font-medium rounded-lg whitespace-nowrap transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'text-white bg-indigo-500/20 border border-indigo-500/30'
                    : 'text-slate-500 hover:text-white border border-transparent hover:bg-white/[0.05]'
                }`}
                role="tab"
                aria-selected={activeTab === tab.id}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Panel content */}
          <div className="flex-1 overflow-y-auto p-6 bg-[#09090b]">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2 }}
              >
                {activeTab === 'hierarchy' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-white font-bold text-lg">Component Hierarchy</h2>
                      <p className="text-slate-500 text-sm">Semantic page tree inferred from layout and component positions</p>
                    </div>
                    <CodeBlock
                      content={result ? JSON.stringify(result.component_hierarchy, null, 2) : ''}
                      placeholder="Run analysis to see inferred component tree."
                    />
                  </div>
                )}

                {activeTab === 'design' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-white font-bold text-lg">Design System</h2>
                      <p className="text-slate-500 text-sm">Extracted colors, typography, spacing, radii, and shadows</p>
                    </div>
                    {result && <PaletteStrip colors={result.design_system.colors.all_colors || []} />}
                    <CodeBlock
                      content={result ? JSON.stringify(result.design_system, null, 2) : ''}
                      placeholder="Run analysis to extract design tokens."
                    />
                  </div>
                )}

                {activeTab === 'layout' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-white font-bold text-lg">Layout Intelligence</h2>
                      <p className="text-slate-500 text-sm">Rows, grids, alignment patterns, and spacing analysis</p>
                    </div>
                    <CodeBlock
                      content={result ? JSON.stringify(result.layout_intelligence, null, 2) : ''}
                      placeholder="Run analysis to inspect layout reasoning."
                    />
                  </div>
                )}

                {activeTab === 'code' && (
                  <div>
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h2 className="text-white font-bold text-lg">Generated Project</h2>
                        <p className="text-slate-500 text-sm">
                          {result ? `${result.generated_project.framework} · ${result.generated_project.styling}` : 'Next.js, React, and HTML/CSS/JS output files'}
                        </p>
                      </div>
                      {result && (
                        <span className="text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-full">
                          {Object.keys(result.generated_project.files).length} files
                        </span>
                      )}
                    </div>
                    {result ? (
                      <FileViewer files={result.generated_project.files} />
                    ) : (
                      <CodeBlock content="" placeholder="Generated files will appear here after analysis." />
                    )}
                  </div>
                )}

                {activeTab === 'raw' && (
                  <div>
                    <div className="mb-4">
                      <h2 className="text-white font-bold text-lg">Full JSON</h2>
                      <p className="text-slate-500 text-sm">Complete screenshot-to-code analysis payload</p>
                    </div>
                    <CodeBlock
                      content={result ? JSON.stringify(result, null, 2) : ''}
                      placeholder="Run analysis to view the complete intermediate representation."
                    />
                  </div>
                )}
              </motion.div>
            </AnimatePresence>
          </div>
        </section>
      </div>
    </div>
  )
}
