describe('Test bookmark', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('test@gmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('test');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1500);
	});

	it('test set bookmark', () => {
		cy.get('.sort-button').click();
		cy.contains('Sort by upload Date (descending)').click();
		cy.wait(1000);
		cy.get('.images .image-card').should('not.be.empty').first().click();
		cy.url().should('include', '/postZoom');
		cy.wait(500);
		cy.get('button.btn-default.btn-xs.bookmark').click();
		cy.wait(500);
		cy.get('[data-cy=bookmark-img]').should('have.attr', 'src').and('include', 'bookmark-fill.');
	})

	it('test unset bookmark', () => {
		cy.get('.sort-button').click();
		cy.contains('Sort by upload Date (descending)').click();
		cy.wait(1000);
		cy.get('.images .image-card').should('not.be.empty').first().click();
		cy.url().should('include', '/postZoom');
		cy.wait(500);
		cy.get('button.btn-default.btn-xs.bookmark').click();
		cy.wait(500);
		cy.get('[data-cy=bookmark-img]').should('have.attr', 'src').and('include', 'bookmark.');
	})
});