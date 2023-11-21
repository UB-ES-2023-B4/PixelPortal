import 'cypress-file-upload';

describe('Test update profile', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
	});

	it('test change user profile', () => {
		cy.get('.username').click();
		cy.get('[data-cy=edit-profile]').click();
		cy.wait(500);
		cy.get('.form-control').clear();
		cy.get('.form-control').type('Yee@t');
		cy.get('button:contains("Save")').click();
		cy.on('window:confirm', () => true);
		cy.url().should('include', '/user');
		cy.wait(500);
		cy.get('[data-cy=user-description]').should('include.text', 'Yee@t');
	})
});