import apiClient from './client';

export const moderatorApi = {
	getTasksForModeration(params) {
		return apiClient.get('/moderator/tasks', { params });
	},

	changeTaskStatus(taskId, newStatus) {
		return apiClient.patch(`/moderator/tasks/${taskId}/status`, null, {
			params: { new_status: newStatus },
		});
	},

	deleteTaskByModerator(taskId) {
		return apiClient.delete(`/moderator/tasks/${taskId}`);
	},

	getCommentsForModeration(params) {
		return apiClient.get('/moderator/comments', { params });
	},

	deleteCommentByModerator(commentId) {
		return apiClient.delete(`/moderator/comments/${commentId}`);
	},
};
