# !/bin/bash

if [ -f backend/test.db ]; then
  echo "Removing existing test.db file..."
  rm backend/test.db
fi

cd backend
uvicorn main:app --reload > /dev/null 2>&1 &

cd ..
echo $! > uvicorn_pid.txt
echo "uvicorn started with PID: $(cat uvicorn_pid.txt)"

cd frontend
npm run serve > /dev/null 2>&1 &

cd ..
echo $! > npm_pid.txt
echo "npm run serve started with PID: $(cat npm_pid.txt)"

sleep 5

cd frontend
npx cypress run --spec "cypress/e2e/*.spec.cy.js"

cd ..
uvicorn_pid=$(cat uvicorn_pid.txt)
npm_pid=$(cat npm_pid.txt)
kill $uvicorn_pid
kill $npm_pid

rm uvicorn_pid.txt
rm npm_pid.txt

cd backend
#rm test.db

echo "Test completed."

exit $cypress_exit_status