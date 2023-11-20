describe('Test filter image by category', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
	});

	const filter_image_by_category = (category) => {
		cy.get('.image-container .search-container .search-box input[type="text"]').as('searchInput');
		cy.get('@searchInput').type('#' + category);
		cy.wait(500);
		if (category) {
			cy.get('.images .image-card').should('not.be.empty')
			cy.get('.images .image-card').first(($card) => {
				cy.wrap($card).click();
				cy.url().should('include', '/postZoom');
				cy.get('.tag').should(($tags) => {
					expect($tags.toArray().some((tag) => tag.innerText.toLowerCase().includes(category))).to.be.true;
				});
			});
		}
	}

	it('filter by category1', () => {
		filter_image_by_category('cat');
	});
	it('filter by category2', () => {
		filter_image_by_category('nyam');
	});
});