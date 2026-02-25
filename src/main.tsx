import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

const getBaseName = () => {
  // Handles local, production, and GitHub Pages
  if (window.location.hostname === 'mywebglory.github.io') {
    return '/cbhn-playground';
  }
  return '/';
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter basename={getBaseName()}>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
