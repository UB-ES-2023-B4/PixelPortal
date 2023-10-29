import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyCmnNSJ5Wk5lyTKtNXMBrNUQDpVYrK5sic",
  authDomain: "pixelportal-258d4.firebaseapp.com",
  projectId: "pixelportal-258d4",
  storageBucket: "pixelportal-258d4.appspot.com",
  messagingSenderId: "289369338205",
  appId: "1:289369338205:web:4cb86387430a5f97b0b8b4",
  measurementId: "G-9FQMZNHJGW",
};

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

export { storage };
