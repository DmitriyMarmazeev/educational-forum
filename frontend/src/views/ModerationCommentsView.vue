<template>
	<div class="space-y-6 animate-fade-in">
		<div class="glass-card p-6">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
				Comment Moderation
			</h1>
			<p class="text-gray-600 dark:text-gray-400">
				Review and manage user comments
			</p>
		</div>

		<div class="glass-card p-6">
			<div
				v-if="loading"
				class="flex justify-center py-8">
				<div
					class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
			</div>

			<div
				v-else-if="comments.length === 0"
				class="text-center py-8 text-gray-500">
				No comments to moderate
			</div>

			<div
				v-else
				class="space-y-4">
				<div
					v-for="comment in comments"
					:key="comment.id_task_comment"
					class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
					<div class="flex justify-between items-start">
						<div class="flex-1">
							<div class="flex items-center gap-2 mb-2">
								<span class="text-sm font-semibold">{{
									comment.user_email || `User #${comment.user_id}`
								}}</span>
								<span class="text-xs text-gray-500"
									>Task ID: {{ comment.task_id }}</span
								>
							</div>
							<p class="text-gray-700 dark:text-gray-300">
								{{ comment.comment }}
							</p>
							<p class="text-xs text-gray-500 mt-2">
								{{ formatDate(comment.created_at) }}
							</p>
						</div>
						<button
							@click="deleteComment(comment)"
							class="btn-outline px-3 py-1 text-sm text-red-500">
							Delete
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { moderatorApi } from '../api';

	const comments = ref([]);
	const loading = ref(false);

	const formatDate = (date) => {
		if (!date) return '';
		return new Date(date).toLocaleString();
	};

	const loadComments = async () => {
		loading.value = true;
		try {
			const response = await moderatorApi.getCommentsForModeration();
			comments.value = response.data;
		} catch (error) {
			console.error('Failed to load comments', error);
		} finally {
			loading.value = false;
		}
	};

	const deleteComment = async (comment) => {
		if (confirm('Are you sure you want to delete this comment?')) {
			try {
				await moderatorApi.deleteCommentByModerator(comment.id_task_comment);
				comments.value = comments.value.filter(
					(c) => c.id_task_comment !== comment.id_task_comment,
				);
			} catch (error) {
				console.error('Failed to delete comment', error);
			}
		}
	};

	onMounted(() => {
		loadComments();
	});
</script>
