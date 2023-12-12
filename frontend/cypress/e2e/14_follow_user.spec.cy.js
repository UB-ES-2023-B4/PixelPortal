describe('Test follow user', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('test@gmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('test');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1500);
	});

	it('test follow', () => {
		cy.get('.sort-button').click();
		cy.contains('Sort by upload Date (descending)').click();
		cy.wait(1000);
		cy.get('.images .image-card').should('not.be.empty').first().click();
		cy.url().should('include', '/postZoom');
		cy.wait(500);
		cy.get('.username').click();
		cy.wait(500);
		cy.get('.page-button').contains('Follow').click();
		cy.wait(500);
		cy.get('[data-cy=check-follow]').should('include.text', '1 Followers');
		cy.get('[data-cy=home-button]').click();
		cy.wait(500);
		cy.get('[data-cy=go-back-button]').click();
		cy.wait(500);
		cy.get('.username').click();
		cy.get('[data-cy=check-follow]').should('include.text', '1 Following');
	})

	it('test unfollow', () => {
		cy.get('.sort-button').click();
		cy.contains('Sort by upload Date (descending)').click();
		cy.wait(1000);
		cy.get('.images .image-card').should('not.be.empty').first().click();
		cy.url().should('include', '/postZoom');
		cy.wait(500);
		cy.get('.username').click();
		cy.wait(500);
		cy.get('.page-button').contains('Unfollow').click();
		cy.wait(500);
		cy.get('[data-cy=check-follow]').should('include.text', '0 Followers');
		cy.get('[data-cy=home-button]').click();
		cy.wait(500);
		cy.get('[data-cy=go-back-button]').click();
		cy.wait(500);
		cy.get('.username').click();
		cy.get('[data-cy=check-follow]').should('include.text', '0 Following');
	})
});