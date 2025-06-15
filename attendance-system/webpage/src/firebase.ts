import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCOCBus1vrmko6jMqiBQOoPMsZcWzRvXhg",
  authDomain: "mpta-ymca.firebaseapp.com",
  projectId: "mpta-ymca",
  storageBucket: "mpta-ymca.firebasestorage.app",
  messagingSenderId: "840275516990",
  appId: "1:840275516990:web:c56161a78f939882a33b6f",
  measurementId: "G-GHRRQD5YZ4"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { auth, googleProvider };
