declare global {
    namespace Cypress {
        interface Chainable {
            getByData(dataTestAttribure: string): Chainable<JQuery<HTMLElement>>,
            registerUser(userData: UserRegisterData): Chainable<void>,
            errorShouldBeVisible(errorSelector: string, errorText: string): Chainable<void>,
            resetDB(): Chainable<void>,
            seedDB(): Chainable<void>,
            execDBUtils(args: string[]): Chainable<Exec>,
            getUserByEmail(email: string): Chainable<ReturnedUserByEmail>,
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