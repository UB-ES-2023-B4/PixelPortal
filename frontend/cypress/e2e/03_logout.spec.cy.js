describe('Test logout', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type('testemail111@hotmail.com');
		cy.get('[data-cy=login-password]').type('testPassword1!');
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
	});

	it('logout user', () => {
		cy.get('[data-cy=user-vertical-rounded-dots]').click();
		cy.get('[data-cy=logout-button]').click();
		cy.url().should('eq', 'http://localhost:8080/');
	});
});