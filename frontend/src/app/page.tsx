import WebGLBackground from '@/components/WebGLBackground'
import Navbar from '@/components/Navbar'
import Hero from '@/components/Hero'
import UploadStudio from '@/components/UploadStudio'
import Pipeline from '@/components/Pipeline'
import Features from '@/components/Features'
import DemoSection from '@/components/DemoSection'
import Footer from '@/components/Footer'

export default function HomePage() {
  return (
    <>
      <WebGLBackground />
      <Navbar />
      <main>
        <Hero />
        <UploadStudio />
        <Pipeline />
        <Features />
        <DemoSection />
      </main>
      <Footer />
    </>
  )
}
