<template>
	<div class="space-y-6 animate-fade-in">
		<div class="glass-card p-6">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
				Task Moderation
			</h1>
			<p class="text-gray-600 dark:text-gray-400">
				Review and manage submitted tasks
			</p>
		</div>

		<div class="glass-card p-6">
			<div class="flex gap-4 mb-6">
				<select
					v-model="statusFilter"
					@change="loadTasks"
					class="input-field w-48">
					<option :value="null">All Status</option>
					<option value="draft">Draft</option>
					<option value="public">Public</option>
					<option value="rejected">Rejected</option>
					<option value="archived">Archived</option>
				</select>
			</div>

			<div
				v-if="loading"
				class="flex justify-center py-8">
				<div
					class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
			</div>

			<div
				v-else-if="tasks.length === 0"
				class="text-center py-8 text-gray-500">
				No tasks to moderate
			</div>

			<div
				v-else
				class="space-y-4">
				<div
					v-for="task in tasks"
					:key="task.id_task"
					class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
					<div class="flex justify-between items-start">
						<div class="flex-1">
							<div class="flex items-center gap-2 mb-2">
								<span
									class="text-xs font-semibold px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded"
									>{{ task.subject_name }}</span
								>
								<span
									class="text-xs font-semibold px-2 py-1 rounded"
									:class="statusClass(task.status)">
									{{ task.status }}
								</span>
							</div>
							<h3 class="text-lg font-bold mb-2">
								Task #{{ task.task_number }}
							</h3>
							<p
								class="text-gray-600 dark:text-gray-400 text-sm mb-2 line-clamp-2">
								{{ task.condition }}
							</p>
							<p class="text-sm text-gray-500">
								Author: {{ task.author_name || task.author_email }}
							</p>
						</div>
						<div class="flex gap-2">
							<select
								v-model="task.newStatus"
								@change="changeStatus(task)"
								class="input-field text-sm py-1 w-28">
								<option value="draft">Draft</option>
								<option value="public">Approve</option>
								<option value="rejected">Reject</option>
								<option value="archived">Archive</option>
							</select>
							<button
								@click="deleteTask(task)"
								class="btn-outline px-3 py-1 text-sm text-red-500">
								Delete
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { moderatorApi } from '../api';

	const tasks = ref([]);
	const loading = ref(false);
	const statusFilter = ref(null);

	const statusClass = (status) => {
		const classes = {
			draft:
				'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
			public:
				'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
			rejected: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
			archived:
				'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
		};
		return classes[status] || classes.draft;
	};

	const loadTasks = async () => {
		loading.value = true;
		try {
			const params = {};
			if (statusFilter.value) params.status = statusFilter.value;
			const response = await moderatorApi.getTasksForModeration(params);
			tasks.value = response.data.map((t) => ({ ...t, newStatus: t.status }));
		} catch (error) {
			console.error('Failed to load tasks', error);
		} finally {
			loading.value = false;
		}
	};

	const changeStatus = async (task) => {
		try {
			await moderatorApi.changeTaskStatus(task.id_task, task.newStatus);
			task.status = task.newStatus;
		} catch (error) {
			task.newStatus = task.status;
			console.error('Failed to change status', error);
		}
	};

	const deleteTask = async (task) => {
		if (confirm('Are you sure you want to delete this task?')) {
			try {
				await moderatorApi.deleteTaskByModerator(task.id_task);
				tasks.value = tasks.value.filter((t) => t.id_task !== task.id_task);
			} catch (error) {
				console.error('Failed to delete task', error);
			}
		}
	};

	onMounted(() => {
		loadTasks();
	});
</script>
