import type { Metadata } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'ui2code — Screenshot to Production Frontend Code',
  description:
    'Upload any UI screenshot. ui2code detects components, extracts text, understands layouts, and generates clean HTML, CSS, React, and Tailwind code automatically.',
  keywords: ['design to code', 'screenshot to code', 'UI to code', 'React generator', 'Tailwind generator'],
  authors: [{ name: 'Smriti Prajapati' }],
  openGraph: {
    title: 'ui2code — Screenshot to Frontend Code',
    description: 'AI-powered design-to-code platform. Upload a screenshot, get production-ready React & Tailwind.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className={`${inter.className} noise`}>
        {children}
      </body>
    </html>
  )
}
