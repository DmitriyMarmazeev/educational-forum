<template>
	<div class="max-w-4xl mx-auto animate-fade-in">
		<div class="glass-card p-8">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
				Create New Task
			</h1>
			<p class="text-gray-600 dark:text-gray-400 mb-8">
				Share a new problem with the community
			</p>

			<form
				@submit.prevent="handleSubmit"
				class="space-y-6">
				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Subject *</label
					>
					<select
						v-model="form.id_subject"
						class="input-field"
						required>
						<option value="">Select subject</option>
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
						>Task Number *</label
					>
					<input
						type="number"
						v-model="form.task_number"
						class="input-field"
						required
						placeholder="e.g., 42" />
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Condition *</label
					>
					<textarea
						v-model="form.condition"
						rows="6"
						class="input-field"
						required
						placeholder="Describe the problem in detail..."></textarea>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Answer *</label
					>
					<input
						type="text"
						v-model="form.answer"
						class="input-field"
						required
						placeholder="The correct answer" />
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Solution *</label
					>
					<textarea
						v-model="form.solution"
						rows="4"
						class="input-field"
						required
						placeholder="Step-by-step solution explanation..."></textarea>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Image URL (optional)</label
					>
					<input
						type="text"
						v-model="form.image"
						class="input-field"
						placeholder="https://example.com/image.jpg" />
				</div>

				<div
					v-if="error"
					class="error-message text-center p-3 bg-red-50 dark:bg-red-900/30 rounded-lg">
					{{ error }}
				</div>

				<div class="flex gap-4">
					<button
						type="submit"
						:disabled="loading"
						class="btn-primary">
						{{ loading ? 'Creating...' : 'Create Task' }}
					</button>
					<router-link
						to="/"
						class="btn-outline"
						>Cancel</router-link
					>
				</div>
			</form>
		</div>
	</div>
</template>

<script setup>
	import { ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { useTasksStore } from '../stores/tasks';

	const router = useRouter();
	const tasksStore = useTasksStore();

	const form = ref({
		condition: '',
		image: null,
		answer: '',
		task_number: null,
		id_subject: '',
		solution: '',
	});

	const loading = ref(false);
	const error = ref('');

	const handleSubmit = async () => {
		if (!form.value.id_subject) {
			error.value = 'Please select a subject';
			return;
		}

		loading.value = true;
		error.value = '';

		const result = await tasksStore.createTask({
			condition: form.value.condition,
			image: form.value.image || null,
			answer: form.value.answer,
			task_number: form.value.task_number,
			id_subject: parseInt(form.value.id_subject),
			solution: form.value.solution,
		});

		if (result.success) {
			router.push(`/tasks/${result.data.id_task}`);
		} else {
			error.value = result.error || 'Failed to create task';
		}

		loading.value = false;
	};
</script>
