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
		cy.wait(200);
		cy.fixture("pingu.jpg").then((fileContent) => {
			cy.get('.image-upload-input').attachFile({
			  fileContent: fileContent,
			  fileName: "pingu.jpg",
			  mimeType: 'image/jpeg',
			});
			cy.get('.image-upload-input').trigger('change', { force: true });
		  });
		cy.get('.form-control').clear();
		cy.get('.form-control').type('Yee@t');
		cy.get('button:contains("Save")').click();
		cy.on('window:confirm', () => true);
		cy.url().should('include', '/user');
		cy.get('p.text-muted.mb-1[data-cy=user-description]').should('include.text', 'Yee@t');
	})
});