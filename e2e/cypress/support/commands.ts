Cypress.Commands.add('getByData', (selector) => {
  return cy.get(`[data-test=${selector}]`);
});

Cypress.Commands.add('registerUser', (userData) => {
  cy.visit('/register');

  const {
    email = 'test1@example.ru',
    name = 'test1-name',
    surname = 'test1-surname',
    password = 'test1-password',
    passwordConfirm = 'test1-password',
  } = userData;

  if (email !==  null) cy.getByData('email-input').type(email);
  if (name !==  null) cy.getByData('name-input').type(name);
  if (surname !==  null) cy.getByData('surname-input').type(surname);
  if (password !==  null) cy.getByData('password-input').type(password);
  if (passwordConfirm !==  null) cy.getByData('password-confirm-input').type(passwordConfirm);

  cy.getByData('submit').click();
});

Cypress.Commands.add('loginUser', (userData) => {
  cy.visit('/login');

  const {
    email = 'test1@example.ru',
    password = 'test1-password',
  } = userData;

  if (email !== null) cy.getByData('email-input').type(email);
  if (password !== null) cy.getByData('password-input').type(password);

  cy.getByData('submit').click();
});

Cypress.Commands.add('errorShouldBeVisible', (errorSelector, errorText) => {
  cy.getByData(errorSelector).should('be.visible').should('contain', errorText);
});

Cypress.Commands.add('editField', (field, value) => {
  cy.getByData(`${field}-edit`).click();

  cy.getByData(`${field}-input`).then(($input) => {
    const currentValue = $input.val();

    cy.wrap($input).clear();

    if (value !== '' && value !== currentValue) {
      cy.wrap($input).type(value);
    }
  });
});
