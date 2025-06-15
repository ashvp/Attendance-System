// src/App.tsx
// import React from "react";
import GoogleLoginButton from "./components/GoogleLoginButton.tsx";

function App() {
  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Firebase Auth Test</h2>
      <GoogleLoginButton />
    </div>
  );
}

export default App;
