describe('Test bookmark', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('test@gmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('test');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1500);
	});

	it('test search user', () => {
		cy.contains('button.post-button', 'Search User').click();
		cy.wait(1500);
		cy.get('.user-container .user').should('have.length.greaterThan', 3);
		cy.get('[data-cy=close-button]').click();
	})

	it('test user search bar', () => {
		cy.contains('button.post-button', 'Search User').click();
		cy.wait(500);
		cy.get('[data-cy=user-search-bar').type('3');
		cy.wait(1000);
		cy.get('.user-container .user').should('have.length', 1);
		cy.get('[data-cy=close-button]').click();
	})

	it('test user select', () => {
		cy.contains('button.post-button', 'Search User').click();
		cy.wait(1500);
		cy.get('.user-container .user').first().click();
		cy.url().should('include', '/user');
	})
});