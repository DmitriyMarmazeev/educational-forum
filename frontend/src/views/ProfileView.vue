<!-- frontend/src/views/ProfileView.vue -->
<template>
	<div class="max-w-4xl mx-auto space-y-8 animate-fade-in">
		<div class="glass-card p-8">
			<div class="flex justify-between items-start mb-8">
				<div>
					<h1 class="text-3xl font-bold text-gray-900 dark:text-white">
						Profile
					</h1>
					<p class="text-gray-600 dark:text-gray-400 mt-1">
						Manage your account settings
					</p>
				</div>
				<button
					@click="handleLogout"
					data-test="logout-button"
					class="btn-outline px-4 py-2 text-sm">
					Logout
				</button>
			</div>

			<div class="space-y-6">
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<div>
						<label
							class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
							>Name</label
						>
						<input
							type="text"
							v-model="editForm.name"
							class="input-field"
							:class="{ 'border-red-500': errors.name }"
							data-test="name-input" />
						<p
							v-if="errors.name"
							class="error-message"
							data-test="name-error">
							{{ errors.name }}
						</p>
					</div>

					<div>
						<label
							class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
							>Surname</label
						>
						<input
							type="text"
							v-model="editForm.surname"
							class="input-field"
							:class="{ 'border-red-500': errors.surname }"
							data-test="surname-input" />
						<p
							v-if="errors.surname"
							class="error-message"
							data-test="surname-error">
							{{ errors.surname }}
						</p>
					</div>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Email</label
					>
					<input
						type="email"
						v-model="editForm.email"
						class="input-field"
						:class="{ 'border-red-500': errors.email }"
						data-test="email-input" />
					<p
						v-if="errors.email"
						class="error-message"
						data-test="email-error">
						{{ errors.email }}
					</p>
				</div>

				<!-- Поле для кошелька - показываем только для автора -->
				<div v-if="authStore.isAuthor">
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Wallet Address</label
					>
					<input
						type="text"
						v-model="editForm.wallet"
						class="input-field"
						placeholder="Enter your wallet address (e.g., 0x... or bank account)"
						data-test="wallet-input" />
					<p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
						Your wallet address for receiving payments
					</p>
				</div>

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>New Password</label
					>
					<input
						type="password"
						v-model="editForm.password"
						class="input-field"
						placeholder="Leave blank to keep current"
						data-test="password-input" />
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

				<div class="flex justify-end">
					<button
						v-if="hasChanges"
						@click="saveChanges"
						:disabled="saving"
						class="btn-primary"
						data-test="save-button">
						{{ saving ? 'Saving...' : 'Save Changes' }}
					</button>
				</div>
			</div>

			<div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
					<div>
						<span class="text-gray-500 dark:text-gray-400">Email:</span>
						<span
							class="ml-2 font-medium"
							data-test="profile-email"
							>{{ authStore.user?.email }}</span
						>
					</div>
					<div>
						<span class="text-gray-500 dark:text-gray-400">Name:</span>
						<span
							class="ml-2 font-medium"
							data-test="profile-name"
							>{{ authStore.user?.name }} {{ authStore.user?.surname }}</span
						>
					</div>
					<!-- Кошелек отображаем только для автора -->
					<div v-if="authStore.isAuthor">
						<span class="text-gray-500 dark:text-gray-400">Wallet:</span>
						<span
							class="ml-2 font-mono text-sm"
							data-test="profile-wallet"
							>{{ authStore.user?.wallet || 'Not set' }}</span
						>
					</div>
					<div>
						<span class="text-gray-500 dark:text-gray-400">Role:</span>
						<span
							class="ml-2 font-semibold px-2 py-1 rounded text-xs"
							:class="roleClass"
							data-test="profile-role">
							{{ formattedRole }}
						</span>
					</div>
					<!-- Статус подписки отображаем только для обычных пользователей (не author, не moderator, не admin) -->
					<div
						v-if="
							!authStore.isAuthor &&
							!authStore.isModerator &&
							!authStore.isAdmin
						">
						<span class="text-gray-500 dark:text-gray-400">Subscription:</span>
						<span
							class="ml-2 font-medium"
							data-test="profile-subscription">
							{{ subscriptionStatus }}
						</span>
					</div>
				</div>

				<div class="flex gap-4 mt-6">
					<!-- Кнопка "Apply for Author" - показываем только если пользователь не author, не moderator и не admin -->
					<button
						v-if="
							!authStore.isAuthor &&
							!authStore.isModerator &&
							!authStore.isAdmin
						"
						@click="applyForAuthor"
						:disabled="applyingForAuthor"
						class="btn-secondary px-4 py-2 text-sm">
						{{ applyingForAuthor ? 'Applying...' : 'Apply for Author' }}
					</button>

					<!-- Кнопка подписки - показываем только для обычных пользователей без активной подписки -->
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
						{{ subscribing ? 'Processing...' : 'Subscribe Now' }}
					</button>

					<button
						@click="showDeleteModal = true"
						class="btn-outline px-4 py-2 text-sm text-red-500 border-red-500 hover:bg-red-50 dark:hover:bg-red-900/30">
						Delete Account
					</button>
				</div>
			</div>
		</div>

		<!-- Модальное окно подтверждения удаления -->
		<div
			v-if="showDeleteModal"
			class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fade-in"
			@click.self="showDeleteModal = false">
			<div class="glass-card p-6 max-w-md w-full mx-4">
				<h3 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">
					Delete Account
				</h3>
				<p class="text-gray-600 dark:text-gray-400 mb-6">
					Are you sure you want to delete your account? This action cannot be
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
						:disabled="deleting"
						class="btn-primary px-4 py-2 bg-red-500 hover:bg-red-600">
						{{ deleting ? 'Deleting...' : 'Delete' }}
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

	const editForm = ref({
		name: '',
		surname: '',
		email: '',
		wallet: '',
		password: '',
	});

	const originalData = ref({});
	const errors = ref({ name: '', surname: '', email: '' });
	const successMessage = ref('');
	const formError = ref('');
	const showDeleteModal = ref(false);
	const saving = ref(false);
	const deleting = ref(false);
	const applyingForAuthor = ref(false);
	const subscribing = ref(false);

	// Вычисляемые свойства
	const hasChanges = computed(() => {
		return (
			editForm.value.name !== originalData.value.name ||
			editForm.value.surname !== originalData.value.surname ||
			editForm.value.email !== originalData.value.email ||
			editForm.value.wallet !== originalData.value.wallet ||
			editForm.value.password
		);
	});

	const hasActiveSubscription = computed(() => {
		if (!authStore.user?.subscribed_until_date) return false;
		return new Date(authStore.user.subscribed_until_date) > new Date();
	});

	const subscriptionStatus = computed(() => {
		if (!authStore.user?.subscribed_until_date) {
			return 'No active subscription';
		}
		const expiryDate = new Date(authStore.user.subscribed_until_date);
		if (expiryDate > new Date()) {
			return `Active until ${expiryDate.toLocaleDateString('ru-RU')}`;
		}
		return 'Expired';
	});

	const formattedRole = computed(() => {
		const role = authStore.user?.role_name;
		const roleMap = {
			user: 'User',
			author: 'Author',
			moderator: 'Moderator',
			admin: 'Administrator',
		};
		return roleMap[role] || role || 'User';
	});

	const roleClass = computed(() => {
		const role = authStore.user?.role_name;
		const classMap = {
			user: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
			author:
				'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
			moderator:
				'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
			admin: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
		};
		return classMap[role] || classMap['user'];
	});

	// Методы
	const validateForm = () => {
		let isValid = true;
		errors.value = { name: '', surname: '', email: '' };

		if (!editForm.value.name || !editForm.value.name.trim()) {
			errors.value.name = 'Заполните имя';
			isValid = false;
		}

		if (!editForm.value.surname || !editForm.value.surname.trim()) {
			errors.value.surname = 'Заполните фамилию';
			isValid = false;
		}

		if (
			editForm.value.email &&
			!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(editForm.value.email)
		) {
			errors.value.email = 'Некорректный email';
			isValid = false;
		}

		return isValid;
	};

	const saveChanges = async () => {
		if (!validateForm()) return;

		saving.value = true;
		formError.value = '';
		successMessage.value = '';

		const updateData = {};
		if (editForm.value.name !== originalData.value.name)
			updateData.name = editForm.value.name;
		if (editForm.value.surname !== originalData.value.surname)
			updateData.surname = editForm.value.surname;
		if (editForm.value.email !== originalData.value.email)
			updateData.email = editForm.value.email;
		if (editForm.value.wallet !== originalData.value.wallet)
			updateData.wallet = editForm.value.wallet;
		if (editForm.value.password) updateData.password = editForm.value.password;

		if (Object.keys(updateData).length === 0) {
			saving.value = false;
			return;
		}

		const result = await authStore.updateUser(updateData);

		if (result.success) {
			originalData.value = { ...editForm.value };
			successMessage.value = 'Данные обновлены';
			setTimeout(() => {
				successMessage.value = '';
			}, 3000);
		} else {
			formError.value = result.error || 'Ошибка при обновлении данных';
		}

		saving.value = false;
	};

	const handleLogout = () => {
		authStore.logout();
		router.push('/login');
	};

	const applyForAuthor = async () => {
		applyingForAuthor.value = true;
		const result = await authStore.applyForAuthor();
		if (result.success) {
			successMessage.value = 'Application submitted successfully!';
			setTimeout(() => {
				successMessage.value = '';
			}, 3000);
		} else {
			formError.value = result.error || 'Failed to submit application';
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
			successMessage.value = 'Successfully subscribed!';
			setTimeout(() => {
				successMessage.value = '';
			}, 3000);
		} else {
			formError.value = result.error || 'Failed to subscribe';
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
			formError.value = result.error || 'Failed to delete account';
			showDeleteModal.value = false;
			setTimeout(() => {
				formError.value = '';
			}, 3000);
		}
		deleting.value = false;
	};

	onMounted(async () => {
		await authStore.fetchUser();
		if (authStore.user) {
			editForm.value = {
				name: authStore.user.name || '',
				surname: authStore.user.surname || '',
				email: authStore.user.email || '',
				wallet: authStore.user.wallet || '',
				password: '',
			};
			originalData.value = { ...editForm.value };
		}
	});
</script>
