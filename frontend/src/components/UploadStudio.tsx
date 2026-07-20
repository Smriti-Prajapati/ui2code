'use client'

import { useState, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { uploadImage } from '@/lib/api'

const PIPELINE_STEPS = [
  { label: 'Screenshot loaded', icon: '📸' },
  { label: 'OCR text extraction', icon: '🔤' },
  { label: 'Component detection', icon: '🧩' },
  { label: 'Layout intelligence', icon: '📐' },
  { label: 'Code generation', icon: '⚡' },
  { label: 'Project ready', icon: '✅' },
]

export default function UploadStudio() {
  const router = useRouter()
  const inputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [activeStep, setActiveStep] = useState(-1)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('Supports PNG, JPG, JPEG, and WEBP · Max 10MB')
  const [error, setError] = useState<string | null>(null)

  const handleFile = useCallback((f: File | null) => {
    if (!f) return
    if (!f.type.startsWith('image/')) {
      setError('Please select a valid image file.')
      return
    }
    if (f.size > 10 * 1024 * 1024) {
      setError('File too large. Max 10MB.')
      return
    }
    setError(null)
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setStatus(`${f.name} — ready to generate`)
    setActiveStep(-1)
    setProgress(0)
  }, [])

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }, [handleFile])

  const runPipeline = () => new Promise<void>((resolve) => {
    const delays = [0, 280, 560, 840, 1120, 1400]
    const pcts = [16, 33, 50, 66, 82, 100]
    delays.forEach((d, i) => {
      setTimeout(() => {
        setActiveStep(i)
        setProgress(pcts[i])
        setStatus(`${PIPELINE_STEPS[i].label}…`)
        if (i === delays.length - 1) setTimeout(resolve, 300)
      }, d)
    })
  })

  const handleGenerate = async () => {
    if (!file) { setError('Please select a screenshot first.'); return }
    setError(null)
    setUploading(true)
    try {
      await runPipeline()
      const data = await uploadImage(file)
      // Extract filename from redirect_url like /editor/filename
      const filename = data.filename || data.redirect_url.split('/').pop() || ''
      router.push(`/studio/${encodeURIComponent(filename)}`)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Upload failed. Is the Flask server running?')
      setUploading(false)
      setActiveStep(-1)
      setProgress(0)
    }
  }

  return (
    <section id="studio" className="py-24 px-6 relative overflow-hidden">
      {/* bg glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-indigo-600/8 rounded-full blur-[100px] pointer-events-none" aria-hidden="true" />

      <div className="relative z-10 max-w-3xl mx-auto">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <span className="inline-flex items-center gap-2 px-3 py-1.5 mb-5 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 text-xs font-semibold tracking-wide uppercase">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            Interactive Studio
          </span>
          <h2 className="text-4xl lg:text-5xl font-black text-white tracking-[-0.03em] mb-4">
            Drop your screenshot.<br />
            <span className="gradient-text">Get real frontend code.</span>
          </h2>
          <p className="text-slate-400 text-lg">
            Websites, dashboards, mobile apps, Figma frames, wireframes — anything works.
          </p>
        </motion.div>

        {/* Studio card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="glass-light rounded-3xl overflow-hidden shadow-2xl"
        >
          {/* Card header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-white/[0.06]">
            <div>
              <p className="text-xs font-semibold text-indigo-400 tracking-widest uppercase mb-0.5">Screenshot Input</p>
              <h3 className="text-lg font-bold text-white">Upload your UI</h3>
            </div>
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors duration-300 ${
              uploading
                ? 'text-amber-300 bg-amber-500/10 border-amber-500/30'
                : file
                ? 'text-emerald-300 bg-emerald-500/10 border-emerald-500/30'
                : 'text-slate-400 bg-white/[0.04] border-white/[0.08]'
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${uploading ? 'bg-amber-400 animate-pulse' : file ? 'bg-emerald-400' : 'bg-slate-500'}`} />
              {uploading ? 'Processing' : file ? 'Loaded' : 'Ready'}
            </div>
          </div>

          <div className="p-6 space-y-4">
            {/* Dropzone */}
            <div
              role="button"
              tabIndex={0}
              aria-label="Drop or click to upload UI screenshot"
              onClick={() => inputRef.current?.click()}
              onKeyDown={(e) => e.key === 'Enter' && inputRef.current?.click()}
              onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
              onDragLeave={() => setDragging(false)}
              onDrop={onDrop}
              className={`relative flex flex-col items-center justify-center gap-3 min-h-[200px] rounded-2xl border-2 border-dashed cursor-pointer transition-all duration-300 ${
                dragging
                  ? 'border-indigo-400 bg-indigo-500/10 scale-[1.01]'
                  : 'border-white/[0.12] hover:border-indigo-500/50 hover:bg-white/[0.03] bg-white/[0.02]'
              }`}
            >
              <input
                ref={inputRef}
                type="file"
                accept="image/png,image/jpeg,image/webp"
                className="sr-only"
                onChange={(e) => handleFile(e.target.files?.[0] || null)}
                aria-hidden="true"
              />

              <AnimatePresence mode="wait">
                {preview ? (
                  <motion.img
                    key="preview"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0 }}
                    src={preview}
                    alt="Preview of selected screenshot"
                    className="max-h-48 rounded-xl object-contain shadow-xl"
                  />
                ) : (
                  <motion.div
                    key="placeholder"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex flex-col items-center gap-3 select-none"
                  >
                    <div className="w-14 h-14 rounded-2xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center">
                      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#818cf8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                      </svg>
                    </div>
                    <div className="text-center">
                      <p className="font-semibold text-white">Drop a UI screenshot here</p>
                      <p className="text-sm text-slate-500 mt-1">or click to browse — PNG, JPG, WEBP</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Pipeline progress */}
            <AnimatePresence>
              {(uploading || activeStep >= 0) && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="overflow-hidden rounded-2xl bg-[#0d1117] border border-white/[0.08] p-4"
                >
                  {/* Progress bar */}
                  <div className="h-1.5 bg-white/[0.06] rounded-full overflow-hidden mb-4">
                    <motion.div
                      className="h-full rounded-full bg-gradient-to-r from-indigo-500 via-violet-500 to-purple-500"
                      animate={{ width: `${progress}%` }}
                      transition={{ duration: 0.4 }}
                    />
                  </div>
                  {/* Steps */}
                  <ol className="space-y-2">
                    {PIPELINE_STEPS.map((step, i) => (
                      <motion.li
                        key={step.label}
                        initial={{ opacity: 0.3 }}
                        animate={{ opacity: i <= activeStep ? 1 : 0.3 }}
                        className="flex items-center gap-3 text-sm"
                      >
                        <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] border transition-colors ${
                          i < activeStep
                            ? 'bg-emerald-500 border-emerald-400 text-white'
                            : i === activeStep
                            ? 'bg-indigo-500 border-indigo-400 text-white animate-pulse'
                            : 'bg-white/[0.04] border-white/[0.1] text-slate-600'
                        }`}>
                          {i < activeStep ? '✓' : i + 1}
                        </span>
                        <span className={i <= activeStep ? 'text-white font-medium' : 'text-slate-600'}>
                          {step.label}
                        </span>
                      </motion.li>
                    ))}
                  </ol>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Error */}
            <AnimatePresence>
              {error && (
                <motion.p
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center gap-2 text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3"
                  role="alert"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                  {error}
                </motion.p>
              )}
            </AnimatePresence>

            {/* Generate button */}
            <motion.button
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleGenerate}
              disabled={uploading}
              className="w-full flex items-center justify-center gap-3 py-4 rounded-2xl font-bold text-white bg-gradient-to-r from-indigo-600 via-violet-600 to-indigo-600 bg-[length:200%_100%] hover:bg-right transition-all duration-500 shadow-[0_0_30px_rgba(99,102,241,0.4)] hover:shadow-[0_0_50px_rgba(99,102,241,0.6)] disabled:opacity-60 disabled:cursor-wait"
            >
              {uploading ? (
                <>
                  <svg className="animate-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                    <path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10" strokeLinecap="round" />
                  </svg>
                  Analyzing screenshot…
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <polygon points="5 3 19 12 5 21 5 3" />
                  </svg>
                  Generate Code
                </>
              )}
            </motion.button>

            <p className="text-xs text-center text-slate-600" role="status" aria-live="polite">
              {status}
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
