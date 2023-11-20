describe('Test like', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
	});

	it('test like and dislike', () => {
		cy.get('.images .image-card').should('not.be.empty')
		cy.get('.images .image-card').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
			cy.url().should('include', '/postZoom');
			cy.wait(500);
		});
		cy.get('.like-button').click();
		cy.get('.like-button img').should('have.attr', 'src').and('include', 'favorite_black_24dp');
		cy.get('.like-button').click();
		cy.get('.like-button img').should('have.attr', 'src').and('include', 'favorite_border_black_24dp');
	})

	it('test spam like button', () => {
		cy.get('.images .image-card').should('not.be.empty')
		cy.get('.images .image-card').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
			cy.url().should('include', '/postZoom');
			cy.wait(500);
		});
		for (let i = 0; i < 8; i++) {
			cy.get('.like-button').click();
		}
		cy.get('.like-button img').should('have.attr', 'src').and('include', 'favorite_border_black_24dp');
	})
});