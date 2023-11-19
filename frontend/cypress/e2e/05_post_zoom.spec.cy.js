describe('Test postZoom', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type('testemail111@hotmail.com');
		cy.get('[data-cy=login-password]').type('testPassword1!');
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
	});

	it('click image card', () => {
		cy.get('[data-cy=image-card]').should('not.be.empty');
		cy.get('[data-cy=image-card]').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
		});
		cy.url().should('include', '/postZoom');
	});
});