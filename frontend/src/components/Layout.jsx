import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const navLinks = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/sessions', label: 'Sessions', icon: '🧗' },
    { path: '/programs', label: 'Programmes', icon: '📋' },
    { path: '/goals', label: 'Objectifs', icon: '🎯' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-8">
              <Link to="/" className="text-2xl font-bold text-blue-600">
                🧗 Training App
              </Link>
              
              <nav className="hidden md:flex space-x-4">
                {navLinks.map((link) => (
                  <Link
                    key={link.path}
                    to={link.path}
                    className={`px-3 py-2 rounded-lg font-medium transition-colors ${
                      isActive(link.path)
                        ? 'bg-blue-50 text-blue-600'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <span className="mr-2">{link.icon}</span>
                    {link.label}
                  </Link>
                ))}
              </nav>
            </div>

            <div className="flex items-center space-x-4">
              <Link
                to="/profile"
                className="flex items-center space-x-2 text-gray-700 hover:text-blue-600"
              >
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                  {user?.username?.charAt(0).toUpperCase() || 'U'}
                </div>
                <span className="hidden sm:block font-medium">{user?.username}</span>
              </Link>
              
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-gray-700 hover:text-red-600 font-medium transition-colors"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <nav className="md:hidden border-t border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-2 flex justify-around">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`flex flex-col items-center py-2 px-3 rounded-lg ${
                  isActive(link.path)
                    ? 'text-blue-600'
                    : 'text-gray-600'
                }`}
              >
                <span className="text-2xl">{link.icon}</span>
                <span className="text-xs mt-1">{link.label}</span>
              </Link>
            ))}
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}