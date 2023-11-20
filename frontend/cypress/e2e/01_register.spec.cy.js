describe('Test register', () => {

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

  it('valid register1', () => {
    registerUser('testUser', 
                 'testemail111@hotmail.com', 
                 'testPassword1!', 
                 'testPassword1!');
    cy.url().should('include', '/home');
  });
  it('valid register2', () => {
    registerUser('testUser2', 
                 'testemail222@hotmail.com', 
                 'testPassword2!', 
                 'testPassword2!');
    cy.url().should('include', '/home');
  });
  it('valid register3', () => {
    registerUser('test3User', 
                 'testemail333@hotmail.com', 
                 'testPassword3!', 
                 'testPassword3!');
    cy.url().should('include', '/home');
  });
  it('valid register4', () => {
    registerUser('test', 
                 'test@gmail.com', 
                 'test', 
                 'test');
    cy.url().should('include', '/home');
  });
  it('repeated username register', () => {
    registerUser('testUser',
                 'newEmail@hotmail.com',
                 'testPassword2!',
                 'testPassword2!');
    cy.on('window:alert', () => {});
  });
  it('repeated email register', () => {
    registerUser('newUser',
                 'testemail999@hotmail.com',
                 'testPassword3!',
                 'testPassword3!');
    cy.on('window:alert', () => {});
  });
  it('empty field register', () => {
    registerUser('',
                 '',
                 'testPassword4!',
                 'testPassword4!');
    cy.on('window:alert', () => {});
  });
  it('repeated mismatch password register', () => {
    registerUser('newUser',
                 'newEmail@hotmail.com',
                 'testPassword2!',
                 'differentPassword');
    cy.on('window:alert', () => {});
  });
});
