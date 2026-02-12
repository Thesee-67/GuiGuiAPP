import { useAuth } from '../context/AuthContext';

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Mon Profil</h1>

      <div className="card">
        <div className="flex items-center space-x-4 mb-6">
          <div className="w-20 h-20 bg-blue-600 text-white rounded-full flex items-center justify-center text-3xl font-bold">
            {user?.username?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">{user?.username}</h2>
            <p className="text-gray-600">{user?.email}</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nom d'utilisateur
            </label>
            <input
              type="text"
              value={user?.username || ''}
              className="input-field"
              disabled
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              value={user?.email || ''}
              className="input-field"
              disabled
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Membre depuis
            </label>
            <input
              type="text"
              value={user?.created_at ? new Date(user.created_at).toLocaleDateString('fr-FR') : ''}
              className="input-field"
              disabled
            />
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            Modification du profil disponible prochainement
          </p>
        </div>
      </div>
    </div>
  );
}