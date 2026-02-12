// SessionDetail.jsx
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSession } from '../services/api';

export default function SessionDetail() {
  const { id } = useParams();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSession();
  }, [id]);

  const loadSession = async () => {
    try {
      const data = await getSession(id);
      setSession(data);
    } catch (error) {
      console.error('Failed to load session:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Chargement...</div>;
  }

  if (!session) {
    return <div className="text-center py-8">Session non trouvée</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">{session.title || 'Session'}</h1>
      <div className="card">
        <p>Détails de la session #{id}</p>
        <pre className="mt-4 text-sm">{JSON.stringify(session, null, 2)}</pre>
      </div>
    </div>
  );
}