// If redirected from 404.html, use the ?redirect param to restore the intended route
// ...existing code...
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

export function RestoreRedirect() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const redirect = params.get('redirect');
    if (redirect) {
      navigate(redirect, { replace: true });
    }
  }, [location, navigate]);

  return null;
}
