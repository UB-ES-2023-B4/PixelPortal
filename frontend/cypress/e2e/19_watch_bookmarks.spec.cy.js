describe('Test watch bookmarked images', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('test@gmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('test');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1500);
	});

	it('test show bookmark list', () => {
		cy.get('.sort-button').click();
		cy.contains('Sort by upload Date (descending)').click();
		cy.wait(1000);
		cy.get('.images .image-card').should('not.be.empty').first().click();
		cy.url().should('include', '/postZoom');
		cy.wait(500);
		cy.get('button.btn-default.btn-xs.bookmark').click();
		cy.wait(500);

		cy.get('button:contains("Go Back")').click();
		cy.url().should('include', '/home');
		cy.wait(1000);

		cy.get('.username').click();
		cy.contains('li', 'Bookmarks').click();
		cy.wait(500);
		cy.get('.image-container .images').should('have.length', 1);
		cy.get('[data-cy=bookmark-list-close]').click();
	})
});