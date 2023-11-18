describe('Test register', () => {
  it('valid register', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=sign-up-button').click();
    cy.get('[data-cy=register-username').type('testUser');
    cy.get('[data-cy=register-email]').type('testemail999@hotmail.com');
    cy.get('[data-cy=register-password').type('testPassword1!');
    cy.get('[data-cy=register-confirm_password').type('testPassword1!');
    cy.get('[data-cy=register-button').click();
    cy.url().should('include', '/home');
  });
  it('repeated username register', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=sign-up-button').click();
    cy.get('[data-cy=register-username').type('testUser');
    cy.get('[data-cy=register-email]').type('newEmail@hotmail.com');
    cy.get('[data-cy=register-password').type('testPassword2!');
    cy.get('[data-cy=register-confirm_password').type('testPassword2!');
    cy.get('[data-cy=register-button').click();
    cy.on('window:alert',(t)=>{
      expect(t).to.equal("Error: User already registered")
    });
  });
  it('repeated email register', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=sign-up-button').click();
    cy.get('[data-cy=register-username').type('newUser');
    cy.get('[data-cy=register-email]').type('testemail999@hotmail.com');
    cy.get('[data-cy=register-password').type('testPassword3!');
    cy.get('[data-cy=register-confirm_password').type('testPassword3!');
    cy.get('[data-cy=register-button').click();
    cy.on('window:alert',(t)=>{
      expect(t).to.equal("Error: Email already registered")
    });
  });
  it('empty field register', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=sign-up-button').click();
    cy.get('[data-cy=register-password').type('testPassword4!');
    cy.get('[data-cy=register-confirm_password').type('testPassword4!');
    cy.get('[data-cy=register-button').click();
    cy.on('window:alert',(t)=>{
      expect(t).to.equal("Email is not valid")
    });
  });
  it('repeated missmatch password register', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=sign-up-button').click();
    cy.get('[data-cy=register-username').type('newUser');
    cy.get('[data-cy=register-email]').type('newEmail@hotmail.com');
    cy.get('[data-cy=register-password').type('testPassword2!');
    cy.get('[data-cy=register-confirm_password').type('differentPassword');
    cy.get('[data-cy=register-button').click();
    cy.on('window:alert',(t)=>{
      expect(t).to.equal("Passwords do not match")
    });
  });
});
