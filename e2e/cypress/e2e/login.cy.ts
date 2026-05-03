describe('login page', () => {
  context('Client-side validation', () => {
    it('redirects to main on success', () => {
      const email = 'test_login@example.ru';
      const password = 'test-password';

      cy.registerUser({ email, password, passwordConfirm: password });

      cy.loginUser({ email, password });

      cy.location('pathname').should('eq', '/');
      cy.window().then((win) => {
        expect(win.localStorage.getItem('access_token')).to.exist;
      });
    });

    it('should show email validation error', () => {
      cy.loginUser({ email: 'incorrect_email' });
      cy.errorShouldBeVisible('email-error', 'Некорректный email');
    });

    it('should show empty email validation error', () => {
      cy.loginUser({ email: null });
      cy.errorShouldBeVisible('email-error', 'Заполните email');
    });

    it('should show empty password validation error', () => {
      cy.loginUser({ password: null });
      cy.errorShouldBeVisible('password-error', 'Заполните пароль');
    });
  });

  context('Server-side validation', () => {
    it('should show error on wrong credentials', () => {
      cy.loginUser({
        email: 'not_existing@example.ru',
        password: 'wrong-password',
      });

      cy.errorShouldBeVisible(
        'form-error',
        'Неверное имя пользователя или пароль'
      );
    });
  });
});