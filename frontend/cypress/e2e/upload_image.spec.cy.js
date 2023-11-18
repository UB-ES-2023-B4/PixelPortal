import 'cypress-file-upload';

describe('Test upload image', () => {
	before(() => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type('testemail999@hotmail.com');
		cy.get('[data-cy=login-password]').type('testPassword1!');
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
	});

	it('valid upload image', () => {
		cy.get('[data-cy=post-button]').click();
		cy.get('[data-cy=image-upload-input]').attachFile({
			fileContent: 'tiredcat.jpg',
			fileName: 'tiredcat.jpg',
			mimeType: 'image/jpg',
		});
		cy.get('[data-cy=image-upload-input]').trigger('change', { force: true });
		cy.get('[data-cy=upload-title]').type('Tired cat');
		cy.get('[data-cy=upload-description]').type('This image represents a very tierd cat.');
		cy.get('[data-cy=upload-tags-input]').type('cat, cutie, cattie!').type('{enter}');
		cy.get('[data-cy=upload-publish-button]').click();
		cy.on('window:alert',(t)=>{
		  expect(t).to.equal("Image uploaded successfully!")
		});
	});

	it('empty attachFile upload image', () => {
		cy.get('[data-cy=post-button]').click();
		cy.get('[data-cy=upload-title]').type('Tired cat');
		cy.get('[data-cy=upload-description]').type('This image represents a very tierd cat.');
		cy.get('[data-cy=upload-publish-button]').should('be.disabled');
		cy.get('[data-cy=upload-close-button]').click();
	});

	it('empty title and description upload image', () => {
		cy.get('[data-cy=post-button]').click();
		cy.get('[data-cy=image-upload-input]').attachFile({
			fileContent: 'tiredcat.jpg',
			fileName: 'tiredcat.jpg',
			mimeType: 'image/jpg',
		});
		cy.get('[data-cy=image-upload-input]').trigger('change', { force: true });
		cy.get('[data-cy=upload-publish-button]').should('be.disabled');
		cy.get('[data-cy=upload-close-button]').click();
	});
});