describe('Test postZoom', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type('test@gmail.com');
		cy.get('[data-cy=login-password]').type('test');
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
		cy.wait(1000);
	});

	it('click image card', () => {
		cy.get('[data-cy=image-card]').should('not.be.empty');
		cy.get('[data-cy=image-card]').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
			cy.url().should('include', '/postZoom');
			cy.wait(1000);
		});
		cy.get('[data-cy=input-comment]').type("some random comment");
		cy.get('[data-cy=post-comment-button]').click();
		cy.wait(1000);
		cy.get('[data-cy=comment-list]').should('not.have.length', 0);
		cy.get('[data-cy=go-back-button]').click();
		cy.url().should('include', '/home');
	});
});