import { createRouter, createWebHistory } from 'vue-router';

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
		meta: { requiresAuth: true, title: 'Edit Task' },
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
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

router.beforeEach((to, from, next) => {
	const token = localStorage.getItem('access_token');
	const isAuthenticated = !!token;

	if (to.meta.requiresAuth && !isAuthenticated) {
		next('/login');
	} else if (to.meta.guestOnly && isAuthenticated) {
		next('/');
	} else {
		document.title = `${to.meta.title || 'Educational Forum'} | Educational Forum`;
		next();
	}
});

export default router;
