<template>
	<nav class="glass-card sticky top-4 mx-4 z-50">
		<div class="container mx-auto px-6 py-3">
			<div class="flex items-center justify-between flex-wrap">
				<router-link
					to="/"
					class="flex items-center space-x-3">
					<div
						class="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center">
						<svg
							class="w-6 h-6 text-white"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
						</svg>
					</div>
					<span
						class="text-xl font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent"
						>Зов Знаний</span
					>
				</router-link>

				<div class="flex items-center space-x-4">
					<router-link
						to="/"
						class="text-gray-700 dark:text-gray-300 hover:text-primary-500 dark:hover:text-primary-500 transition-colors">
						Tasks
					</router-link>

					<template v-if="authStore.isAuthenticated">
						<router-link
							v-if="authStore.isAuthor"
							to="/tasks/create"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors">
							Create Task
						</router-link>
						<router-link
							v-if="authStore.isModerator"
							to="/moderation/tasks"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors">
							Moderation
						</router-link>
						<router-link
							v-if="authStore.isAdmin"
							to="/admin/users"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors">
							Admin
						</router-link>
						<router-link
							to="/profile"
							class="flex items-center space-x-2">
							<div
								class="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
								{{ authStore.user?.name?.charAt(0) || 'U' }}
							</div>
						</router-link>
					</template>

					<template v-else>
						<router-link
							to="/login"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors">
							Login
						</router-link>
						<router-link
							to="/register"
							class="btn-primary px-4 py-2 text-sm">
							Sign Up
						</router-link>
					</template>
				</div>
			</div>
		</div>
	</nav>
</template>

<script setup>
	import { useAuthStore } from '../stores/auth';

	const authStore = useAuthStore();
</script>
