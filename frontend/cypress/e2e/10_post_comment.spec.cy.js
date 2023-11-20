describe('Test postZoom', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type('test@gmail.com');
		cy.get('.login-show input[placeholder="Password"]').type('test');
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(1000);
	});

	it('click image card', () => {
		cy.get('.images .image-card').should('not.be.empty');
		cy.get('.images .image-card').first().within(() => {
			cy.get('img').should('be.visible');
			cy.get('img').click();
			cy.url().should('include', '/postZoom');
			cy.wait(1000);
		});
		cy.get('input[type="text"][placeholder="Add a comment..."]').type("some random comment");
		cy.get('button:contains("Post")').click();
		cy.wait(1000);
		cy.get('.box-info .box-footer .box-comment').should('have.length', 1);
		cy.get('button:contains("Go Back")').click();
		cy.url().should('include', '/home');
	});
});