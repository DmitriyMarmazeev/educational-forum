<!-- frontend/src/views/EditTaskView.vue -->
<template>
	<div class="max-w-4xl mx-auto animate-fade-in">
		<!-- Состояние загрузки -->
		<div
			v-if="loading"
			class="flex justify-center py-12">
			<div
				class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
		</div>

		<!-- Ошибка -->
		<div
			v-else-if="error"
			class="glass-card p-8 text-center">
			<p class="text-red-500 dark:text-red-400">{{ error }}</p>
			<router-link
				to="/"
				class="btn-primary mt-4 inline-block"
				>Back to Tasks</router-link
			>
		</div>

		<!-- Форма редактирования -->
		<div
			v-else-if="task"
			class="glass-card p-8">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
				Edit Task
			</h1>
			<p class="text-gray-600 dark:text-gray-400 mb-8">Update your problem</p>

			<form
				@submit.prevent="handleSubmit"
				class="space-y-6">
				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Subject</label
					>
					<select
						v-model="form.id_subject"
						class="input-field">
						<option :value="null">Select subject</option>
						<option :value="1">Mathematics</option>
						<option :value="2">Physics</option>
						<option :value="3">Chemistry</option>
						<option :value="4">Biology</option>
						<option :value="5">Computer Science</option>
					</select>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Task Number</label
					>
					<input
						type="number"
						v-model="form.task_number"
						class="input-field" />
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Condition</label
					>
					<textarea
						v-model="form.condition"
						rows="6"
						class="input-field"></textarea>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Answer</label
					>
					<input
						type="text"
						v-model="form.answer"
						class="input-field" />
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Solution</label
					>
					<textarea
						v-model="form.solution"
						rows="4"
						class="input-field"></textarea>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Image URL</label
					>
					<input
						type="text"
						v-model="form.image"
						class="input-field"
						placeholder="https://example.com/image.jpg" />
				</div>

				<div
					v-if="submitError"
					class="error-message text-center p-3 bg-red-50 dark:bg-red-900/30 rounded-lg">
					{{ submitError }}
				</div>

				<div class="flex gap-4">
					<button
						type="submit"
						:disabled="submitting"
						class="btn-primary">
						{{ submitting ? 'Saving...' : 'Save Changes' }}
					</button>
					<router-link
						:to="`/tasks/${taskId}`"
						class="btn-outline"
						>Cancel</router-link
					>
					<button
						v-if="canDelete"
						type="button"
						@click="showDeleteModal = true"
						class="btn-outline text-red-500 border-red-500 hover:bg-red-50">
						Delete Task
					</button>
				</div>
			</form>
		</div>

		<!-- Модальное окно подтверждения удаления -->
		<div
			v-if="showDeleteModal"
			class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in"
			@click.self="showDeleteModal = false">
			<div class="glass-card p-6 max-w-md w-full mx-4">
				<h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">
					Delete Task
				</h3>
				<p class="text-gray-600 dark:text-gray-400 mb-6">
					Are you sure you want to delete this task? This action cannot be
					undone.
				</p>
				<div class="flex gap-4 justify-end">
					<button
						@click="showDeleteModal = false"
						class="btn-outline px-4 py-2">
						Cancel
					</button>
					<button
						@click="confirmDelete"
						:disabled="deleteLoading"
						class="btn-primary px-4 py-2 bg-red-500 hover:bg-red-600">
						{{ deleteLoading ? 'Deleting...' : 'Delete' }}
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, computed, onMounted } from 'vue';
	import { useRoute, useRouter } from 'vue-router';
	import { useTasksStore } from '../stores/tasks';
	import { useAuthStore } from '../stores/auth';

	const route = useRoute();
	const router = useRouter();
	const tasksStore = useTasksStore();
	const authStore = useAuthStore();

	const taskId = route.params.id;

	// Состояния
	const loading = ref(true);
	const error = ref('');
	const task = ref(null);
	const form = ref({
		condition: '',
		image: '',
		answer: '',
		task_number: null,
		id_subject: null,
		solution: '',
	});
	const submitting = ref(false);
	const submitError = ref('');
	const showDeleteModal = ref(false);
	const deleteLoading = ref(false);

	// Вычисляемые свойства
	const canDelete = computed(() => {
		if (!task.value || !authStore.user) return false;
		return (
			authStore.isModerator || authStore.user.id_user === task.value.author_id
		);
	});

	const loadTask = async () => {
		loading.value = true;
		error.value = '';

		try {
			const result = await tasksStore.fetchTask(taskId);
			if (result.success && result.data) {
				task.value = result.data;
				// Заполняем форму данными задачи
				form.value = {
					condition: result.data.condition || '',
					image: result.data.image || '',
					answer: result.data.answer || '',
					task_number: result.data.task_number || null,
					id_subject: null,
					solution: '',
				};
			} else {
				error.value = result.error || 'Task not found';
				// Перенаправляем на главную через 2 секунды
				setTimeout(() => {
					router.push('/');
				}, 2000);
			}
		} catch (err) {
			error.value = 'Failed to load task';
			console.error(err);
			setTimeout(() => {
				router.push('/');
			}, 2000);
		} finally {
			loading.value = false;
		}
	};

	const handleSubmit = async () => {
		submitting.value = true;
		submitError.value = '';

		const updateData = {};
		if (form.value.condition !== task.value.condition)
			updateData.condition = form.value.condition;
		if (form.value.image !== task.value.image)
			updateData.image = form.value.image;
		if (form.value.answer !== task.value.answer)
			updateData.answer = form.value.answer;
		if (form.value.task_number !== task.value.task_number)
			updateData.task_number = form.value.task_number;
		if (form.value.id_subject)
			updateData.id_subject = parseInt(form.value.id_subject);

		if (Object.keys(updateData).length === 0) {
			submitting.value = false;
			router.push(`/tasks/${taskId}`);
			return;
		}

		const result = await tasksStore.updateTask(taskId, updateData);

		if (result.success) {
			router.push(`/tasks/${taskId}`);
		} else {
			submitError.value = result.error || 'Failed to update task';
		}

		submitting.value = false;
	};

	const confirmDelete = async () => {
		deleteLoading.value = true;
		const result = await tasksStore.deleteTask(taskId);
		if (result.success) {
			router.push('/');
		} else {
			submitError.value = result.error || 'Failed to delete task';
			showDeleteModal.value = false;
		}
		deleteLoading.value = false;
	};

	onMounted(() => {
		loadTask();
	});
</script>
