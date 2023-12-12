describe('Test show following posts', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('test@gmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('test');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1500);
	});

	it('test show following post', () => {
		cy.get('button.post-button').contains('Following Posts').click();
		cy.wait(500);
		cy.get('.image-container .images .image-card').should('have.length.gte', 1);
		cy.get('button.post-button').contains('Following Posts').click();
	})
});