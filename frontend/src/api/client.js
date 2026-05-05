import axios from 'axios';

const apiClient = axios.create({
	baseURL: '/api',
	timeout: 30000,
});

apiClient.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem('access_token');
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error) => Promise.reject(error),
);

apiClient.interceptors.response.use(
	(response) => response,
	(error) => {
		if (error.response?.status === 401) {
			localStorage.removeItem('access_token');
			if (
				window.location.pathname !== '/login' &&
				window.location.pathname !== '/register'
			) {
				window.location.href = '/login';
			}
		}
		return Promise.reject(error);
	},
);

export default apiClient;
