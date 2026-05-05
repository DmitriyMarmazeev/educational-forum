<template>
	<router-link
		:to="`/tasks/${task.id_task}`"
		class="glass-card p-6 hover:scale-[1.02] transition-all duration-300 block group">
		<div class="flex justify-between items-start mb-4">
			<span
				class="text-xs font-semibold px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-lg">
				{{ task.subject_name }}
			</span>
			<div class="flex items-center gap-1">
				<svg
					class="w-4 h-4 text-yellow-400"
					fill="currentColor"
					viewBox="0 0 20 20">
					<path
						d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
				</svg>
				<span class="text-sm text-gray-600 dark:text-gray-400">{{
					task.average_rating?.toFixed(1) || 'No ratings'
				}}</span>
			</div>
		</div>

		<h3
			class="text-lg font-bold text-gray-900 dark:text-white mb-3 line-clamp-2">
			Problem #{{ task.task_number }}
		</h3>

		<p class="text-gray-600 dark:text-gray-400 text-sm line-clamp-3 mb-4">
			{{ task.condition }}
		</p>

		<div
			class="flex justify-between items-center text-sm text-gray-500 dark:text-gray-500">
			<span>By {{ task.author_name || 'Unknown' }}</span>
			<span>{{ task.comments_count || 0 }} comments</span>
		</div>
	</router-link>
</template>

<script setup>
	defineProps({
		task: {
			type: Object,
			required: true,
		},
	});
</script>
