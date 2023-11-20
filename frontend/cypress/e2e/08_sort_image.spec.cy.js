describe('Test sort image', () => {
	beforeEach(() => {
	  // Login before each test
	  cy.visit('http://localhost:8080');
	  cy.get('.login-show input[placeholder="Username"]').type('testemail111@hotmail.com');
	  cy.get('.login-show input[placeholder="Password"]').type('testPassword1!');
	  cy.get('.login-show input[type="button"][value="Login"]').click();
	  cy.url().should('include', '/home');
	  cy.wait(1000);
	});
  
	it('should sort images by upload date in ascending order', () => {
	  cy.get('.sort-button').click();
	  cy.contains('Sort by upload Date (ascending)').click();
	  cy.wait(2000);
  
	  cy.get('.images .image-card').should('not.be.empty').first().click();
	  cy.url().should('include', '/postZoom');
	  cy.wait(500);
  
	  cy.get('.debug-description').invoke('text').then((text) => {
		Cypress.env('postDate1', text);
	  });
  
	  cy.get('button:contains("Go Back")').click();
	  cy.url().should('include', '/home');
  
	  cy.get('.sort-button').click();
	  cy.contains('Sort by upload Date (ascending)').click();
	  cy.wait(2000);
  
	  cy.get('.images .image-card').should('not.be.empty').eq(1).click();
	  cy.url().should('include', '/postZoom');
	  cy.wait(500);
  
	  cy.get('.debug-description').invoke('text').then((text) => {
		Cypress.env('postDate2', text);
	  });
  
	  cy.get('button:contains("Go Back")').click();
	  cy.url().should('include', '/home');
	});
  
	it('should compare post dates', () => {
	  const postDate1 = Cypress.env('postDate1');
	  const postDate2 = Cypress.env('postDate2');

	  cy.log(postDate1)
	  cy.log(postDate2)
  
	  const date1 = new Date(postDate1);
	  const date2 = new Date(postDate2);

	  expect(date1).to.be.lessThan(date2);
	});

	it('should sort images by upload date in descending order', () => {
		cy.get('.sort-button').click();
		cy.contains('Sort by upload Date (descending)').click();
		cy.wait(2000);
	
		cy.get('.images .image-card').should('not.be.empty').first().click();
		cy.url().should('include', '/postZoom');
		cy.wait(500);
	
		cy.get('.debug-description').invoke('text').then((text) => {
		  Cypress.env('postDate1', text);
		});
	
		cy.get('button:contains("Go Back")').click();
		cy.url().should('include', '/home');
	
		cy.get('.sort-button').click();
		cy.contains('Sort by upload Date (descending)').click();
		cy.wait(2000);
	
		cy.get('.images .image-card').should('not.be.empty').eq(1).click();
		cy.url().should('include', '/postZoom');
		cy.wait(500);
	
		cy.get('.debug-description').invoke('text').then((text) => {
		  Cypress.env('postDate2', text);
		});
	
		cy.get('button:contains("Go Back")').click();
		cy.url().should('include', '/home');
	  });
	
	  it('should compare post dates', () => {
		const postDate1 = Cypress.env('postDate1');
		const postDate2 = Cypress.env('postDate2');
  
		cy.log(postDate1)
		cy.log(postDate2)
	
		const date1 = new Date(postDate1);
		const date2 = new Date(postDate2);
  
		expect(date1).to.be.greaterThan(date2);
	  });
  });
  