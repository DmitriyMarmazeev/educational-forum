Cypress.Commands.add('getByData', (selector) => {
  return cy.get(`[data-test=${selector}]`);
});

Cypress.Commands.add('registerUser', (userData) => {
  cy.visit('/');

  const {
    email = 'test1@example.ru',
    name = 'test1-name',
    surname = 'test1-surname',
    password = 'test1-password',
    passwordConfirm = 'test1-password',
    shouldFail = false,
    shouldSuccessBeStubbed = false,
  } = userData;

  if (email !== undefined) cy.getByData('email-input').type(email);
  if (name !== undefined) cy.getByData('name-input').type(name);
  if (surname !== undefined) cy.getByData('surname-input').type(surname);
  if (password !== undefined) cy.getByData('password-input').type(password);
  if (passwordConfirm !== undefined) cy.getByData('password-confirm-input').type(passwordConfirm);

  if (shouldSuccessBeStubbed) {
    if (shouldFail) {
      cy.intercept('POST', '/auth/register', {
        statusCode: 400,
        body: {
          detail: 'Validation error'
        }
      }).as('register');
    } else {
      cy.intercept('POST', 'auth/register', {
        statusCode: 201,
        body: {
          "access_token": "access_token_stub",
          "token_type": "access"
        }
      }).as('register');
    }
  }

  cy.getByData('submit').click();
  
   if (shouldSuccessBeStubbed) cy.wait('@register');
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
