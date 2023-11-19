describe('Test filter image by category', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type('testemail111@hotmail.com');
		cy.get('[data-cy=login-password]').type('testPassword1!');
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
	});

	const filter_image_by_category = (category) => {
		cy.get('[data-cy=search-bar]').type('#' + category);
		cy.wait(500);
		if (category) {
			cy.get('.images .image-card').should('not.be.empty')
			cy.get('.images .image-card').first(($card) => {
				cy.wrap($card).click();
				cy.url().should('include', '/postZoom');
				cy.get('.tag').should(($tags) => {
					expect($tags.toArray().some((tag) => tag.innerText.toLowerCase().includes(category))).to.be.true;
				});
				cy.get('[data-cy=go-back-button]').click();
				cy.url().should('include', '/home');
			});
			cy.get('[data-cy=search-bar]').clear();
		}
	}

	it('filter by category1', () => {
		filter_image_by_category('cat');
	});
	it('filter by category2', () => {
		filter_image_by_category('nyam');
	});
});