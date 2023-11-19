describe('Test postZoom', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
	});

	it('click image card', () => {
		cy.get('.images .image-card').should('not.be.empty');
		cy.get('.images .image-card').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
		});
		cy.url().should('include', '/postZoom');
	});
});