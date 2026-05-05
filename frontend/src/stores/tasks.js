// frontend/src/stores/tasks.js
import { defineStore } from 'pinia';
import { tasksApi } from '../api';

export const useTasksStore = defineStore('tasks', {
	state: () => ({
		tasks: [],
		currentTask: null,
		currentSolution: null,
		comments: [],
		loading: false,
		total: 0,
		filters: {
			subject_id: null,
			task_number: null,
			skip: 0,
			limit: 20,
		},
	}),

	actions: {
		async fetchTasks(params = {}) {
			this.loading = true;
			try {
				const response = await tasksApi.getTasks({
					...this.filters,
					...params,
				});
				this.tasks = response.data;
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Fetch tasks error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Failed to fetch tasks',
				};
			} finally {
				this.loading = false;
			}
		},

		async fetchTask(taskId) {
			this.loading = true;
			try {
				const response = await tasksApi.getTask(taskId);
				this.currentTask = response.data;
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Fetch task error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Task not found',
				};
			} finally {
				this.loading = false;
			}
		},

		async fetchSolution(taskId) {
			this.loading = true;
			try {
				const response = await tasksApi.getSolution(taskId);
				this.currentSolution = response.data;
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Fetch solution error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Solution not available',
				};
			} finally {
				this.loading = false;
			}
		},

		async createTask(taskData) {
			this.loading = true;
			try {
				const response = await tasksApi.createTask(taskData);
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Create task error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Failed to create task',
				};
			} finally {
				this.loading = false;
			}
		},

		async updateTask(taskId, taskData) {
			this.loading = true;
			try {
				const response = await tasksApi.updateTask(taskId, taskData);
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Update task error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Failed to update task',
				};
			} finally {
				this.loading = false;
			}
		},

		async deleteTask(taskId) {
			this.loading = true;
			try {
				await tasksApi.deleteTask(taskId);
				return { success: true };
			} catch (error) {
				console.error('Delete task error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Failed to delete task',
				};
			} finally {
				this.loading = false;
			}
		},

		async rateTask(taskId, rating) {
			try {
				const response = await tasksApi.rateTask(taskId, rating);
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Rate task error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Failed to rate task',
				};
			}
		},

		async fetchComments(taskId) {
			try {
				const response = await tasksApi.getComments(taskId);
				this.comments = response.data || [];
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Fetch comments error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Failed to fetch comments',
				};
			}
		},

		async addComment(taskId, comment) {
			try {
				const response = await tasksApi.addComment(taskId, comment);
				return { success: true, data: response.data };
			} catch (error) {
				console.error('Add comment error:', error);
				return {
					success: false,
					error: error.response?.data?.detail || 'Failed to add comment',
				};
			}
		},

		setFilters(filters) {
			this.filters = { ...this.filters, ...filters };
		},

		resetFilters() {
			this.filters = {
				subject_id: null,
				task_number: null,
				skip: 0,
				limit: 20,
			};
		},
	},
});
