<template>
	<div class="max-w-4xl mx-auto space-y-8 animate-fade-in">
		<div class="glass-card p-8">
			<div class="flex justify-between items-start mb-8">
				<div>
					<h1 class="text-3xl font-bold text-gray-900 dark:text-white">
						Профиль
					</h1>
					<p class="text-gray-600 dark:text-gray-400 mt-1">
						Управление данными аккаунта
					</p>
				</div>
				<button
					@click="handleLogout"
					data-test="logout-button"
					class="btn-outline px-4 py-2 text-sm">
					Выйти
				</button>
			</div>

			<div class="space-y-6">
				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Имя
					</label>
					<div class="flex items-center gap-3">
						<span
							class="text-gray-900 dark:text-white"
							data-test="profile-name">
							{{ authStore.user?.name }}
						</span>
						<button
							@click="openEditModal('name')"
							class="text-primary-500 hover:text-primary-600 text-sm"
							data-test="name-edit">
							Редактировать
						</button>
					</div>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Фамилия
					</label>
					<div class="flex items-center gap-3">
						<span
							class="text-gray-900 dark:text-white"
							data-test="profile-surname">
							{{ authStore.user?.surname }}
						</span>
						<button
							@click="openEditModal('surname')"
							class="text-primary-500 hover:text-primary-600 text-sm"
							data-test="surname-edit">
							Редактировать
						</button>
					</div>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Email
					</label>
					<div class="flex items-center gap-3">
						<span
							class="text-gray-900 dark:text-white"
							data-test="profile-email">
							{{ authStore.user?.email }}
						</span>
						<button
							@click="openEditModal('email')"
							class="text-primary-500 hover:text-primary-600 text-sm"
							data-test="email-edit">
							Редактировать
						</button>
					</div>
				</div>

				<div v-if="authStore.isAuthor || authStore.isRegularUser">
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Адрес кошелька
					</label>
					<div class="flex items-center gap-3">
						<span
							class="text-gray-900 dark:text-white font-mono text-sm"
							data-test="profile-wallet">
							{{ authStore.isAuthor? authStore.user?.wallet || 'Не указан' : 'Доступно только для авторов' }}
						</span>
						<button
              v-if="authStore.isAuthor"
							@click="openEditModal('wallet')"
							class="text-primary-500 hover:text-primary-600 text-sm"
							data-test="wallet-edit">
							Редактировать
						</button>
					</div>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Пароль
					</label>
					<div class="flex items-center gap-3">
						<span class="text-gray-500 dark:text-gray-400"> •••••••• </span>
						<button
							@click="openEditModal('password')"
							class="text-primary-500 hover:text-primary-600 text-sm"
							data-test="password-edit">
							Изменить пароль
						</button>
					</div>
				</div>

				<div
					v-if="successMessage"
					class="success-message"
					data-test="success-message">
					{{ successMessage }}
				</div>

				<div
					v-if="formError"
					class="error-message"
					data-test="form-error">
					{{ formError }}
				</div>
			</div>

			<div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
					<div>
						<span class="text-gray-500 dark:text-gray-400">Роль:</span>
						<span
							class="ml-2 font-semibold px-2 py-1 rounded text-xs"
							:class="roleClass"
							data-test="profile-role">
							{{ formattedRole }}
						</span>
					</div>
					<div
						v-if="
							!authStore.isAuthor &&
							!authStore.isModerator &&
							!authStore.isAdmin
						">
						<span class="text-gray-500 dark:text-gray-400">Подписка:</span>
						<span
							class="ml-2 font-medium"
							data-test="profile-subscription">
							{{ subscriptionStatus }}
						</span>
					</div>
				</div>

				<div class="flex gap-4 mt-6">
					<button
						v-if="
							!authStore.isAuthor &&
							!authStore.isModerator &&
							!authStore.isAdmin
						"
						@click="applyForAuthor"
						:disabled="applyingForAuthor"
						class="btn-secondary px-4 py-2 text-sm">
						{{ applyingForAuthor ? 'Отправка...' : 'Стать автором' }}
					</button>

					<button
						v-if="
							!authStore.isAuthor &&
							!authStore.isModerator &&
							!authStore.isAdmin &&
							!hasActiveSubscription
						"
						@click="subscribe"
						:disabled="subscribing"
						class="btn-primary px-4 py-2 text-sm">
						{{ subscribing ? 'Обработка...' : 'Оформить подписку' }}
					</button>

					<button
						@click="showDeleteModal = true"
						class="btn-outline px-4 py-2 text-sm text-red-500 border-red-500 hover:bg-red-50 dark:hover:bg-red-900/30"
						data-test="delete-button">
						Удалить аккаунт
					</button>
				</div>
			</div>
		</div>

		<div
			v-if="editModal.visible"
			class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in"
			@click.self="closeEditModal">
			<div class="glass-card p-6 max-w-md w-full mx-4">
				<h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">
					Редактировать {{ editModal.label }}
				</h3>

				<div class="space-y-4">
					<input
						:type="editModal.field === 'password' ? 'password' : 'text'"
						v-model="editModal.value"
						class="input-field"
						:placeholder="editModal.placeholder"
						:data-test="`${editModal.field}-input`"
						@keyup.enter="saveEditModal" />

					<p
						v-if="editModal.error"
						class="error-message"
						:data-test="`${editModal.field}-error`">
						{{ editModal.error }}
					</p>
				</div>

				<div class="flex gap-4 justify-end mt-6">
					<button
						@click="closeEditModal"
						class="btn-outline px-4 py-2">
						Отменить
					</button>
					<button
						v-if="hasFieldChanged"
						@click="saveEditModal"
						:disabled="editModal.saving"
						class="btn-primary px-4 py-2"
						data-test="save-button">
						{{ editModal.saving ? 'Сохранение...' : 'Сохранить' }}
					</button>
				</div>
			</div>
		</div>

		<div
			v-if="showDeleteModal"
			class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in"
			@click.self="showDeleteModal = false">
			<div class="glass-card p-6 max-w-md w-full mx-4">
				<h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">
					Удалить аккаунт
				</h3>
				<p class="text-gray-600 dark:text-gray-400 mb-6">
					Вы уверены, что хотите удалить свой аккаунт? Это действие нельзя
					отменить.
				</p>
				<div class="flex gap-4 justify-end">
					<button
						@click="showDeleteModal = false"
						class="btn-outline px-4 py-2">
						Отменить
					</button>
					<button
						@click="confirmDelete"
						:disabled="deleting"
						class="btn-primary px-4 py-2 bg-red-500 hover:bg-red-600"
						data-test="confirm-delete">
						{{ deleting ? 'Удаление...' : 'Удалить' }}
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, computed, onMounted } from 'vue';
	import { useRouter } from 'vue-router';
	import { useAuthStore } from '../stores/auth';

	const router = useRouter();
	const authStore = useAuthStore();

	const editModal = ref({
		visible: false,
		field: '',
		label: '',
		value: '',
		originalValue: '',
		placeholder: '',
		saving: false,
		error: '',
	});

	const successMessage = ref('');
	const formError = ref('');
	const showDeleteModal = ref(false);
	const deleting = ref(false);
	const applyingForAuthor = ref(false);
	const subscribing = ref(false);

	const hasFieldChanged = computed(() => {
		if (editModal.value.field === 'password') {
			return editModal.value.value && editModal.value.value.length > 0;
		}
		return editModal.value.value !== editModal.value.originalValue;
	});

	const hasActiveSubscription = computed(() => {
		if (!authStore.user?.subscribed_until_date) return false;
		return new Date(authStore.user.subscribed_until_date) > new Date();
	});

	const subscriptionStatus = computed(() => {
		if (!authStore.user?.subscribed_until_date) {
			return 'Нет активной подписки';
		}
		const expiryDate = new Date(authStore.user.subscribed_until_date);
		if (expiryDate > new Date()) {
			return `Активна до ${expiryDate.toLocaleDateString('ru-RU')}`;
		}
		return 'Закончилась';
	});

	const formattedRole = computed(() => {
		const role = authStore.user?.role_name;
		const roleMap = {
			user: 'Ученик',
			student: 'Ученик',
			author: 'Автор',
			moderator: 'Модератор',
			admin: 'Администратор',
		};
		return roleMap[role] || role || 'Ученик';
	});

	const roleClass = computed(() => {
		const role = authStore.user?.role_name;
		const classMap = {
			user: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
			student: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
			author:
				'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
			moderator:
				'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
			admin: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
		};
		return classMap[role] || classMap['user'];
	});

	const validateField = (field, value) => {
		switch (field) {
			case 'name':
				if (!value || !value.trim()) return 'Заполните имя';
				return '';
			case 'surname':
				if (!value || !value.trim()) return 'Заполните фамилию';
				return '';
			case 'email':
				if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
					return 'Некорректный email';
				}
				return '';
			case 'password':
				if (value && value.length < 6)
					return 'Пароль должен содержать не менее 6 символов';
				return '';
			default:
				return '';
		}
	};

	const openEditModal = (field) => {
		let label = '';
		let value = '';
		let placeholder = '';

		switch (field) {
			case 'name':
				label = 'имя';
				value = authStore.user?.name || '';
				placeholder = 'Введите имя';
				break;
			case 'surname':
				label = 'фамилию';
				value = authStore.user?.surname || '';
				placeholder = 'Введите фамилию';
				break;
			case 'email':
				label = 'email';
				value = authStore.user?.email || '';
				placeholder = 'Введите email';
				break;
			case 'wallet':
				label = 'адрес кошелька';
				value = authStore.user?.wallet || '';
				placeholder = 'Введите адрес кошелька';
				break;
			case 'password':
				label = 'пароль';
				value = '';
				placeholder = 'Введите новый пароль';
				break;
		}

		editModal.value = {
			visible: true,
			field,
			label,
			value,
			originalValue: value,
			placeholder,
			saving: false,
			error: '',
		};
	};

	const closeEditModal = () => {
		editModal.value.visible = false;
		editModal.value.error = '';
	};

	const saveEditModal = async () => {
		const error = validateField(editModal.value.field, editModal.value.value);
		if (error) {
			editModal.value.error = error;
			return;
		}

		if (
			editModal.value.value === editModal.value.originalValue &&
			editModal.value.field !== 'password'
		) {
			closeEditModal();
			return;
		}

		editModal.value.saving = true;
		editModal.value.error = '';
		formError.value = '';
		successMessage.value = '';

		const updateData = {};

		switch (editModal.value.field) {
			case 'name':
				if (editModal.value.value !== editModal.value.originalValue) {
					updateData.name = editModal.value.value;
				}
				break;
			case 'surname':
				if (editModal.value.value !== editModal.value.originalValue) {
					updateData.surname = editModal.value.value;
				}
				break;
			case 'email':
				if (editModal.value.value !== editModal.value.originalValue) {
					updateData.email = editModal.value.value;
				}
				break;
			case 'wallet':
				if (editModal.value.value !== editModal.value.originalValue) {
					updateData.wallet = editModal.value.value;
				}
				break;
			case 'password':
				if (editModal.value.value) {
					updateData.password = editModal.value.value;
				}
				break;
		}

		if (Object.keys(updateData).length === 0) {
			closeEditModal();
			editModal.value.saving = false;
			return;
		}

		const result = await authStore.updateUser(updateData);

		if (result.success) {
			successMessage.value = 'Данные обновлены';
			closeEditModal();
			setTimeout(() => {
				successMessage.value = '';
			}, 3000);
		} else {
			editModal.value.error = result.error || 'Ошибка при обновлении данных';
		}

		editModal.value.saving = false;
	};

	const handleLogout = () => {
		authStore.logout();
		router.push('/login');
	};

	const applyForAuthor = async () => {
		applyingForAuthor.value = true;
		const result = await authStore.applyForAuthor();
		if (result.success) {
			successMessage.value = 'Заявка успешно отправлена!';
			setTimeout(() => {
				successMessage.value = '';
			}, 3000);
		} else {
			formError.value = result.error || 'Не удалось отправить заявку';
			setTimeout(() => {
				formError.value = '';
			}, 3000);
		}
		applyingForAuthor.value = false;
	};

	const subscribe = async () => {
		subscribing.value = true;
		const result = await authStore.subscribe();
		if (result.success) {
			successMessage.value = 'Вы успешно подписались!';
			setTimeout(() => {
				successMessage.value = '';
			}, 3000);
		} else {
			formError.value = result.error || 'Не удалось подписаться';
			setTimeout(() => {
				formError.value = '';
			}, 3000);
		}
		subscribing.value = false;
	};

	const confirmDelete = async () => {
		deleting.value = true;
		const result = await authStore.deleteAccount();
		if (result.success) {
			router.push('/login');
		} else {
			formError.value = result.error || 'Не удалось удалить аккаунт';
			showDeleteModal.value = false;
			setTimeout(() => {
				formError.value = '';
			}, 3000);
		}
		deleting.value = false;
	};

	onMounted(async () => {
		await authStore.fetchUser();
	});
</script>
