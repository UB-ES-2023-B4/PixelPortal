describe('Test list followers', () => {
	it('test list following', () => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('test@gmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('test');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1500);

		cy.contains('button.post-button', 'Search User').click();
		cy.wait(1500);
		cy.get('.user-container .user').first().click();
		cy.url().should('include', '/user');
		cy.wait(500);
		cy.get('.page-button').contains('Follow').click();
		cy.get('[data-cy=home-button]').click();
		cy.wait(1500);
		cy.get('.username').click();
		cy.get('[data-cy=check-follow]').click();
		cy.get('label').contains('Following').click();
		cy.wait(500);
		cy.get('.follower-container .follower').should('have.length', 1);
		cy.get('button.btn-close').click();
	})
	it('test list followers', () => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1500);
		
		cy.get('.username').click();
		cy.get('[data-cy=check-follow]').click();
		cy.wait(500);
		cy.get('.follower-container .follower').should('have.length', 1);
		cy.get('button.btn-close').click();
	})
});