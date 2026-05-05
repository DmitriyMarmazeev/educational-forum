// frontend/src/stores/auth.js (добавлен wallet и обновлены методы)
import { defineStore } from 'pinia';
import { authApi } from '../api';

export const useAuthStore = defineStore('auth', {
	state: () => ({
		user: null,
		token: localStorage.getItem('access_token'),
		loading: false,
	}),

	getters: {
		isAuthenticated: (state) => !!state.token,
		isAuthor: (state) => state.user?.role_name === 'author',
		isModerator: (state) => state.user?.role_name === 'moderator',
		isAdmin: (state) => state.user?.role_name === 'admin',
		// Добавляем геттер для обычного пользователя
		isRegularUser: (state) => state.user?.role_name === 'student',
		userName: (state) =>
			state.user ? `${state.user.name} ${state.user.surname}` : '',
		hasActiveSubscription: (state) => {
			if (!state.user?.subscribed_until_date) return false;
			return new Date(state.user.subscribed_until_date) > new Date();
		},
		subscriptionExpiryDate: (state) => {
			if (!state.user?.subscribed_until_date) return null;
			return new Date(state.user.subscribed_until_date);
		},
	},

	actions: {
		async register(userData) {
			this.loading = true;
			try {
				const response = await authApi.register(userData);
				this.token = response.data.access_token;
				localStorage.setItem('access_token', this.token);
				await this.fetchUser();
				return { success: true };
			} catch (error) {
				return {
					success: false,
					error: error.response?.data?.detail || 'Registration failed',
				};
			} finally {
				this.loading = false;
			}
		},

		async login(credentials) {
			this.loading = true;
			try {
				const response = await authApi.login(credentials);
				this.token = response.data.access_token;
				localStorage.setItem('access_token', this.token);
				await this.fetchUser();
				return { success: true };
			} catch (error) {
				return {
					success: false,
					error: error.response?.data?.detail || 'Login failed',
				};
			} finally {
				this.loading = false;
			}
		},

		async fetchUser() {
			if (!this.token) return;
			try {
				const response = await authApi.getMe();
				this.user = response.data;
			} catch (error) {
				this.logout();
			}
		},

		async updateUser(userData) {
			try {
				const response = await authApi.updateMe(userData);
				this.user = response.data;
				return { success: true, data: response.data };
			} catch (error) {
				return {
					success: false,
					error: error.response?.data?.detail || 'Update failed',
				};
			}
		},

		async deleteAccount() {
			try {
				await authApi.deleteMe();
				this.logout();
				return { success: true };
			} catch (error) {
				return {
					success: false,
					error: error.response?.data?.detail || 'Delete failed',
				};
			}
		},

		async applyForAuthor() {
			try {
				await authApi.applyForAuthor();
				await this.fetchUser();
				return { success: true };
			} catch (error) {
				return {
					success: false,
					error: error.response?.data?.detail || 'Application failed',
				};
			}
		},

		async subscribe() {
			try {
				await authApi.subscribe();
				await this.fetchUser();
				return { success: true };
			} catch (error) {
				return {
					success: false,
					error: error.response?.data?.detail || 'Subscription failed',
				};
			}
		},

		logout() {
			this.user = null;
			this.token = null;
			localStorage.removeItem('access_token');
		},
	},
});
