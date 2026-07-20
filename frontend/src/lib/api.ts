const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000'

export interface AnalysisResult {
  image: { filename: string; width: number; height: number }
  visual_understanding: {
    components: Array<{ type: string; bbox: object; confidence: number }>
    component_count: number
    component_types: string[]
  }
  ocr_semantics: {
    text_elements: Array<{ text: string; type: string; confidence: number }>
    semantic_structure: object
  }
  layout_intelligence: object
  design_system: {
    colors: {
      primary: string
      secondary: string
      accent: string
      background: string
      text: string
      all_colors: Array<{ rgb: number[]; hex: string; type: string }>
    }
    typography: object
    spacing: object
    border_radius: object
    shadows: object
    design_tokens: object
  }
  component_hierarchy: object
  generated_project: {
    framework: string
    styling: string
    files: Record<string, string>
  }
  evaluation: {
    component_detection_accuracy: number
    ocr_accuracy: number
    layout_reconstruction_accuracy: number
    visual_similarity_score: number
    code_quality_score: number
    overall_score: number
    notes: string[]
  }
}

export async function uploadImage(file: File): Promise<{ redirect_url: string; filename: string }> {
  const formData = new FormData()
  formData.append('image', file)
  const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Upload failed' }))
    throw new Error(err.error || 'Upload failed')
  }
  return res.json()
}

export async function analyzeImage(
  filename: string,
  framework = 'nextjs',
  styling = 'tailwind'
): Promise<AnalysisResult> {
  const url = `${API_BASE}/api/analyze/${encodeURIComponent(filename)}?framework=${framework}&styling=${styling}`
  const res = await fetch(url)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Analysis failed' }))
    throw new Error(err.error || 'Analysis failed')
  }
  return res.json()
}

export function downloadUrl(filename: string, framework = 'nextjs') {
  return `${API_BASE}/download/${encodeURIComponent(filename)}?framework=${framework}`
}

export function imageUrl(filename: string) {
  return `${API_BASE}/uploads/${encodeURIComponent(filename)}`
}
