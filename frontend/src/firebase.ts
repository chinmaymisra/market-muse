import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// Replace these with actual values from your Firebase project settings
const firebaseConfig = {
    apiKey: "AIzaSyD81biTG432RL0ZzSsZspAfRNh6A0bqNEg",
    authDomain: "marketmuse-38589.firebaseapp.com",
    projectId: "marketmuse-38589",
    storageBucket: "marketmuse-38589.firebasestorage.app",
    messagingSenderId: "490636455329",
    appId: "1:490636455329:web:978e19e15d9d1b3bfa2fe0"
  };

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();
