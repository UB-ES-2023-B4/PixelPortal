import 'cypress-file-upload';

describe('Test upload image', () => {
	const before_each = (email, password) => {
		cy.visit('http://localhost:8080');
		cy.get('[data-cy=login-email]').type(email);
		cy.get('[data-cy=login-password]').type(password);
		cy.get('[data-cy=login-button]').click();
		cy.url().should('include', '/home');
	};
	const after_each = () => {
		cy.visit('http://localhost:8080');
	};

	const  upload_image = (_fileContent, _filename, _mimeType, title, description, tags) => {
		cy.get('[data-cy=post-button]').click();
		if (_fileContent && _mimeType){
			cy.fixture(_fileContent).then((fileContent) => {
				cy.get('[data-cy=image-upload-input]').attachFile({
				  fileContent,
				  fileName: _filename,
				  mimeType: _mimeType,
				});
			  });
		}
		cy.get('[data-cy=image-upload-input]').trigger('change', { force: true });
		if (title) {
		cy.get('[data-cy=upload-title]').type(title);
		}
		if (description) {
		cy.get('[data-cy=upload-description]').type(description);
		}
		if (tags) {
		cy.get('[data-cy=upload-tags-input]').type(tags).type('{enter}');
		}
		cy.get('[data-cy=upload-publish-button]').then(($button) => {
			if ($button.is(":disabled")) {
			  return
			} else {
			  cy.wrap($button).click()
			}
		  })
	};

	it('valid upload image', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		upload_image('tiredcat.jpg',
					 'tiredcat.jpg',
					 'image/jpg',
					 'Tired cat',
					 'This image represents a very tierd cat.',
					 'cat, cutie, cattie');
		cy.on('window:confirm', () => true);
		cy.wait(500)
		after_each();
	});
	it('valid upload image2', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		upload_image('angrycat.jpg',
					 'angrycat.jpg',
					 'image/jpg',
					 'Angry cat',
					 'Be aware from this angry cat',
					 'Do Not Distrub, cat');
		cy.on('window:confirm', () => true);
		cy.wait(500)
		after_each();
	});
	it('valid upload image3', () => {
		before_each('testemail222@hotmail.com', 'testPassword2!');
		upload_image('lickingcat.jpg',
					 'lickingcat.jpg',
					 'image/jpg',
					 'Licking cat',
					 'That\'s very tasty!',
					 'nyam, cat');
		cy.on('window:confirm', () => true);
		cy.wait(500)
		after_each();
	});
	it('valid upload image4', () => {
		before_each('testemail333@hotmail.com', 'testPassword3!');
		upload_image('cutiecat.jpg',
					 'cutiecat.jpg',
					 'image/jpg',
					 'Cutie cat',
					 'The most cutiest cat',
					 '');
		cy.on('window:confirm', () => true);
		cy.wait(500)
		after_each();
	});
	it('empty attachFile upload image', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		upload_image('',
					 '',
					 '',
					 'Tired cat',
					 'This image represents a very tierd cat.',
					 '');
		cy.get('[data-cy=upload-publish-button]').should('be.disabled');
		cy.get('[data-cy=upload-close-button]').click();
		after_each();
	});
	it('empty title and description upload image', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		upload_image('tiredcat.jpg',
					 'tiredcat.jpg',
					 'image/jpg',
					 '',
					 '',
					 '');
		cy.get('[data-cy=upload-publish-button]').should('be.disabled');
		cy.get('[data-cy=upload-close-button]').click();
		after_each();
	});
});