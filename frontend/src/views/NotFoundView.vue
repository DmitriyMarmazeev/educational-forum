<template>
	<div
		class="min-h-[calc(100vh-200px)] flex items-center justify-center py-12">
		<div class="glass-card p-12 text-center max-w-md w-full animate-fade-in">
			<div class="mb-6">
				<div
					class="w-24 h-24 mx-auto bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
					<svg
						class="w-12 h-12 text-white"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
				</div>
			</div>

			<h1 class="text-6xl font-bold text-gray-900 dark:text-white mb-4">
				404
			</h1>
			<h2 class="text-2xl font-semibold text-gray-700 dark:text-gray-300 mb-4">
				Страница не найдена
			</h2>
			<p class="text-gray-500 dark:text-gray-400 mb-8">
				К сожалению, запрашиваемая страница не существует или была перемещена.
			</p>

			<div class="flex flex-col sm:flex-row gap-4 justify-center">
				<router-link
					to="/"
					class="btn-primary">
					На главную
				</router-link>
				<button
					@click="goBack"
					class="btn-outline">
					Вернуться назад
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { useRouter } from 'vue-router';

	const router = useRouter();

	const goBack = () => {
		router.back();
	};
</script>
