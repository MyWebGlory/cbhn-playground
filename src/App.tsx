
import { Routes, Route } from 'react-router-dom'
import Home from '@/pages/Home'
import StaticProject from '@/pages/StaticProject'
import { RestoreRedirect } from '@/components/RestoreRedirect'

export default function App() {
  return (
    <>
      <RestoreRedirect />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/projects/:slug" element={<StaticProject />} />
      </Routes>
    </>
  )
}
