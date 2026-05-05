<template>
	<div class="space-y-6 animate-fade-in">
		<div class="glass-card p-6">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
				User Management
			</h1>
			<p class="text-gray-600 dark:text-gray-400">
				Manage user roles and permissions
			</p>
		</div>

		<div class="glass-card p-6">
			<div
				v-if="loading"
				class="flex justify-center py-8">
				<div
					class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
			</div>

			<div
				v-else
				class="overflow-x-auto">
				<table class="w-full">
					<thead>
						<tr class="border-b border-gray-200 dark:border-gray-700">
							<th class="text-left py-3 px-4">ID</th>
							<th class="text-left py-3 px-4">Name</th>
							<th class="text-left py-3 px-4">Email</th>
							<th class="text-left py-3 px-4">Role</th>
							<th class="text-left py-3 px-4">Actions</th>
						</tr>
					</thead>
					<tbody>
						<tr
							v-for="user in users"
							:key="user.id_user"
							class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50">
							<td class="py-3 px-4">{{ user.id_user }}</td>
							<td class="py-3 px-4">{{ user.name }} {{ user.surname }}</td>
							<td class="py-3 px-4">{{ user.email }}</td>
							<td class="py-3 px-4">
								<span
									class="text-xs font-semibold px-2 py-1 rounded"
									:class="roleClass(user.role_name)">
									{{ user.role_name }}
								</span>
							</td>
							<td class="py-3 px-4">
								<select
									v-model="user.newRole"
									@change="changeRole(user)"
									class="input-field text-sm py-1 w-32">
									<option value="user">User</option>
									<option value="author">Author</option>
									<option value="moderator">Moderator</option>
									<option value="admin">Admin</option>
								</select>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { adminApi } from '../api';

	const users = ref([]);
	const loading = ref(false);

	const roleClass = (role) => {
		const classes = {
			user: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
			author:
				'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
			moderator:
				'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
			admin: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
		};
		return classes[role] || classes.user;
	};

	const loadUsers = async () => {
		loading.value = true;
		try {
			const response = await adminApi.listAllUsers();
			users.value = response.data.map((u) => ({ ...u, newRole: u.role_name }));
		} catch (error) {
			console.error('Failed to load users', error);
		} finally {
			loading.value = false;
		}
	};

	const changeRole = async (user) => {
		if (user.newRole === user.role_name) return;
		try {
			await adminApi.changeUserRole(user.id_user, user.newRole);
			user.role_name = user.newRole;
		} catch (error) {
			user.newRole = user.role_name;
			console.error('Failed to change role', error);
		}
	};

	onMounted(() => {
		loadUsers();
	});
</script>
