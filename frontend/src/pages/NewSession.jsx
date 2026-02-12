import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createSession } from '../services/api';
import { format } from 'date-fns';

export default function NewSession() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    session_date: format(new Date(), 'yyyy-MM-dd'),
    duration: 90,
    difficulty: '6a',
    location: '',
    session_type: 'salle',
    notes: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const session = await createSession({
        ...formData,
        duration: parseInt(formData.duration),
      });
      navigate(`/sessions/${session.id}`);
    } catch (error) {
      console.error('Failed to create session:', error);
      alert('Erreur lors de la création de la session');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Nouvelle Session</h1>

      <form onSubmit={handleSubmit} className="card space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Titre (optionnel)
          </label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="input-field"
            placeholder="Ma session d'escalade"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date *
            </label>
            <input
              type="date"
              name="session_date"
              value={formData.session_date}
              onChange={handleChange}
              className="input-field"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Durée (minutes) *
            </label>
            <input
              type="number"
              name="duration"
              value={formData.duration}
              onChange={handleChange}
              className="input-field"
              min="1"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulté *
            </label>
            <select
              name="difficulty"
              value={formData.difficulty}
              onChange={handleChange}
              className="input-field"
              required
            >
              <option value="5a">5a</option>
              <option value="5b">5b</option>
              <option value="5c">5c</option>
              <option value="6a">6a</option>
              <option value="6b">6b</option>
              <option value="6c">6c</option>
              <option value="7a">7a</option>
              <option value="7b">7b</option>
              <option value="7c">7c</option>
              <option value="8a">8a</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Type *
            </label>
            <select
              name="session_type"
              value={formData.session_type}
              onChange={handleChange}
              className="input-field"
              required
            >
              <option value="salle">Salle</option>
              <option value="falaise">Falaise</option>
              <option value="bloc">Bloc</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Lieu
          </label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className="input-field"
            placeholder="Salle d'escalade de Mulhouse"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Notes
          </label>
          <textarea
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            className="input-field"
            rows="4"
            placeholder="Notes sur la session..."
          />
        </div>

        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex-1 disabled:opacity-50"
          >
            {loading ? 'Création...' : 'Créer la session'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/sessions')}
            className="btn-secondary"
          >
            Annuler
          </button>
        </div>
      </form>
    </div>
  );
}