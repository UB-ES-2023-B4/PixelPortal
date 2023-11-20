describe('Test my images view', () => {
	const before_each = (email, password) => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type(email);
		cy.get('.login-show input[placeholder="Password"]').type(password);
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
	};
	const after_each = () => {
		cy.visit('http://localhost:8080');
	};
	
	const show_my_images = (username) => {
		cy.get('.user-info-wrapper .post-button:contains("My Images")').click();
		cy.wait(500);
		if (username) {
			cy.get('.images .image-card').should('not.be.empty');
			cy.get('.images .image-card .image-username').each(($usernameElement) => {
				cy.wrap($usernameElement).should('include.text', username);
			  });
		}
	}

	it('testUser1 images', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		show_my_images('testUser');
		cy.wait(500)
		after_each();
	});
	it('testUser2 images', () => {
		before_each('testemail222@hotmail.com', 'testPassword2!');
		show_my_images('testUser2');
		cy.wait(500)
		after_each();
	});
	it('testUser3 images', () => {
		before_each('testemail333@hotmail.com', 'testPassword3!');
		show_my_images('test3User');
		cy.wait(500)
		after_each();
	});
});