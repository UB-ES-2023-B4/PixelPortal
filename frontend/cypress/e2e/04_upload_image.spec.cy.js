import 'cypress-file-upload';

describe('Test upload image', () => {
	const before_each = (email, password) => {
		cy.visit('http://localhost:8080');
		cy.get('.login-show input[placeholder="Username"]').type(email);
		cy.get('.login-show input[placeholder="Password"]').type(password);
		cy.get('.login-show input[type="button"][value="Login"]').click();
		cy.url().should('include', '/home');
		cy.wait(500);
	};
	const after_each = () => {
		cy.visit('http://localhost:8080');
	};

	const upload_image = (_fileContent, _filename, _mimeType, title, description, tags) => {
		cy.get('.user-info-wrapper .post-button:contains("Post")').click();
		if (_fileContent && _mimeType){
			cy.fixture(_fileContent).then((fileContent) => {
				cy.get('.popup-inner .image-upload-input').attachFile({
				  fileContent: fileContent.toString(),
				  fileName: _filename,
				  mimeType: _mimeType,
				});
			  });
		}
		cy.get('.popup-inner .image-upload-input').trigger('change', { force: true });
		if (title) {
			cy.get('.popup-inner .image-title-input').type(title);
		}
		if (description) {
			cy.get('.popup-inner .image-description-input').type(description);
		}
		if (tags) {
			cy.get('.popup-inner .image-tags-input').type(tags).type('{enter}');
		}
		cy.get('.popup-inner .form-button .popup-button:contains("Publish")').then(($button) => {
			if ($button.is(":disabled")) {
			  return ;
			} else {
			  cy.wrap($button).click();
			}
		  });
	};

	it('valid upload image', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		upload_image('tiredcat.jpg',
					 'tiredcat.jpg',
					 'image/jpeg',
					 'Tired cat',
					 'This image represents a very tierd cat.',
					 'cat, cutie, cattie');
		cy.on('window:confirm', () => true);
		cy.wait(1000)
		after_each();
	});
	it('valid upload image2', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		upload_image('angrycat.jpg',
					 'angrycat.jpg',
					 'image/jpeg',
					 'Angry cat',
					 'Be aware from this angry cat',
					 'Do Not Distrub, cat');
		cy.on('window:confirm', () => true);
		cy.wait(1000)
		after_each();
	});
	it('valid upload image3', () => {
		before_each('testemail222@hotmail.com', 'testPassword2!');
		upload_image('lickingcat.jpg',
					 'lickingcat.jpg',
					 'image/jpeg',
					 'Licking cat',
					 'That\'s very tasty!',
					 'nyam, cat');
		cy.on('window:confirm', () => true);
		cy.wait(1000)
		after_each();
	});
	it('valid upload image4', () => {
		before_each('testemail333@hotmail.com', 'testPassword3!');
		upload_image('cutiecat.jpg',
					 'cutiecat.jpg',
					 'image/jpeg',
					 'Cutie cat',
					 'The most cutiest cat',
					 '');
		cy.on('window:confirm', () => true);
		cy.wait(1000)
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
		cy.get('.popup-inner .form-button .popup-button:contains("Publish")').should('be.disabled');
		cy.get('.popup-inner .form-button .popup-button:contains("Close")').click();
		after_each();
	});
	it('empty title and description upload image', () => {
		before_each('testemail111@hotmail.com', 'testPassword1!');
		upload_image('tiredcat.jpg',
					 'tiredcat.jpg',
					 'image/jpeg',
					 '',
					 '',
					 '');
		cy.get('.popup-inner .form-button .popup-button:contains("Publish")').should('be.disabled');
		cy.get('.popup-inner .form-button .popup-button:contains("Close")').click();
		after_each();
	});
});