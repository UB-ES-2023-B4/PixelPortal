describe('Test delete post', () => {
	const before_each = (email, password) => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type(email);
		cy.get('.login-show input[placeholder="Password"]').type(password);
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(500);
	};

	it('test deleting post', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		cy.get('.user-info-wrapper .post-button:contains("My Images")').click();
		cy.wait(500);
		cy.get('.images .image-card').should('not.be.empty')
		cy.get('.images .image-card').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
			cy.url().should('include', '/postZoom');
			cy.wait(500);
		});
		cy.get('button:contains("Delete")').click();
		cy.wait(200);
		cy.on('window:confirm', () => true);
		cy.wait(200);
		cy.on('window:confirm', () => true);
		cy.url().should('include', '/home');
	});

	it('test deleting other user\'s post', () => {
		before_each('test@gmail.com', 'test');
		cy.get('.images .image-card').should('not.be.empty')
		cy.get('.images .image-card').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
			cy.url().should('include', '/postZoom');
			cy.wait(500);
		});
		cy.get('button:contains("Delete")').should('be.hidden');
	});
});