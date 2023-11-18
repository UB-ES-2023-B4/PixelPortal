describe('Test upload image', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type('testemail999@hotmail.com');
		cy.get('[data-cy=login-password]').type('testPassword1!');
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
	});

	it('valid upload image', () => {
		
	});
});