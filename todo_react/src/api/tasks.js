import axiosInstance from './axiosInstance';

const tasksAPI = {
    getTasks: async (params = {}) => {
        const response = await axiosInstance.get('/tasks/', { params });
        return response.data;
    },

    getTask: async (id) => {
        const response = await axiosInstance.get(`/tasks/${id}/`);
        return response.data;
    },

    createTask: async (taskData) => {
        const response = await axiosInstance.post('/tasks/', taskData);
        return response.data;
    },

    updateTask: async (id, taskData) => {
        const response = await axiosInstance.patch(`/tasks/${id}/`, taskData);
        return response.data;
    },

    deleteTask: async (id) => {
        const response = await axiosInstance.delete(`/tasks/${id}/`);
        return response.data;
    },

    toggleComplete: async (id) => {
        const response = await axiosInstance.post(`/tasks/${id}/complete/`);
        return response.data;
    },
};

export default tasksAPI;