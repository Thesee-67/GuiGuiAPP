import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getSessions } from '../services/api';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

export default function Sessions() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, week, month

  useEffect(() => {
    loadSessions();
  }, [filter]);

  const loadSessions = async () => {
    try {
      const data = await getSessions();
      setSessions(data);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      '5a': 'bg-green-100 text-green-800',
      '5b': 'bg-green-100 text-green-800',
      '5c': 'bg-yellow-100 text-yellow-800',
      '6a': 'bg-yellow-100 text-yellow-800',
      '6b': 'bg-orange-100 text-orange-800',
      '6c': 'bg-orange-100 text-orange-800',
      '7a': 'bg-red-100 text-red-800',
      '7b': 'bg-red-100 text-red-800',
      '7c': 'bg-purple-100 text-purple-800',
    };
    return colors[difficulty] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-bold text-gray-800">Mes Sessions</h1>
        <Link to="/sessions/new" className="btn-primary">
          + Nouvelle session
        </Link>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            Toutes
          </button>
          <button
            onClick={() => setFilter('week')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'week'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            Cette semaine
          </button>
          <button
            onClick={() => setFilter('month')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === 'month'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            Ce mois
          </button>
        </div>
      </div>

      {/* Sessions List */}
      {sessions.length === 0 ? (
        <div className="card text-center py-12">
          <div className="text-6xl mb-4">🧗</div>
          <p className="text-gray-500 text-lg mb-4">Aucune session enregistrée</p>
          <Link to="/sessions/new" className="btn-primary">
            Créer votre première session
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sessions.map((session) => (
            <Link
              key={session.id}
              to={`/sessions/${session.id}`}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
            >
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-bold text-lg text-gray-800">
                  {session.title || 'Session d\'escalade'}
                </h3>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(session.difficulty)}`}>
                  {session.difficulty}
                </span>
              </div>

              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center">
                  <span className="mr-2">📅</span>
                  {format(new Date(session.session_date), 'dd MMMM yyyy', { locale: fr })}
                </div>
                <div className="flex items-center">
                  <span className="mr-2">⏱️</span>
                  {session.duration} minutes
                </div>
                <div className="flex items-center">
                  <span className="mr-2">🏔️</span>
                  {session.location || 'Salle d\'escalade'}
                </div>
              </div>

              {session.notes && (
                <p className="mt-4 text-sm text-gray-500 line-clamp-2">
                  {session.notes}
                </p>
              )}

              <div className="mt-4 flex justify-between items-center text-xs text-gray-500">
                <span>{session.exercises_count || 0} exercices</span>
                <span className="text-blue-600 font-medium">Voir détails →</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}