describe('Test login', () => {
  it('valid login', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=login-email]').type('testemail999@hotmail.com');
    cy.get('[data-cy=login-password]').type('testPassword1!');
    cy.get('[data-cy=login-button]').click();
    cy.url().should('include', '/home');
  });

  it('invalid login', () => {
    cy.visit('http://localhost:8080');
    cy.get('[data-cy=login-email]').type('invalid-email'); 
    cy.get('[data-cy=login-password]').type('invalid-password');
    cy.get('[data-cy=login-button]').click();
    cy.on('window:alert',(t)=>{
      expect(t).to.equal("Email is not valid")
   })
  });
});
