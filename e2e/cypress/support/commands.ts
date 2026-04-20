import { ReturnedUserByEmail } from "./index";

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

Cypress.Commands.add('errorShouldBeVisible', (errorSelector, errorText) => {
  cy.getByData(errorSelector).should('be.visible').should('contain', errorText);
});

Cypress.Commands.add('execDBUtils', (args) => {
  return cy.exec(`cd ../backend && python3 -m tests.db_utils_for_cypress ${args.join(' ')}`);
});

Cypress.Commands.add('resetDB', () => {
  cy.execDBUtils(['reset']);
});

Cypress.Commands.add('seedDB', () => {
  cy.execDBUtils(['seed']);
});

Cypress.Commands.add('getUserByEmail', (email) => {
  cy.execDBUtils(['getUserByEmail', email])
    .then((result) => {
      const user: ReturnedUserByEmail = JSON.parse(result.stdout);
      return user;
  });
});
