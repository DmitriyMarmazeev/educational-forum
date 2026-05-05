<!-- frontend/src/views/TaskDetailView.vue -->
<template>
	<div class="max-w-4xl mx-auto space-y-8 animate-fade-in">
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

		<!-- Данные задачи -->
		<template v-else-if="task">
			<div class="glass-card p-8">
				<div class="flex justify-between items-start mb-6 flex-wrap gap-4">
					<div>
						<span
							class="text-sm font-semibold px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-full">
							{{ task.subject_name }}
						</span>
						<h1 class="text-3xl font-bold text-gray-900 dark:text-white mt-4">
							Problem #{{ task.task_number }}
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
							{{ task.average_rating?.toFixed(1) || '0' }} ({{
								task.ratings_count || 0
							}}
							ratings)
						</span>
					</div>
				</div>

				<div class="prose dark:prose-invert max-w-none mb-8">
					<h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white">
						Condition
					</h3>
					<p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
						{{ task.condition }}
					</p>

					<h3
						class="text-lg font-semibold mt-6 mb-2 text-gray-900 dark:text-white">
						Answer
					</h3>
					<div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg">
						<p class="text-gray-700 dark:text-gray-300 font-mono">
							{{ task.answer }}
						</p>
					</div>

					<h3
						v-if="showSolution"
						class="text-lg font-semibold mt-6 mb-2 text-gray-900 dark:text-white">
						Solution
					</h3>
					<div
						v-if="showSolution"
						class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
						<p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
							{{ solutionText }}
						</p>
					</div>

					<!-- Кнопка показа решения - доступна только если пользователь может видеть решение -->
					<div
						v-else-if="canViewSolution"
						class="mt-6">
						<button
							@click="loadSolution"
							:disabled="solutionLoading"
							class="btn-primary">
							{{ solutionLoading ? 'Loading...' : 'Show Solution' }}
						</button>
					</div>

					<!-- Блок для обычных пользователей без подписки (не author, не moderator, не admin) -->
					<div
						v-else-if="
							isRegularUser &&
							!hasActiveSubscription &&
							authStore.isAuthenticated
						"
						class="mt-6 p-4 bg-yellow-50 dark:bg-yellow-900/30 rounded-lg">
						<p class="text-yellow-800 dark:text-yellow-200">
							Subscribe to view the solution!
						</p>
						<button
							@click="subscribe"
							:disabled="subscribing"
							class="btn-primary mt-3 px-4 py-2 text-sm">
							{{ subscribing ? 'Processing...' : 'Subscribe Now' }}
						</button>
					</div>

					<!-- Блок для неавторизованных пользователей -->
					<div
						v-else-if="!authStore.isAuthenticated"
						class="mt-6 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-center">
						<router-link
							to="/login"
							class="text-primary-500"
							>Login</router-link
						>
						to view the solution
					</div>
				</div>

				<!-- Кнопки действий - только для автора задачи -->
				<div
					v-if="isOwner"
					class="flex gap-4 mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
					<router-link
						:to="`/tasks/${task.id_task}/edit`"
						class="btn-outline">
						Edit Task
					</router-link>
					<button
						@click="showDeleteModal = true"
						class="btn-outline text-red-500 border-red-500 hover:bg-red-50 dark:hover:bg-red-900/30">
						Delete Task
					</button>
				</div>
			</div>

			<!-- Комментарии -->
			<div class="glass-card p-8">
				<h3 class="text-xl font-bold mb-6 text-gray-900 dark:text-white">
					Comments ({{ comments.length }})
				</h3>

				<div
					v-if="authStore.isAuthenticated"
					class="mb-8">
					<textarea
						v-model="newCommentText"
						rows="3"
						class="input-field"
						placeholder="Write a comment..."></textarea>
					<button
						@click="submitComment"
						:disabled="commentLoading"
						class="btn-primary mt-3 px-6 py-2">
						{{ commentLoading ? 'Posting...' : 'Post Comment' }}
					</button>
				</div>

				<div
					v-else
					class="mb-8 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-center">
					<router-link
						to="/login"
						class="text-primary-500"
						>Login</router-link
					>
					to comment
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
					No comments yet. Be the first to comment!
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
									comment.user_name || 'User'
								}}</span>
								<span class="text-xs text-gray-500">{{
									formatDate(comment.created_at)
								}}</span>
							</div>
							<!-- Кнопка удаления комментария для модератора -->
							<button
								v-if="authStore.isModerator"
								@click="deleteComment(comment.id_task_comment)"
								:disabled="deletingCommentId === comment.id_task_comment"
								class="text-red-500 hover:text-red-700 transition-colors text-sm"
								title="Delete comment">
								{{
									deletingCommentId === comment.id_task_comment
										? '...'
										: 'Delete'
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

		<!-- Модальное окно подтверждения удаления задачи -->
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
	import { moderatorApi } from '../api';

	const route = useRoute();
	const router = useRouter();
	const tasksStore = useTasksStore();
	const authStore = useAuthStore();

	const taskId = route.params.id;

	// Состояния
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

	// Вычисляемые свойства с правильным определением ролей
	const isOwner = computed(() => {
		if (!task.value || !authStore.user) return false;
		return authStore.user.id_user === task.value.author_id;
	});

	const isRegularUser = computed(() => {
		if (!authStore.isAuthenticated) return false;
		const role = authStore.user?.role_name;
		// Только обычный пользователь (user) считается регулярным
		return role === 'student';
	});

	const hasActiveSubscription = computed(() => {
		if (!authStore.user?.subscribed_until_date) return false;
		return new Date(authStore.user.subscribed_until_date) > new Date();
	});

	// Кто может видеть решение:
	// 1. Автор задачи
	// 2. Пользователь с активной подпиской (только обычные пользователи могут иметь подписку)
	// 3. Модератор (всегда)
	// 4. Админ (всегда)
	const canViewSolution = computed(() => {
		if (!authStore.isAuthenticated) return false;

		const role = authStore.user?.role_name;

		// Модератор и админ всегда видят решение
		if (role === 'moderator' || role === 'admin') return true;

		// Автор видит решение своей задачи
		if (isOwner.value) return true;

		// Обычный пользователь с активной подпиской видит решение
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
				error.value = result.error || 'Task not found';
			}
		} catch (err) {
			error.value = 'Failed to load task';
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
				alert(result.error || 'Failed to load solution');
			}
		} catch (err) {
			alert('Failed to load solution');
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
			console.error('Failed to load comments', err);
		} finally {
			commentsLoading.value = false;
		}
	};

	const rateTask = async (rating) => {
		if (!authStore.isAuthenticated) {
			alert('Please login to rate');
			router.push('/login');
			return;
		}

		try {
			const result = await tasksStore.rateTask(taskId, rating);
			if (result.success) {
				userRating.value = rating;
				await loadTask();
			} else {
				alert(result.error || 'Failed to rate task');
			}
		} catch (err) {
			alert('Failed to rate task');
			console.error(err);
		}
	};

	const submitComment = async () => {
		if (!newCommentText.value.trim()) {
			alert('Please enter a comment');
			return;
		}

		commentLoading.value = true;
		try {
			const result = await tasksStore.addComment(taskId, newCommentText.value);
			if (result.success) {
				newCommentText.value = '';
				await loadComments();
			} else {
				alert(result.error || 'Failed to post comment');
			}
		} catch (err) {
			alert('Failed to post comment');
			console.error(err);
		} finally {
			commentLoading.value = false;
		}
	};

	const deleteComment = async (commentId) => {
		if (!confirm('Are you sure you want to delete this comment?')) return;

		deletingCommentId.value = commentId;
		try {
			await moderatorApi.deleteCommentByModerator(commentId);
			await loadComments();
		} catch (err) {
			console.error('Failed to delete comment', err);
			alert('Failed to delete comment');
		} finally {
			deletingCommentId.value = null;
		}
	};

	const subscribe = async () => {
		subscribing.value = true;
		const result = await authStore.subscribe();
		if (result.success) {
			alert('Successfully subscribed!');
			await loadTask();
		} else {
			alert(result.error || 'Failed to subscribe');
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
				alert(result.error || 'Failed to delete task');
				showDeleteModal.value = false;
			}
		} catch (err) {
			alert('Failed to delete task');
			console.error(err);
		} finally {
			deleteLoading.value = false;
		}
	};

	onMounted(async () => {
		// Убеждаемся, что данные пользователя загружены
		if (authStore.token && !authStore.user) {
			await authStore.fetchUser();
		}
		await loadTask();
		await loadComments();
	});
</script>
