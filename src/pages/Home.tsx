import { Link } from 'react-router-dom'
import { ExternalLink, Folder } from 'lucide-react'
import { projects } from '@/lib/projects'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-charcoal via-gray-900 to-charcoal">
      {/* Header */}
      <header className="border-b border-white/10 px-8 py-6">
        <div className="max-w-5xl mx-auto flex items-center gap-4">
          <img src={`${import.meta.env.BASE_URL}images/cbhn-logo.png`} alt="CBHN" className="h-10 w-auto" />
          <div>
            <h1 className="text-white text-xl font-bold tracking-tight">CBHN Playground</h1>
            <p className="text-white/50 text-sm">Project workspace, California Black Health Network</p>
          </div>
        </div>
      </header>

      {/* Projects Grid */}
      <main className="max-w-5xl mx-auto px-8 py-12">
        <div className="flex items-center gap-2 mb-8">
          <Folder className="w-5 h-5 text-white/40" />
          <h2 className="text-white/60 text-sm font-semibold uppercase tracking-wider">Projects</h2>
          <span className="ml-2 px-2 py-0.5 bg-white/10 text-white/50 text-xs rounded-full">{projects.length}</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.slug}
              className="group relative bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-2xl p-6 transition-all duration-300"
            >
              {/* Color accent bar */}
              <div className={`absolute top-0 left-6 right-6 h-0.5 bg-gradient-to-r ${project.color} rounded-b-full opacity-60 group-hover:opacity-100 transition-opacity`} />

              <span className="inline-block px-2.5 py-1 bg-white/10 text-white/60 text-[10px] font-semibold uppercase tracking-wider rounded-full mb-4">
                {project.category}
              </span>

              <h3 className="text-white font-bold text-lg mb-2">{project.title}</h3>
              <p className="text-white/50 text-sm leading-relaxed mb-6">{project.description}</p>

              <div className="flex gap-3">
                <Link
                  to={`/projects/${project.slug}`}
                  className="inline-flex items-center gap-1.5 px-4 py-2 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold rounded-lg transition-colors"
                >
                  Open in app
                </Link>
                <a
                  href={`/projects/${project.slug}/`}
                  target="_blank"
                  rel="noopener"
                  className="inline-flex items-center gap-1.5 px-4 py-2 text-white/50 hover:text-white text-xs font-semibold rounded-lg transition-colors"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  Raw HTML
                </a>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 px-8 py-6 mt-12">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <p className="text-white/30 text-xs">&copy; 2026 California Black Health Network</p>
          <a
            href="https://yourcbhn.org/"
            target="_blank"
            rel="noopener"
            className="text-white/30 hover:text-white/60 text-xs transition-colors"
          >
            yourcbhn.org
          </a>
        </div>
      </footer>
    </div>
  )
}
