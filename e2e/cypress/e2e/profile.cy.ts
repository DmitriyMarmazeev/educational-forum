describe('profile page', () => {
  const user = {
    email: `test_${Date.now()}@example.ru`,
    name: 'test-name',
    surname: 'test-surname',
    password: 'test-password',
  };

  beforeEach(() => {
    cy.registerUser({
      email: user.email,
      name: user.name,
      surname: user.surname,
      password: user.password,
      passwordConfirm: user.password,
    });

    cy.visit('/profile');
  });

  context('Access', () => {
    it('redirects to login if not authorized', () => {
      cy.clearLocalStorage();
      cy.visit('/profile');

      cy.location('pathname').should('eq', '/login');
    });
  });

  context('Display user data', () => {
    it('should display user data', () => {
      cy.getByData('profile-email').should('contain', user.email);
      cy.getByData('profile-name').should('contain', user.name);
      cy.getByData('profile-surname').should('contain', user.surname);

      cy.getByData('profile-wallet').should('exist');
      cy.getByData('profile-role').should('exist');
      cy.getByData('profile-subscription').should('exist');
    });
  });

  context('Edit profile', () => {
    it('should allow editing name and save changes', () => {
      const newName = 'updated-name';

      cy.editField('name', newName);
      cy.getByData('save-button').should('be.visible').click();

      cy.getByData('profile-name').should('contain', newName);
      cy.getByData('success-message')
        .should('be.visible')
        .should('contain', 'Данные обновлены');
    });

    it('should show validation error for empty name', () => {
      cy.editField('name', '');
      cy.getByData('save-button').click();

      cy.errorShouldBeVisible('name-error', 'Заполните имя');
    });

    it('should allow updating surname', () => {
      const newSurname = 'updated-surname';

      cy.editField('surname', newSurname);
      cy.getByData('save-button').should('be.visible').click();

      cy.getByData('profile-surname').should('contain', newSurname);
      cy.getByData('success-message')
        .should('be.visible')
        .should('contain', 'Данные обновлены');
    });

    it('should show validation error for empty surname', () => {
      cy.editField('surname', '');
      cy.getByData('save-button').click();

      cy.errorShouldBeVisible('surname-error', 'Заполните фамилию');
    });

    it('should show validation error for incorrect email', () => {
      cy.editField('email', 'invalid_email');
      cy.getByData('save-button').click();

      cy.errorShouldBeVisible('email-error', 'Некорректный email');
    });

    it('should show server error on update fail', () => {
      cy.registerUser({ email: 'existing@example.ru' });

      cy.visit('/profile');
      cy.editField('email', 'existing@example.ru');
      cy.getByData('save-button').click();

      cy.getByData('form-error')
        .should('be.visible')
        .should('contain', 'Ошибка при обновлении данных');
    });

    it('should allow updating password', () => {
      const newPassword = 'new-password';

      cy.editField('password', newPassword);
      cy.getByData('save-button').should('be.visible').click();

      cy.getByData('success-message')
        .should('be.visible')
        .should('contain', 'Данные обновлены');

      cy.getByData('logout-button').click();

      cy.loginUser({
        email: user.email,
        password: newPassword,
      });

      cy.location('pathname').should('eq', '/');
    });
  });

  context('Logout', () => {
    it('should logout user', () => {
      cy.getByData('logout-button').click();

      cy.location('pathname').should('eq', '/login');

      cy.window().then((win) => {
        expect(win.localStorage.getItem('access_token')).to.be.null;
      });
    });
  });

  context('Delete account', () => {
    it('should delete account after confirmation', () => {
      cy.getByData('delete-button').click();
      cy.getByData('confirm-delete').click();

      cy.location('pathname').should('eq', '/login');

      cy.window().then((win) => {
        expect(win.localStorage.getItem('access_token')).to.be.null;
      });
    });
  });

  context('Save button behavior', () => {
    it('should not show save button without changes', () => {
      cy.getByData('save-button').should('not.exist');
    });

    it('should show save button after field change', () => {
      cy.editField('name', 'new-name');

      cy.getByData('save-button').should('be.visible');
    });

    it('should hide save button after successful save', () => {
      cy.editField('name', 'another-name');

      cy.getByData('save-button').click();

      cy.getByData('save-button').should('not.exist');
    });

    it('should not show save button if value is unchanged', () => {
      cy.getByData('profile-name')
        .invoke('text')
        .then((currentName) => {
          cy.editField('name', currentName.trim());
        });

      cy.getByData('save-button').should('not.exist');
    });
  });
});