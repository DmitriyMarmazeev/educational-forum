<template>
	<div class="space-y-8 animate-fade-in pt-6">
		<div class="text-center space-y-4">
			<h1
				class="text-3xl/[1.2] sm:text-5xl/[1.2] font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
				Образовательный форум
			</h1>
			<p class="text-base sm:text-xl text-gray-600 dark:text-gray-400">
				Создавайте, обсуждайте и делитесь заданиями по различным предметам
			</p>
		</div>

		<div class="glass-card p-6">
			<div class="flex flex-wrap gap-4 items-end">
				<div class="flex-1 min-w-[200px]">
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Предмет</label
					>
					<select
						v-model="filters.subject_id"
						@change="applyFilters"
						class="input-field">
						<option :value="null">Все предметы</option>
						<option value="1">Математика</option>
						<option value="2">Русский язык</option>
						<option value="3">Физика</option>
						<option value="4">Информатика</option>
						<option value="5">История</option>
					</select>
				</div>

				<div class="flex-1 min-w-[150px]">
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>№ задания</label
					>
					<input
						type="number"
						v-model.number="filters.task_number"
						@input="applyFilters"
						placeholder="№ задания"
						class="input-field" />
				</div>

				<button
					@click="resetFilters"
					class="btn-outline px-4 py-3">
					Сбросить
				</button>
			</div>
		</div>

		<div
			v-if="tasksStore.loading"
			class="flex justify-center py-12">
			<div
				class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
		</div>

		<div
			v-else-if="tasksStore.tasks.length === 0"
			class="glass-card p-12 text-center">
			<p class="text-gray-500 dark:text-gray-400">Задания не найдены</p>
		</div>

		<div
			v-else
			class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			<TaskCard
				v-for="task in tasksStore.tasks"
				:key="task.id_task"
				:task="task" />
		</div>

		<div class="flex justify-center gap-4 pt-4">
			<button
				@click="prevPage"
				:disabled="skip === 0"
				class="btn-outline px-6 py-2 disabled:opacity-50 disabled:cursor-not-allowed">
				Предыдущая
			</button>
			<button
				@click="nextPage"
				class="btn-outline px-6 py-2">
				Следующая
			</button>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted, watch } from 'vue';
	import { useTasksStore } from '../stores/tasks';
	import TaskCard from '../components/TaskCard.vue';

	const tasksStore = useTasksStore();
	const filters = ref({
		subject_id: null,
		task_number: null,
	});
	const skip = ref(0);
	const limit = ref(20);

	const loadTasks = async () => {
		await tasksStore.fetchTasks({
			subject_id: filters.value.subject_id,
			task_number: filters.value.task_number,
			skip: skip.value,
			limit: limit.value,
		});
	};

	const applyFilters = () => {
		skip.value = 0;
		loadTasks();
	};

	const resetFilters = () => {
		filters.value = { subject_id: null, task_number: null };
		skip.value = 0;
		loadTasks();
	};

	const prevPage = () => {
		if (skip.value >= limit.value) {
			skip.value -= limit.value;
			loadTasks();
		}
	};

	const nextPage = () => {
		skip.value += limit.value;
		loadTasks();
	};

	onMounted(() => {
		loadTasks();
	});
</script>
