<template>
	<div class="max-w-4xl mx-auto animate-fade-in">
		<div class="glass-card p-8">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
				Создать новое задание
			</h1>
			<p class="text-gray-600 dark:text-gray-400 mb-8">
				Делитесь новыми заданиями с сообществом
			</p>

			<form
				@submit.prevent="handleSubmit"
				class="space-y-6">
				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Предмет *</label
					>
					<select
						v-model="form.id_subject"
						class="input-field"
						required>
						<option value="">Выберите предмет</option>
						<option :value="1">Математика</option>
						<option :value="2">Русский язык</option>
						<option :value="3">Физика</option>
						<option :value="4">Информатика</option>
						<option :value="5">История</option>
					</select>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Номер задания *</label
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
						>Условие *</label
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
						>Ответ *</label
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
						>Решение *</label
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
						>Ссылка на картинку (необязательно)</label
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

				<div class="flex gap-4 flex-wrap">
					<button
						type="submit"
						:disabled="loading"
						class="btn-primary">
						{{ loading ? 'Создаём...' : 'Создать задание' }}
					</button>
					<router-link
						to="/"
						class="btn-outline"
						>Отменить</router-link
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
			error.value = 'Выберите предмет';
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
			error.value = result.error || 'Не удалось создать задание';
		}

		loading.value = false;
	};
</script>
