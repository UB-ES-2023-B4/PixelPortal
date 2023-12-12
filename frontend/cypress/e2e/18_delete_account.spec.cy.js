describe('Test delete account', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080');
	});

	const registerUser = (username, email, password, confirmPassword) => {
		cy.visit('http://localhost:8080');
		cy.get('label[for="log-login-show"]').click();
		if (username){
			cy.get('.register-show input[placeholder="Username"]').type(username);
		}
		if (email){
			cy.get('.register-show input[placeholder="Email"]').type(email);
		}
		if (password){
			cy.get('.register-show input[placeholder="Password"]').type(password);
		}
		if (confirmPassword){
			cy.get('.register-show input[placeholder="Confirm Password"]').type(confirmPassword);
		}
		cy.get('.register-show input[type="button"][value="Sign Up"]').click();
	};

	const loginUser = (email, password) => {
		cy.visit('http://localhost:8080');
		if (email) {
			cy.get('.login-show input[placeholder="Username"]').type(email);
		}
		if (password) {
			cy.get('.login-show input[placeholder="Password"]').type(password);
		}
		cy.get('.login-show input[type="button"][value="Login"]').click();
	};

	it('test delete account', () => {
		registerUser('delUser', 
					 'delEmail@gmail.com', 
					 'delete', 
					 'delete');
		cy.url().should('include', '/home');
		cy.wait(1500);
		cy.get('.username').click();
		cy.contains('li', 'Delete Account').click();
		cy.wait(500);
		loginUser('delEmail@gmail.com', 'delete')
		cy.wait(500);
		cy.url().should('eq', 'http://localhost:8080/')
	})
});