import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useTasksStore } from '../stores/tasks';

const routes = [
	{
		path: '/',
		name: 'Home',
		component: () => import('../views/HomeView.vue'),
		meta: { requiresAuth: false, title: 'Home' },
	},
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/LoginView.vue'),
		meta: { requiresAuth: false, guestOnly: true, title: 'Login' },
	},
	{
		path: '/register',
		name: 'Register',
		component: () => import('../views/RegisterView.vue'),
		meta: { requiresAuth: false, guestOnly: true, title: 'Register' },
	},
	{
		path: '/profile',
		name: 'Profile',
		component: () => import('../views/ProfileView.vue'),
		meta: { requiresAuth: true, title: 'Profile' },
	},
	{
		path: '/tasks/:id',
		name: 'TaskDetail',
		component: () => import('../views/TaskDetailView.vue'),
		meta: { requiresAuth: false, title: 'Task' },
	},
	{
		path: '/tasks/create',
		name: 'CreateTask',
		component: () => import('../views/CreateTaskView.vue'),
		meta: { requiresAuth: true, requiresAuthor: true, title: 'Create Task' },
	},
	{
		path: '/tasks/:id/edit',
		name: 'EditTask',
		component: () => import('../views/EditTaskView.vue'),
		meta: { requiresAuth: true, requiresOwner: true, title: 'Edit Task' },
	},
	{
		path: '/moderation/tasks',
		name: 'ModerationTasks',
		component: () => import('../views/ModerationTasksView.vue'),
		meta: {
			requiresAuth: true,
			requiresModerator: true,
			title: 'Task Moderation',
		},
	},
	{
		path: '/moderation/comments',
		name: 'ModerationComments',
		component: () => import('../views/ModerationCommentsView.vue'),
		meta: {
			requiresAuth: true,
			requiresModerator: true,
			title: 'Comment Moderation',
		},
	},
	{
		path: '/admin/users',
		name: 'AdminUsers',
		component: () => import('../views/AdminUsersView.vue'),
		meta: {
			requiresAuth: true,
			requiresAdmin: true,
			title: 'User Management',
		},
	},
	{
		path: '/404',
		name: 'NotFound',
		component: () => import('../views/NotFoundView.vue'),
		meta: { title: 'Страница не найдена' },
	},
	{
		path: '/:pathMatch(.*)*',
		redirect: '/404',
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

router.beforeEach(async (to, from, next) => {
	const token = localStorage.getItem('access_token');
	const isAuthenticated = !!token;
	const authStore = useAuthStore();

	if (isAuthenticated && !authStore.user) {
		await authStore.fetchUser();
	}

	if (to.meta.guestOnly && isAuthenticated) {
		next('/');
		return;
	}

	if (to.meta.requiresAuth && !isAuthenticated) {
		next('/login');
		return;
	}

	if (to.meta.requiresAuthor && isAuthenticated) {
		if (!authStore.isAuthor && !authStore.isModerator && !authStore.isAdmin) {
			next('/404');
			return;
		}
	}

	if (to.meta.requiresModerator && isAuthenticated) {
		if (!authStore.isModerator && !authStore.isAdmin) {
			next('/404');
			return;
		}
	}

	if (to.meta.requiresAdmin && isAuthenticated) {
		if (!authStore.isAdmin) {
			next('/404');
			return;
		}
	}

	if (to.meta.requiresOwner && isAuthenticated && authStore.user) {
		const taskId = to.params.id;
		if (taskId) {
			const tasksStore = useTasksStore();
			try {
				const result = await tasksStore.fetchTask(taskId);
				if (result.success && result.data) {
					const isOwner = authStore.user.id_user === result.data.author_id;
					if (!isOwner) {
						next('/404');
						return;
					}
				} else {
					next('/404');
					return;
				}
			} catch (error) {
				next('/404');
				return;
			}
		}
	}

	document.title = `${to.meta.title || 'Образовательный форум'} | Зов Знаний`;
	next();
});

export default router;
