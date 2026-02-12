import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getStats, getSessions } from '../services/api';
import { format, subDays } from 'date-fns';
import { fr } from 'date-fns/locale';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [recentSessions, setRecentSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('7'); // 7, 30, 90 days

  useEffect(() => {
    loadData();
  }, [period]);

  const loadData = async () => {
    try {
      const endDate = format(new Date(), 'yyyy-MM-dd');
      const startDate = format(subDays(new Date(), parseInt(period)), 'yyyy-MM-dd');
      
      const [statsData, sessionsData] = await Promise.all([
        getStats(startDate, endDate),
        getSessions({ limit: 5 })
      ]);
      
      setStats(statsData);
      setRecentSessions(sessionsData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
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
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="7">7 derniers jours</option>
          <option value="30">30 derniers jours</option>
          <option value="90">90 derniers jours</option>
        </select>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Sessions totales</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">
                {stats?.total_sessions || 0}
              </p>
            </div>
            <div className="text-4xl">🧗</div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Temps total</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">
                {Math.round((stats?.total_duration || 0) / 60)}h
              </p>
            </div>
            <div className="text-4xl">⏱️</div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Niveau moyen</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">
                {stats?.avg_difficulty || '-'}
              </p>
            </div>
            <div className="text-4xl">📊</div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Progression</p>
              <p className="text-3xl font-bold text-green-600 mt-2">
                +{stats?.progress || 0}%
              </p>
            </div>
            <div className="text-4xl">📈</div>
          </div>
        </div>
      </div>

      {/* Recent Sessions */}
      <div className="card">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-800">Sessions récentes</h2>
          <Link to="/sessions/new" className="btn-primary">
            + Nouvelle session
          </Link>
        </div>

        {recentSessions.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg mb-4">Aucune session enregistrée</p>
            <Link to="/sessions/new" className="btn-primary">
              Créer votre première session
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {recentSessions.map((session) => (
              <Link
                key={session.id}
                to={`/sessions/${session.id}`}
                className="block p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition-all"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-800">{session.title || 'Session'}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {format(new Date(session.session_date), 'dd MMMM yyyy', { locale: fr })}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                      {session.difficulty}
                    </span>
                    <p className="text-sm text-gray-600 mt-2">
                      {session.duration} min
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {recentSessions.length > 0 && (
          <div className="mt-6 text-center">
            <Link to="/sessions" className="text-blue-600 hover:text-blue-700 font-medium">
              Voir toutes les sessions →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}