describe('register page', () => {
  context('Client-side validation', () => {
    beforeEach(() => {
      cy.resetDB();
    });

    it('redirects to main on success', () => {
      cy.registerUser({});
      cy.location('pathname').should('eq', '/');
      cy.window().then((win) => {
        expect(win.localStorage.getItem('access_token')).to.exist;
      });
    });

    it('should show email validation error', () => {
      cy.registerUser({ email: 'incorrect_email', shouldFail: true });
      cy.errorShouldBeVisible('email-error', 'Некорректный email');
    });

    it('should show empty email validation error', () => {
      cy.registerUser({ email: undefined, shouldFail: true });
      cy.errorShouldBeVisible('email-error', 'Заполните email');
    });

    it('should show empty name validation error', () => {
      cy.registerUser({ name: undefined, shouldFail: true });
      cy.errorShouldBeVisible('name-error', 'Заполните имя');
    });

    it('should show empty surname validation error', () => {
      cy.registerUser({ surname: undefined, shouldFail: true });
      cy.errorShouldBeVisible('surname-error', 'Заполните фамилию');
    });

    it('should show empty password validation error', () => {
      cy.registerUser({ password: undefined, shouldFail: true });
      cy.errorShouldBeVisible('password-error', 'Заполните пароль');
    });

    it('should show empty confirm password validation error', () => {
      cy.registerUser({ passwordConfirm: undefined, shouldFail: true });
      cy.errorShouldBeVisible('password-confirm-error', 'Повторите пароль');
    });

    it('shows error when password and its confirmation do not match', () => {
      cy.registerUser({ passwordConfirm: 'AnotherPassword', shouldFail: true });
      cy.errorShouldBeVisible('password-confirm-error', 'Пароли не совпадают');
    });
  });

  context('Server-side validation', () => {
    beforeEach(() => {
      cy.resetDB();
    });

    it('registers new user and modifies the DB', () => {
      const email = 'test@email.ru'
      cy.registerUser({ email, shouldSuccessBeStubbed: false });
      cy.getUserByEmail(email).then((user) => {
        expect(user).to.not.be.null;
        expect(user.email).to.equal(email);
      });
    });

    it('should not let register two users with same email', () => {
      const email = 'test1@email.ru';

      cy.registerUser({ email, shouldSuccessBeStubbed: false });
      
      cy.getUserByEmail(email).then((user) => {
        expect(user).to.not.be.null;
        expect(user.email).to.equal(email);
      });

      cy.registerUser({ email, shouldSuccessBeStubbed: false });
      cy.errorShouldBeVisible('email-error', 'Пользователь с таким email уже существует');
    });
  });
});