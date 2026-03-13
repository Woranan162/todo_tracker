import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import authAPI from '../api/auth';

function ProfilePage() {
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
  });
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);
  const navigate = useNavigate();

  // Fetch user profile on component load
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setFetchLoading(true);
        const response = await authAPI.getProfile();
        const userData = response.user;
        
        setUser(userData);
        setFormData({
          username: userData.username,
          email: userData.email || '',
          first_name: userData.first_name,
          last_name: userData.last_name,
        });
      } catch (err) {
        console.error('Failed to load profile:', err);
        // If unauthorized, redirect to login
        if (err.response?.status === 401) {
          navigate('/login');
        }
      } finally {
        setFetchLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleEdit = () => {
    setIsEditing(true);
    setError('');
    setSuccess('');
  };

  const handleCancel = () => {
    setIsEditing(false);
    // Reset form data to original user data
    setFormData({
      username: user.username,
      email: user.email || '',
      first_name: user.first_name,
      last_name: user.last_name,
    });
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await authAPI.updateProfile(formData);
      
      // Update local state
      setUser(response.user);
      
      // Update localStorage
      const currentUser = JSON.parse(localStorage.getItem('user'));
      const updatedUser = { ...currentUser, ...response.user };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      setSuccess('Profile updated successfully!');
      setIsEditing(false);
    } catch (err) {
      if (err.response?.data?.errors) {
        // Handle field-specific errors
        const errorMessages = Object.entries(err.response.data.errors)
          .map(([field, messages]) => {
            if (Array.isArray(messages)) {
              return `${field}: ${messages.join(', ')}`;
            }
            return `${field}: ${messages}`;
          })
          .join('\n');
        setError(errorMessages);
      } else {
        setError(err.response?.data?.message || 'Failed to update profile');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  if (fetchLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-gray-600 text-lg">Loading profile...</div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">My Profile</h1>
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            >
              Dashboard
            </button>
            <button
              onClick={() => navigate('/tasks')}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              My Tasks
            </button>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Profile Information</h2>
            {!isEditing && (
              <button
                onClick={handleEdit}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                ✏️ Edit Profile
              </button>
            )}
          </div>

          {/* Success Message */}
          {success && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              {success}
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 whitespace-pre-line">
              {error}
            </div>
          )}

          {/* Profile Form */}
          <form onSubmit={handleSubmit}>
            {/* Username */}
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Username
              </label>
              {isEditing ? (
                <div>
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                    required
                  />
                  {user.can_change_username ? (
                    <p className="text-green-600 text-xs mt-1">
                      ✓ You can change your username
                    </p>
                  ) : (
                    <p className="text-red-600 text-xs mt-1">
                      ⚠️ You can change your username in {user.days_until_username_change} day(s)
                    </p>
                  )}
                </div>
              ) : (
                <p className="text-gray-900 bg-gray-100 px-3 py-2 rounded">
                  {user.username}
                </p>
              )}
            </div>

            {/* Email */}
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Email
              </label>
              {isEditing ? (
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                />
              ) : (
                <p className="text-gray-900 bg-gray-100 px-3 py-2 rounded">
                  {user.email || 'Not provided'}
                </p>
              )}
            </div>

            {/* First Name */}
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                First Name
              </label>
              {isEditing ? (
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                  required
                />
              ) : (
                <p className="text-gray-900 bg-gray-100 px-3 py-2 rounded">
                  {user.first_name}
                </p>
              )}
            </div>

            {/* Last Name */}
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Last Name
              </label>
              {isEditing ? (
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                  required
                />
              ) : (
                <p className="text-gray-900 bg-gray-100 px-3 py-2 rounded">
                  {user.last_name}
                </p>
              )}
            </div>

            {/* Account Info (Read-only) */}
            <div className="border-t pt-4 mt-6">
              <h3 className="text-lg font-semibold mb-3">Account Information</h3>
              
              <div className="mb-3">
                <label className="block text-gray-600 text-sm mb-1">
                  Full Name
                </label>
                <p className="text-gray-900">{user.full_name}</p>
              </div>

              <div className="mb-3">
                <label className="block text-gray-600 text-sm mb-1">
                  Member Since
                </label>
                <p className="text-gray-900">
                  {new Date(user.date_joined).toLocaleDateString()}
                </p>
              </div>

              {user.last_login && (
                <div className="mb-3">
                  <label className="block text-gray-600 text-sm mb-1">
                    Last Login
                  </label>
                  <p className="text-gray-900">
                    {new Date(user.last_login).toLocaleString()}
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            {isEditing && (
              <div className="flex gap-4 mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 font-semibold"
                >
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 font-semibold"
                >
                  Cancel
                </button>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;