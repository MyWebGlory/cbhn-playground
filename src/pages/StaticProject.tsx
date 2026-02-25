import { useParams, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { projects } from '@/lib/projects'

export default function StaticProject() {
  const { slug } = useParams<{ slug: string }>()
  const project = projects.find((p) => p.slug === slug)

  if (!project) {
    return (
      <div className="min-h-screen bg-charcoal flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-white text-2xl font-bold mb-4">Project not found</h1>
          <Link to="/" className="text-shamrock hover:underline">
            Back to projects
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-charcoal flex flex-col">
      {/* Minimal toolbar */}
      <div className="flex items-center gap-3 px-4 py-2 bg-black/40 border-b border-white/10">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-white/60 hover:text-white text-xs font-medium transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Projects
        </Link>
        <span className="text-white/20">|</span>
        <span className="text-white/80 text-xs font-semibold">{project.title}</span>
      </div>

      {/* Full-page iframe */}
      <iframe
        src={`/projects/${slug}/index.html`}
        title={project.title}
        className="flex-1 w-full border-none"
        style={{ minHeight: 'calc(100vh - 40px)' }}
      />
    </div>
  )
}
