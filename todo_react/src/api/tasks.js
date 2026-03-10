import axiosInstance from './axiosInstance';

const authAPI = {
    register: async (userData) => {
        const response = await axiosInstance.post('/auth/register/', userData);
        return response.data;
    },

    login: async (credentials) => {
        const response = await axiosInstance.post('/auth/login/', credentials);
        return response.data;
    },

    logout: async () => {
        const response = await axiosInstance.post('/auth/logout/');
        return response.data;
    },

    getProfile: async () => {
        const response = await axiosInstance.get('/auth/profile/');
        return response.data;
    },

    updateProfile: async (profileData) => {
        const response = await axiosInstance.patch('/auth/profile/', profileData);
        return response.data;
    },
};

export default authAPI;