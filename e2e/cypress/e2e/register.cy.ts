describe('register page', () => {
  context('Client-side validation', () => {
    it('redirects to main on success', () => {
      cy.registerUser({});
      cy.location('pathname').should('eq', '/');
      cy.window().then((win) => {
        expect(win.localStorage.getItem('access_token')).to.exist;
      });
    });

    it('should show email validation error', () => {
      cy.registerUser({ email: 'incorrect_email' });
      cy.errorShouldBeVisible('email-error', 'Некорректный email');
    });

    it('should show empty email validation error', () => {
      cy.registerUser({ email: null });
      cy.errorShouldBeVisible('email-error', 'Заполните email');
    });

    it('should show empty name validation error', () => {
      cy.registerUser({ name: null });
      cy.errorShouldBeVisible('name-error', 'Заполните имя');
    });

    it('should show empty surname validation error', () => {
      cy.registerUser({ surname: null });
      cy.errorShouldBeVisible('surname-error', 'Заполните фамилию');
    });

    it('should show empty password validation error', () => {
      cy.registerUser({ password: null });
      cy.errorShouldBeVisible('password-error', 'Заполните пароль');
    });

    it('should show empty confirm password validation error', () => {
      cy.registerUser({ passwordConfirm: null });
      cy.errorShouldBeVisible('password-confirm-error', 'Повторите пароль');
    });

    it('shows error when password and its confirmation do not match', () => {
      cy.registerUser({ passwordConfirm: 'AnotherPassword' });
      cy.errorShouldBeVisible('password-confirm-error', 'Пароли не совпадают');
    });
  });

  context('Server-side validation', () => {
    it('should not let register two users with same email', () => {
      const email = 'test1@email.ru';

      cy.registerUser({ email });
      cy.registerUser({ email });

      cy.errorShouldBeVisible('email-error', 'Пользователь с таким email уже существует');
    });
  });
});