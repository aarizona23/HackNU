import React, { useState } from "react";
import "./register_extra.css";
import { Link, useNavigate } from 'react-router-dom';

function RegisterWindowExtra() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [telephone, setTelephone] = useState("");
  const [address, setAddress] = useState("");
  const navigate = useNavigate();

  const handleFirstNameChange = (e) => {
    setFirstName(e.target.value);
  };

  const handleLastNameChange = (e) => {
    setLastName(e.target.value);
  };

  const handleTelephoneChange = (e) => {
    setTelephone(e.target.value);
  };

  const handleAddressChange = (e) => {
    setAddress(e.target.value);
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
        step: '2', // Add the step information
        first_name: firstName,
        last_name: lastName,
        telephone: telephone,
        address: address
      }),
    });
    const data = await response.json();
    if (data.success) {
      navigate('/my_cards');
    } else {
      setError(data.errors ? data.errors.join(", ") : "Unknown error occurred");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Registration Step #2</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>First Name:</label>
            <input
              type="text"
              value={firstName}
              onChange={handleFirstNameChange}
              required
            />
          </div>
          <div className="input-group">
            <label>Last Name:</label>
            <input
              type="text"
              value={lastName}
              onChange={handleLastNameChange}
              required
            />
          </div>
          <div className="input-group">
            <label>Telephone:</label>
            <input
              type="tel"
              value={telephone}
              onChange={handleTelephoneChange}
              required
            />
          </div>
          <div className="input-group">
            <label>Address:</label>
            <input
              type="text"
              value={address}
              onChange={handleAddressChange}
              required
            />
          </div>
          <button type="submit">Submit</button>
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

export default RegisterWindowExtra;
