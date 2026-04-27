declare global {
    namespace Cypress {
        interface Chainable {
            getByData(dataTestAttribure: string): Chainable<JQuery<HTMLElement>>,
            registerUser(userData: UserRegisterData): Chainable<void>,
            errorShouldBeVisible(errorSelector: string, errorText: string): Chainable<void>,
        }
    }
}

interface UserRegisterData {
    email?: string,
    name?: string,
    surname?: string,
    password?: string,
    passwordConfirm?: string,
    shouldFail?: boolean,
    shouldSuccessBeStubbed?: boolean,
}

export interface ReturnedUserByEmail {
    user_id: string,
    email: string,
}