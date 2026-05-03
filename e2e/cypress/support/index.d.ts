declare global {
    namespace Cypress {
        interface Chainable {
            getByData(dataTestAttribure: string): Chainable<JQuery<HTMLElement>>,
            registerUser(userData: UserRegisterData): Chainable<void>,
            loginUser(userData: UserLoginData): Chainable<void>,
            errorShouldBeVisible(errorSelector: string, errorText: string): Chainable<void>,
            editField(field: string, value: string): Chainable<void>,
        }
    }
}

export interface UserRegisterData {
    email?: string,
    name?: string,
    surname?: string,
    password?: string,
    passwordConfirm?: string,
}

export interface UserLoginData {
  email?: string,
  password?: string,
}