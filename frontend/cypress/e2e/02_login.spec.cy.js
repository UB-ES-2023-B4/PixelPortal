describe('Test login', () => {
  const loginUser = (email, password) => {
    cy.visit('http://localhost:8080');
    if (email) {
    cy.get('[data-cy=login-email]').type(email);
    }
    if (password) {
    cy.get('[data-cy=login-password]').type(password);
    }
    cy.get('[data-cy=login-button]').click();
  };

  it('valid login1', () => {
    loginUser('testemail111@hotmail.com', 
              'testPassword1!');
    cy.url().should('include', '/home');
  });
  it('valid login2', () => {
    loginUser('testemail222@hotmail.com', 
              'testPassword2!');
    cy.url().should('include', '/home');
  });
  it('valid login3', () => {
    loginUser('testemail333@hotmail.com', 
              'testPassword3!');
    cy.url().should('include', '/home');
  });
  it('invalid login', () => {
    loginUser('invalid-email', 
              'password');
    cy.on('window:alert', () => {});
  });
  it('not existing login', () => {
    loginUser('nonExistingEmail@gmail.com', 
              'password');
    cy.on('window:alert', () => {});
  });
  it('wrong password', () => {
    loginUser('testemail111@hotmail.com', 
              'wrong');
    cy.on('window:alert', () => {});
  });
  it('empty login', () => {
    loginUser('', 
              'password');
    cy.on('window:alert', () => {});
  });
  it('empty password', () => {
    loginUser('testemail111@hotmail.com', 
              '');
    cy.on('window:alert', () => {});
  });
});
