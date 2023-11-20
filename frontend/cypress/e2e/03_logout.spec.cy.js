describe('Test logout', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1000);
	});

	it('logout user', () => {
		cy.get('.user-info .dropdown .options-button').click();
		cy.get('.user-info .dropdown #dropdown-content').click();
		cy.url().should('eq', 'http://localhost:8080/');
	});
});