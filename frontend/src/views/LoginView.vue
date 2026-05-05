<template>
	<div
		class="min-h-[calc(100vh-200px)] flex items-center justify-center py-12">
		<div class="glass-card p-8 max-w-md w-full animate-slide-up">
			<div class="text-center mb-8">
				<h2 class="text-3xl font-bold text-gray-900 dark:text-white">
					Welcome Back
				</h2>
				<p class="text-gray-600 dark:text-gray-400 mt-2">
					Sign in to your account
				</p>
			</div>

			<form
				@submit.prevent="handleLogin"
				class="space-y-6">
				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Email</label
					>
					<input
						type="email"
						v-model="form.email"
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

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Password</label
					>
					<input
						type="password"
						v-model="form.password"
						class="input-field"
						:class="{ 'border-red-500': errors.password }"
						data-test="password-input" />
					<p
						v-if="errors.password"
						class="error-message"
						data-test="password-error">
						{{ errors.password }}
					</p>
				</div>

				<div
					v-if="formError"
					class="error-message text-center p-3 bg-red-50 dark:bg-red-900/30 rounded-lg"
					data-test="form-error">
					{{ formError }}
				</div>

				<button
					type="submit"
					:disabled="authStore.loading"
					class="btn-primary w-full">
					{{ authStore.loading ? 'Signing in...' : 'Sign In' }}
				</button>
			</form>

			<p class="text-center mt-6 text-gray-600 dark:text-gray-400">
				Don't have an account?
				<router-link
					to="/register"
					class="text-primary-500 hover:text-primary-600 font-semibold"
					>Sign Up</router-link
				>
			</p>
		</div>
	</div>
</template>

<script setup>
	import { ref } from 'vue';
	import { useRouter } from 'vue-router';
	import { useAuthStore } from '../stores/auth';

	const router = useRouter();
	const authStore = useAuthStore();

	const form = ref({
		email: '',
		password: '',
	});

	const errors = ref({
		email: '',
		password: '',
	});

	const formError = ref('');

	const validateForm = () => {
		let isValid = true;
		errors.value = { email: '', password: '' };

		if (!form.value.email) {
			errors.value.email = 'Заполните email';
			isValid = false;
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
			errors.value.email = 'Некорректный email';
			isValid = false;
		}

		if (!form.value.password) {
			errors.value.password = 'Заполните пароль';
			isValid = false;
		}

		return isValid;
	};

	const handleLogin = async () => {
		if (!validateForm()) return;

		formError.value = '';
		const result = await authStore.login({
			email: form.value.email,
			password: form.value.password,
		});

		if (result.success) {
			router.push('/');
		} else {
			if (result.error === 'Invalid email or password') {
				formError.value = 'Неверное имя пользователя или пароль';
			} else {
				formError.value = result.error;
			}
		}
	};
</script>
