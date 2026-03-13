import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import tasksAPI from '../api/tasks';

function TaskListPage() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all'); // all, pending, in_progress, completed
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Get user from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    } else {
      navigate('/login');
      return;
    }

    // Fetch tasks
    fetchTasks();
  }, [navigate]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await tasksAPI.getTasks();
      setTasks(response.tasks || []);
      setError('');
    } catch (err) {
      setError('Failed to load tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await tasksAPI.deleteTask(taskId);
      // Remove from local state
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      alert('Failed to delete task');
      console.error(err);
    }
  };

  const handleToggleComplete = async (taskId) => {
    try {
      const response = await tasksAPI.toggleComplete(taskId);
      // Update task in local state
      setTasks(tasks.map(task => 
        task.id === taskId ? response.task : task
      ));
    } catch (err) {
      alert('Failed to update task');
      console.error(err);
    }
  };

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    return task.status === filter;
  });

  // Get status badge color
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'pending':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Get priority badge color
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-orange-100 text-orange-800';
      case 'low':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">My Tasks</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-700">Hello, {user.first_name}!</span>
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            >
              Dashboard
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
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header with Create Button */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-gray-800">All Tasks</h2>
          <button
            onClick={() => navigate('/tasks/create')}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 font-semibold"
          >
            + Create Task
          </button>
        </div>

        {/* Filter Buttons */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded ${
              filter === 'all'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            All ({tasks.length})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-4 py-2 rounded ${
              filter === 'pending'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Pending ({tasks.filter(t => t.status === 'pending').length})
          </button>
          <button
            onClick={() => setFilter('in_progress')}
            className={`px-4 py-2 rounded ${
              filter === 'in_progress'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            In Progress ({tasks.filter(t => t.status === 'in_progress').length})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded ${
              filter === 'completed'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Completed ({tasks.filter(t => t.status === 'completed').length})
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="text-center py-12">
            <div className="text-gray-600 text-lg">Loading tasks...</div>
          </div>
        ) : filteredTasks.length === 0 ? (
          /* Empty State */
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-gray-400 text-6xl mb-4">📝</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              No tasks found
            </h3>
            <p className="text-gray-600 mb-6">
              {filter === 'all'
                ? 'Create your first task to get started!'
                : `No ${filter.replace('_', ' ')} tasks`}
            </p>
            <button
              onClick={() => navigate('/tasks/create')}
              className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600"
            >
              Create Task
            </button>
          </div>
        ) : (
          /* Task List */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredTasks.map((task) => (
              <div
                key={task.id}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
              >
                {/* Task Title */}
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  {task.title}
                </h3>

                {/* Task Description */}
                {task.description && (
                  <p className="text-gray-600 mb-4 line-clamp-2">
                    {task.description}
                  </p>
                )}

                {/* Status and Priority Badges */}
                <div className="flex gap-2 mb-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(
                      task.status
                    )}`}
                  >
                    {task.status.replace('_', ' ')}
                  </span>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${getPriorityColor(
                      task.priority
                    )}`}
                  >
                    {task.priority}
                  </span>
                </div>

                {/* Due Date */}
                {task.due_date && (
                  <p className="text-sm text-gray-600 mb-4">
                    📅 Due: {new Date(task.due_date).toLocaleDateString()}
                    {task.is_overdue && (
                      <span className="text-red-600 font-semibold ml-2">
                        (Overdue!)
                      </span>
                    )}
                  </p>
                )}

                {/* Action Buttons */}
                <div className="flex gap-2">
                  <button
                    onClick={() => navigate(`/tasks/edit/${task.id}`)}
                    className="flex-1 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 font-semibold"
                  >
                    ✏️ Edit
                  </button>
                  <button
                    onClick={() => handleToggleComplete(task.id)}
                    className={`flex-1 px-4 py-2 rounded font-semibold ${
                      task.status === 'completed'
                        ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        : 'bg-green-500 text-white hover:bg-green-600'
                    }`}
                  >
                    {task.status === 'completed' ? '↩️' : '✓'}
                  </button>
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 font-semibold"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default TaskListPage;