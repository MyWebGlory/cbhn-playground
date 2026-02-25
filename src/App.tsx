import { Routes, Route } from 'react-router-dom'
import Home from '@/pages/Home'
import StaticProject from '@/pages/StaticProject'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/projects/:slug" element={<StaticProject />} />
    </Routes>
  )
}
