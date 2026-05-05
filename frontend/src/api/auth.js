// frontend/src/api/auth.js
import apiClient from './client';

export const authApi = {
	register(data) {
		return apiClient.post('/auth/register', data);
	},

	login(data) {
		return apiClient.post('/auth/login', data);
	},

	getMe() {
		return apiClient.get('/users/me');
	},

	updateMe(data) {
		return apiClient.put('/users/me', data);
	},

	deleteMe() {
		return apiClient.delete('/users/me');
	},

	getUserProfile(userId) {
		return apiClient.get(`/users/${userId}`);
	},

	applyForAuthor() {
		return apiClient.post('/users/apply-author');
	},

	subscribe() {
		return apiClient.post('/users/subscribe');
	},
};
