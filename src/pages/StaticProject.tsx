import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, ExternalLink } from 'lucide-react'
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

  const standaloneUrl = `${import.meta.env.BASE_URL}projects/${slug}/index.html`

  return (
    <>
      <style>{`
        @media print {
          .project-toolbar { display: none !important; }
          .project-iframe {
            position: fixed !important;
            inset: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            min-height: 100vh !important;
            border: none !important;
          }
        }
      `}</style>
      <div className="min-h-screen bg-charcoal flex flex-col">
        {/* Minimal toolbar */}
        <div className="project-toolbar flex items-center gap-3 px-4 py-2 bg-black/40 border-b border-white/10">
          <Link
            to="/"
            className="inline-flex items-center gap-1.5 text-white/60 hover:text-white text-xs font-medium transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Projects
          </Link>
          <span className="text-white/20">|</span>
          <span className="text-white/80 text-xs font-semibold">{project.title}</span>
          <div className="ml-auto">
            <a
              href={standaloneUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-white/50 hover:text-white text-xs font-medium transition-colors border border-white/10 hover:border-white/30 rounded px-2 py-1"
              title="Open standalone for clean PDF export"
            >
              <ExternalLink className="w-3 h-3" />
              Open for print
            </a>
          </div>
        </div>

        {/* Full-page iframe */}
        <iframe
          src={standaloneUrl}
          title={project.title}
          className="project-iframe flex-1 w-full border-none"
          style={{ minHeight: 'calc(100vh - 40px)' }}
        />
      </div>
    </>
  )
}
