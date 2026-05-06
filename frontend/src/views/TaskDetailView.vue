<template>
	<div class="max-w-4xl mx-auto space-y-8 animate-fade-in">
		<div
			v-if="loading"
			class="flex justify-center py-12">
			<div
				class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
		</div>

		<div
			v-else-if="error"
			class="glass-card p-8 text-center">
			<p class="text-red-500 dark:text-red-400">{{ error }}</p>
			<router-link
				to="/"
				class="btn-primary mt-4 inline-block"
				>Вернуться к заданиям</router-link
			>
		</div>

		<template v-else-if="task">
			<div class="glass-card p-8">
				<div class="flex justify-between items-start mb-6 flex-wrap gap-4">
					<div>
						<span
							class="text-sm font-semibold px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-full">
							{{ task.subject_name }}
						</span>
						<h1 class="text-3xl font-bold text-gray-900 dark:text-white mt-4">
							Задание №{{ task.task_number }}
						</h1>
					</div>
					<div class="flex items-center gap-2">
						<div class="flex items-center gap-1">
							<button
								v-for="star in 5"
								:key="star"
								@click="rateTask(star)"
								class="hover:scale-110 transition-transform"
								:disabled="!authStore.isAuthenticated">
								<span
									class="text-2xl"
									:class="
										star <= (userRating || task.average_rating || 0)
											? 'text-yellow-400'
											: 'text-gray-300 dark:text-gray-600'
									">
									★
								</span>
							</button>
						</div>
						<span class="text-sm text-gray-600 dark:text-gray-400 ml-2">
							Рейтинг: {{ task.average_rating?.toFixed(1) || '0' }}
						</span>
					</div>
				</div>

				<div class="prose dark:prose-invert max-w-none mb-8">
					<h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white">
						Условие
					</h3>
					<p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
						{{ task.condition }}
					</p>

					<h3
						class="text-lg font-semibold mt-6 mb-2 text-gray-900 dark:text-white">
						Ответ
					</h3>
					<div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
						<p class="text-gray-700 dark:text-gray-300 font-mono">
							{{ task.answer }}
						</p>
					</div>

					<h3
						v-if="showSolution"
						class="text-lg font-semibold mt-6 mb-2 text-gray-900 dark:text-white">
						Решение
					</h3>
					<div
						v-if="showSolution"
						class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
						<p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
							{{ solutionText }}
						</p>
					</div>

					<div
						v-else-if="canViewSolution"
						class="mt-6">
						<button
							@click="loadSolution"
							:disabled="solutionLoading"
							class="btn-primary">
							{{ solutionLoading ? 'Загрузка...' : 'Показать решение' }}
						</button>
					</div>

					<div
						v-else-if="
							isRegularUser &&
							!hasActiveSubscription &&
							authStore.isAuthenticated
						"
						class="mt-6 p-4 bg-yellow-50 dark:bg-yellow-900/30 rounded-lg">
						<p class="text-yellow-800 dark:text-yellow-200">
							Оформите подписку, чтобы просмотреть решение!
						</p>
						<button
							@click="subscribe"
							:disabled="subscribing"
							class="btn-primary mt-3 px-4 py-2 text-sm">
							{{ subscribing ? 'Обработка...' : 'Оформить подписку' }}
						</button>
					</div>

					<div
						v-else-if="!authStore.isAuthenticated"
						class="mt-6 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-center">
						<router-link
							to="/login"
							class="text-primary-500"
							>Login</router-link
						>
						чтобы посмотреть решение
					</div>
				</div>

				<div
					v-if="isOwner"
					class="flex gap-4 mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
					<router-link
						:to="`/tasks/${task.id_task}/edit`"
						class="btn-outline">
						Редактировать задание
					</router-link>
					<button
						@click="showDeleteModal = true"
						class="btn-outline text-red-500 border-red-500 hover:bg-red-50 dark:hover:bg-red-900/30">
						Удалить задание
					</button>
				</div>
			</div>

			<div class="glass-card p-8">
				<h3 class="text-xl font-bold mb-6 text-gray-900 dark:text-white">
					Комментарии ({{ comments.length }})
				</h3>

				<div
					v-if="authStore.isAuthenticated"
					class="mb-8">
					<textarea
						v-model="newCommentText"
						rows="3"
						class="input-field"
						placeholder="Написать комментарий..."></textarea>
					<button
						@click="submitComment"
						:disabled="commentLoading"
						class="btn-primary mt-3 px-6 py-2">
						{{ commentLoading ? 'Отправка...' : 'Отправить' }}
					</button>
				</div>

				<div
					v-else
					class="mb-8 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-center">
					<router-link
						to="/login"
						class="text-primary-500"
						>Войти</router-link
					>
          чтобы оставить комментарий
				</div>

				<div
					v-if="commentsLoading"
					class="flex justify-center py-4">
					<div
						class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-500"></div>
				</div>

				<div
					v-else-if="comments.length === 0"
					class="text-center py-8 text-gray-500 dark:text-gray-400">
					Комментариев пока нет. Будьте первыми, кто оставит комментарий!
				</div>

				<div
					v-else
					class="space-y-6">
					<div
						v-for="comment in comments"
						:key="comment.id_task_comment"
						class="border-b border-gray-200 dark:border-gray-700 pb-4 last:border-0">
						<div class="flex justify-between items-start mb-2">
							<div class="flex items-center gap-2">
								<span class="font-semibold text-gray-900 dark:text-white">{{
									comment.user_name || 'Студент'
								}}</span>
								<span class="text-xs text-gray-500">{{
									formatDate(comment.created_at)
								}}</span>
							</div>
							<button
								v-if="authStore.isModerator"
								@click="deleteComment(comment.id_task_comment)"
								:disabled="deletingCommentId === comment.id_task_comment"
								class="text-red-500 hover:text-red-700 transition-colors text-sm"
								title="Удалить комментарий">
								{{
									deletingCommentId === comment.id_task_comment
										? '...'
										: 'Удалить'
								}}
							</button>
						</div>
						<p class="text-gray-600 dark:text-gray-400">
							{{ comment.comment }}
						</p>
					</div>
				</div>
			</div>
		</template>

		<div
			v-if="showDeleteModal"
			class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in"
			@click.self="showDeleteModal = false">
			<div class="glass-card p-6 max-w-md w-full mx-4">
				<h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">
					Удалить задание
				</h3>
				<p class="text-gray-600 dark:text-gray-400 mb-6">
					Вы уверены, что хотите удалить это задание? Это действие нельзя отменить.
				</p>
				<div class="flex gap-4 justify-end">
					<button
						@click="showDeleteModal = false"
						class="btn-outline px-4 py-2">
						Отменить
					</button>
					<button
						@click="confirmDelete"
						:disabled="deleteLoading"
						class="btn-primary px-4 py-2 bg-red-500 hover:bg-red-600">
						{{ deleteLoading ? 'Удаление...' : 'Удалить' }}
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
	import { moderatorApi } from '../api';

	const route = useRoute();
	const router = useRouter();
	const tasksStore = useTasksStore();
	const authStore = useAuthStore();

	const taskId = route.params.id;

	const loading = ref(true);
	const error = ref('');
	const task = ref(null);
	const solutionText = ref('');
	const showSolution = ref(false);
	const solutionLoading = ref(false);
	const comments = ref([]);
	const commentsLoading = ref(false);
	const newCommentText = ref('');
	const commentLoading = ref(false);
	const showDeleteModal = ref(false);
	const deleteLoading = ref(false);
	const subscribing = ref(false);
	const userRating = ref(null);
	const deletingCommentId = ref(null);

	const isOwner = computed(() => {
		if (!task.value || !authStore.user) return false;
		return authStore.user.id_user === task.value.author_id;
	});

	const isRegularUser = computed(() => {
		if (!authStore.isAuthenticated) return false;
		const role = authStore.user?.role_name;
		return role === 'student';
	});

	const hasActiveSubscription = computed(() => {
		if (!authStore.user?.subscribed_until_date) return false;
		return new Date(authStore.user.subscribed_until_date) > new Date();
	});

	const canViewSolution = computed(() => {
		if (!authStore.isAuthenticated) return false;

		const role = authStore.user?.role_name;

		if (role === 'moderator' || role === 'admin') return true;

		if (isOwner.value) return true;

		if (role === 'student' && hasActiveSubscription.value) return true;

		return false;
	});

	const formatDate = (date) => {
		if (!date) return '';
		return new Date(date).toLocaleDateString('ru-RU', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
		});
	};

	const loadTask = async () => {
		loading.value = true;
		error.value = '';

		try {
			const result = await tasksStore.fetchTask(taskId);
			if (result.success && result.data) {
				task.value = result.data;
			} else {
				error.value = result.error || 'Задание не найдено';
			}
		} catch (err) {
			error.value = 'Не удалось загрузить задание';
			console.error(err);
		} finally {
			loading.value = false;
		}
	};

	const loadSolution = async () => {
		solutionLoading.value = true;
		try {
			const result = await tasksStore.fetchSolution(taskId);
			if (result.success && result.data) {
				solutionText.value = result.data.solution;
				showSolution.value = true;
			} else {
				alert(result.error || 'Не удалось загрузить решение');
			}
		} catch (err) {
			alert('Не удалось загрузить решение');
			console.error(err);
		} finally {
			solutionLoading.value = false;
		}
	};

	const loadComments = async () => {
		commentsLoading.value = true;
		try {
			const result = await tasksStore.fetchComments(taskId);
			if (result.success) {
				comments.value = result.data || [];
			}
		} catch (err) {
			console.error('Не удалось загрузить комментарии', err);
		} finally {
			commentsLoading.value = false;
		}
	};

	const rateTask = async (rating) => {
		if (!authStore.isAuthenticated) {
			alert('Войдите, чтобы оценить задание');
			router.push('/login');
			return;
		}

		try {
			const result = await tasksStore.rateTask(taskId, rating);
			if (result.success) {
				userRating.value = rating;
				await loadTask();
			} else {
				alert(result.error || 'Не удалось оценить задание');
			}
		} catch (err) {
			alert('Не удалось оценить задание');
			console.error(err);
		}
	};

	const submitComment = async () => {
		if (!newCommentText.value.trim()) {
			alert('Пожалуйста, введите комментарий');
			return;
		}

		commentLoading.value = true;
		try {
			const result = await tasksStore.addComment(taskId, newCommentText.value);
			if (result.success) {
				newCommentText.value = '';
				await loadComments();
			} else {
				alert(result.error || 'Не удалось отправить комментарий');
			}
		} catch (err) {
			alert('Не удалось отправить комментарий');
			console.error(err);
		} finally {
			commentLoading.value = false;
		}
	};

	const deleteComment = async (commentId) => {
		if (!confirm('Вы уверены, что хотите удалить этот комментарий?')) return;

		deletingCommentId.value = commentId;
		try {
			await moderatorApi.deleteCommentByModerator(commentId);
			await loadComments();
		} catch (err) {
			console.error('Не удалось удалить комментарий', err);
			alert('Не удалось удалить комментарий');
		} finally {
			deletingCommentId.value = null;
		}
	};

	const subscribe = async () => {
		subscribing.value = true;
		const result = await authStore.subscribe();
		if (result.success) {
			alert('Подписка оформлена!');
			await loadTask();
		} else {
			alert(result.error || 'Не удалось оформить подписку');
		}
		subscribing.value = false;
	};

	const confirmDelete = async () => {
		deleteLoading.value = true;
		try {
			const result = await tasksStore.deleteTask(taskId);
			if (result.success) {
				router.push('/');
			} else {
				alert(result.error || 'Не удалось удалить задание');
				showDeleteModal.value = false;
			}
		} catch (err) {
			alert('Не удалось удалить задание');
			console.error(err);
		} finally {
			deleteLoading.value = false;
		}
	};

	onMounted(async () => {
		if (authStore.token && !authStore.user) {
			await authStore.fetchUser();
		}
		await loadTask();
		await loadComments();
	});
</script>
