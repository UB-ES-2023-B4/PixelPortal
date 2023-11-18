# !/bin/bash
npx cypress run --spec cypress/e2e/register.spec.cy.js
npx cypress run --spec cypress/e2e/login.spec.cy.js
npx cypress run --spec cypress/e2e/upload_image.spec.cy.js