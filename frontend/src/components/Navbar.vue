<template>
	<nav class="glass-card sticky top-4 mx-4 z-50">
		<div class="container mx-auto px-4 sm:px-6 py-3">
			<div class="flex items-center justify-between">
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
						class="text-xl font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
						Зов Знаний
					</span>
				</router-link>

				<div class="hidden sm:flex items-center space-x-4">
					<router-link
						to="/"
						class="text-gray-700 dark:text-gray-300 hover:text-primary-500 dark:hover:text-primary-500 transition-colors">
						Задания
					</router-link>

					<template v-if="authStore.isAuthenticated">
						<router-link
							v-if="authStore.isAuthor"
							to="/tasks/create"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors">
							Создать задание
						</router-link>
						<router-link
							v-if="authStore.isModerator"
							to="/moderation/tasks"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors">
							Модерация
						</router-link>
						<router-link
							v-if="authStore.isAdmin"
							to="/admin/users"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors">
							Управление пользователями
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
							Войти
						</router-link>
						<router-link
							to="/register"
							class="btn-primary px-4 py-2 text-sm">
							Зарегистрироваться
						</router-link>
					</template>
				</div>

				<!-- Бургер-меню для мобильных устройств -->
				<div class="sm:hidden flex items-center gap-2">
					<router-link
						v-if="authStore.isAuthenticated"
						to="/profile"
						class="flex items-center">
						<div
							class="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
							{{ authStore.user?.name?.charAt(0) || 'U' }}
						</div>
					</router-link>

					<!-- Кнопка бургер-меню -->
					<button
						@click="toggleMenu"
						class="text-gray-700 dark:text-gray-300 hover:text-primary-500 focus:outline-none">
						<svg
							v-if="!isMenuOpen"
							class="w-6 h-6"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M4 6h16M4 12h16M4 18h16" />
						</svg>
						<svg
							v-else
							class="w-6 h-6"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>
			</div>

			<!-- Мобильное меню (выпадающее) -->
			<div
				v-if="isMenuOpen"
				class="sm:hidden mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
				<div class="flex flex-col space-y-3">
					<router-link
						@click="closeMenu"
						to="/"
						class="text-gray-700 dark:text-gray-300 hover:text-primary-500 dark:hover:text-primary-500 transition-colors py-2">
						Задания
					</router-link>

					<template v-if="authStore.isAuthenticated">
						<router-link
							v-if="authStore.isAuthor"
							@click="closeMenu"
							to="/tasks/create"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors py-2">
							Создать задание
						</router-link>
						<router-link
							v-if="authStore.isModerator"
							@click="closeMenu"
							to="/moderation/tasks"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors py-2">
							Модерация
						</router-link>
						<router-link
							v-if="authStore.isAdmin"
							@click="closeMenu"
							to="/admin/users"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors py-2">
							Управление пользователями
						</router-link>
						<div class="pt-2 border-t border-gray-200 dark:border-gray-700">
							<button
								@click="handleLogout"
								class="w-full text-left text-red-500 hover:text-red-600 transition-colors py-2">
								Выйти
							</button>
						</div>
					</template>

					<template v-else>
						<router-link
							@click="closeMenu"
							to="/login"
							class="text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors py-2">
							Войти
						</router-link>
						<router-link
							@click="closeMenu"
							to="/register"
							class="btn-primary px-4 py-2 text-sm text-center">
							Зарегистрироваться
						</router-link>
					</template>
				</div>
			</div>
		</div>
	</nav>
</template>

<script setup>
	import { ref, watch } from 'vue';
	import { useRouter } from 'vue-router';
	import { useAuthStore } from '../stores/auth';

	const router = useRouter();
	const authStore = useAuthStore();
	const isMenuOpen = ref(false);

	const toggleMenu = () => {
		isMenuOpen.value = !isMenuOpen.value;
	};

	const closeMenu = () => {
		isMenuOpen.value = false;
	};

	const handleLogout = () => {
		authStore.logout();
		closeMenu();
		router.push('/login');
	};

	watch(
		() => router.currentRoute.value,
		() => {
			closeMenu();
		},
	);
</script>
