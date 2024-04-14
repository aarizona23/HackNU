import React, { useState } from "react";
import "./register_main.css";
import { Link, useNavigate } from 'react-router-dom';

function RegisterWindowMain() {
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const navigate = useNavigate();

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePassword1Change = (e) => {
    setPassword1(e.target.value);
  };

  const handlePassword2Change = (e) => {
    setPassword2(e.target.value);
  };
  const [error, setError] = useState(""); // Add state for error
  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:8000/register_user/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        step: '1', // Add the step information
        email: email,
        password1: password1,
        password2: password2
      }),
    });
    const data = await response.json();
    if (data.success == false) {
      setError(data.errors ? data.errors.join(", ") : "Unknown error occurred");
      
    } 
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Registration Step #1</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={handleEmailChange}
              required
            />
          </div>
          <div className="input-group">
            <label>Password:</label>
            <input
              type="password"
              value={password1}
              onChange={handlePassword1Change}
              required
            />
          </div>
          <div className="input-group">
            <label>Confirm Password:</label>
            <input
              type="password"
              value={password2}
              onChange={handlePassword2Change}
              required
            />
          </div>
          <button type="submit">Continue</button>
        </form>
        <div className="link-container">
          <Link to="/" className="link">
            Login instead
          </Link>
        </div>
      </div>
    </div>
  );
}

export default RegisterWindowMain;
