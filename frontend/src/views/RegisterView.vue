<template>
	<div
		class="min-h-[calc(100vh-200px)] flex items-center justify-center py-12">
		<div class="glass-card p-8 max-w-md w-full animate-slide-up">
			<div class="text-center mb-8">
				<h2 class="text-3xl font-bold text-gray-900 dark:text-white">
					Create Account
				</h2>
				<p class="text-gray-600 dark:text-gray-400 mt-2">
					Join our educational community
				</p>
			</div>

			<form
				@submit.prevent="handleRegister"
				class="space-y-5">
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
						>Name</label
					>
					<input
						type="text"
						v-model="form.name"
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
						v-model="form.surname"
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

				<div>
					<label
						class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
						>Confirm Password</label
					>
					<input
						type="password"
						v-model="form.passwordConfirm"
						class="input-field"
						:class="{ 'border-red-500': errors.passwordConfirm }"
						data-test="password-confirm-input" />
					<p
						v-if="errors.passwordConfirm"
						class="error-message"
						data-test="password-confirm-error">
						{{ errors.passwordConfirm }}
					</p>
				</div>

				<div
					v-if="formError"
					class="error-message text-center p-3 bg-red-50 dark:bg-red-900/30 rounded-lg"
					data-test="email-error">
					{{ formError }}
				</div>

				<button
					type="submit"
					:disabled="authStore.loading"
					class="btn-primary w-full">
					{{ authStore.loading ? 'Creating account...' : 'Sign Up' }}
				</button>
			</form>

			<p class="text-center mt-6 text-gray-600 dark:text-gray-400">
				Already have an account?
				<router-link
					to="/login"
					class="text-primary-500 hover:text-primary-600 font-semibold"
					>Sign In</router-link
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
		name: '',
		surname: '',
		password: '',
		passwordConfirm: '',
	});

	const errors = ref({
		email: '',
		name: '',
		surname: '',
		password: '',
		passwordConfirm: '',
	});

	const formError = ref('');

	const validateForm = () => {
		let isValid = true;
		errors.value = {
			email: '',
			name: '',
			surname: '',
			password: '',
			passwordConfirm: '',
		};

		if (!form.value.email) {
			errors.value.email = 'Заполните email';
			isValid = false;
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
			errors.value.email = 'Некорректный email';
			isValid = false;
		}

		if (!form.value.name) {
			errors.value.name = 'Заполните имя';
			isValid = false;
		}

		if (!form.value.surname) {
			errors.value.surname = 'Заполните фамилию';
			isValid = false;
		}

		if (!form.value.password) {
			errors.value.password = 'Заполните пароль';
			isValid = false;
		}

		if (!form.value.passwordConfirm) {
			errors.value.passwordConfirm = 'Повторите пароль';
			isValid = false;
		} else if (form.value.password !== form.value.passwordConfirm) {
			errors.value.passwordConfirm = 'Пароли не совпадают';
			isValid = false;
		}

		return isValid;
	};

	const handleRegister = async () => {
		if (!validateForm()) return;

		formError.value = '';
		const result = await authStore.register({
			email: form.value.email,
			name: form.value.name,
			surname: form.value.surname,
			password: form.value.password,
		});

		if (result.success) {
			router.push('/');
		} else if (result.error.includes('already exists')) {
			formError.value = 'Пользователь с таким email уже существует';
		} else {
			formError.value = result.error;
		}
	};
</script>
