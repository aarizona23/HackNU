// add_cards.js

import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./add_card.css";
import NavBar from "./nav";

function AddCard(props) {
  const [bankName, setBankName] = useState("");
  const [cardType, setCardType] = useState("");
  const [cardNumber, setCardNumber] = useState("");
  const [expirationDate, setExpirationDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/add_user_cards/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": props.csrfToken, // Include CSRF token for POST requests
        },
        body: JSON.stringify({
          bank_name: bankName,
          card_type: cardType,
          card_number: cardNumber,
          expiration_date: expirationDate,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          history.push("/my_cards");
        } else {
          // Handle errors from the server
          console.error("Failed to add bank card:", data.errors);
        }
      } else {
        // Handle HTTP errors
        console.error("Failed to add bank card:", response.statusText);
      }
    } catch (error) {
      console.error("Error adding bank card:", error);
    }
  };

  return (
    <div>
      <NavBar />
      <div className="login-container">
        <div className="login-box">
          <h2>Add Card</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label>Bank name:</label>
              <input
                type="text"
                value={bankName}
                onChange={(e) => setBankName(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label>Card Type:</label>
              <input
                type="text"
                value={cardType}
                onChange={(e) => setCardType(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label>Card Number:</label>
              <input
                type="text"
                value={cardNumber}
                onChange={(e) => setCardNumber(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label>Expiration Date:</label>
              <input
                type="date"
                value={expirationDate}
                onChange={(e) => setExpirationDate(e.target.value)}
                required
              />
            </div>
            <button type="submit">Add bank card</button>
          </form>
          <div className="link-container">
            <Link to="/my_cards" className="link">
              Back to my bank cards
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AddCard;
