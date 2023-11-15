describe('Login functionality', () => {
  it('should log in with valid credentials', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=login-email]').type('jhwan818@gmail.com');
    cy.get('[data-cy=login-password]').type('Zmfltmaktm1@');
    cy.get('[data-cy=login-button]').click();
    cy.url().should('include', '/home');
  });

  it('should show an error with invalid credentials', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=login-email]').type('invalid-email');
    cy.get('[data-cy=login-password]').type('invalid-password');
    cy.get('[data-cy=login-button]').click();
    cy.on('window:alert',(t)=>{
      expect(t).to.equal("Email is not valid")
   })
  });
});
