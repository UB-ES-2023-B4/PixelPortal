describe('Test filter image by username', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type('testemail111@hotmail.com');
		cy.get('[data-cy=login-password]').type('testPassword1!');
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
	});

	const filter_image_by_username = (username) => {
		cy.get('[data-cy=search-bar]').type('@' + username);
		cy.wait(500);
		if (username) {
			cy.get('.images .image-card').should('not.be.empty');
			cy.get('[data-cy=image-card-username]').each(($usernameElement) => {
				cy.wrap($usernameElement).should('include.text', username);
			  });
		}
		cy.get('[data-cy=search-bar]').clear();
	}

	it('filter by username1', () => {
		filter_image_by_username('User');
	});
	it('filter by username2', () => {
		filter_image_by_username('test');
	});
	it('filter by username3', () => {
		filter_image_by_username('testUser');
	});
});