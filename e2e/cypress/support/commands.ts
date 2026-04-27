import { ReturnedUserByEmail } from "./index";

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

Cypress.Commands.add('errorShouldBeVisible', (errorSelector, errorText) => {
  cy.getByData(errorSelector).should('be.visible').should('contain', errorText);
});