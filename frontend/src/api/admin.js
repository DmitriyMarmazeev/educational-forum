import apiClient from './client';

export const adminApi = {
	listAllUsers() {
		return apiClient.get('/admin/users');
	},

	changeUserRole(userId, roleName) {
		return apiClient.patch(`/admin/users/${userId}/role`, {
			role_name: roleName,
		});
	},
};
