import apiClient from './client';

export const tasksApi = {
	getTasks(params) {
		return apiClient.get('/tasks/', { params });
	},

	getTask(taskId) {
		return apiClient.get(`/tasks/${taskId}`);
	},

	createTask(data) {
		return apiClient.post('/tasks/', data);
	},

	updateTask(taskId, data) {
		return apiClient.put(`/tasks/${taskId}`, data);
	},

	deleteTask(taskId) {
		return apiClient.delete(`/tasks/${taskId}`);
	},

	getSolution(taskId) {
		return apiClient.get(`/tasks/${taskId}/solution`);
	},

	rateTask(taskId, rating) {
		return apiClient.post(`/tasks/${taskId}/rate`, { rating });
	},

	getComments(taskId) {
		return apiClient.get(`/tasks/${taskId}/comments/`);
	},

	addComment(taskId, comment) {
		return apiClient.post(`/tasks/${taskId}/comments/`, { comment });
	},
};
