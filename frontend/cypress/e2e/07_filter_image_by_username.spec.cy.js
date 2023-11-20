describe('Test filter image by username', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
	});

	const filter_image_by_username = (username) => {
		cy.get('.image-container .search-container .search-box input[type="text"]').as('searchInput');
		cy.get('@searchInput').type('@' + username);
		cy.wait(500);
		if (username) {
			cy.get('.images .image-card').should('not.be.empty');
			cy.get('.images .image-card .image-username').each(($usernameElement) => {
				cy.wrap($usernameElement).should('include.text', username);
			  });
		}
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