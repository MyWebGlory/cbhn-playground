export interface Project {
  slug: string
  title: string
  description: string
  category: string
  color: string
}

export const projects: Project[] = [
  {
    slug: 'sponsorship-package',
    title: 'Sponsorship Package',
    description: 'Virtual Behavioral Health Conference — 9-page sponsorship deck with tiers, speakers, agenda, and commitment form.',
    category: 'Conference — May 2026',
    color: 'from-deep-blue to-shamrock',
  },
  {
    slug: 'registration-flyer',
    title: 'Registration Flyer',
    description: 'Single-page conference registration flyer with speaker lineup, event details, and QR code.',
    category: 'Conference — May 2026',
    color: 'from-molten-orange to-gold',
  },
  {
    slug: 'zoom-landing-page',
    title: 'Zoom Landing Page',
    description: '1920×1080 Zoom waiting room / landing page graphic for the conference.',
    category: 'Conference — May 2026',
    color: 'from-deep-blue to-molten-orange',
  },
]
