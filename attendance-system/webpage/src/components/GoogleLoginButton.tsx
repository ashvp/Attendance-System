// src/components/GoogleLoginButton.tsx
import React from "react";
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "../firebase";
import axios from "axios";

const GoogleLoginButton = () => {
  const handleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const user = result.user;
      const token = await user.getIdToken();

      console.log("Firebase token:", token);
      console.log("User:", user.email);

      // Send token to FastAPI
      const response = await axios.post("http://localhost:8000/api/auth/firebase", {
        token
      });

      console.log("Backend response:", response.data);
    } catch (err) {
      console.error("Google Sign-In Error:", err);
    }
  };

  return (
    <button
      onClick={handleLogin}
      style={{
        padding: "10px 20px",
        backgroundColor: "#4285F4",
        color: "white",
        border: "none",
        borderRadius: "5px",
        fontSize: "16px",
        cursor: "pointer"
      }}
    >
      Sign in with Google
    </button>
  );
};

export default GoogleLoginButton;
