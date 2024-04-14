import React, { useState, useEffect } from "react";
import "./bank_accounts.css";
import { Link } from "react-router-dom";
import NavBar from "./nav";

function BankAccounts() {
  const [cards, setCards] = useState([]);

  useEffect(() => {
    fetchUserCards();
  }, []);

  const fetchUserCards = async () => {
    try {
      const response = await fetch("http://localhost:8000/user_cards/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "same-origin", // Send cookies along with the request
      });
      if (response.ok) {
        const data = await response.json();
        setCards(data.cards);
      } else {
        console.error("Failed to fetch user cards");
      }
    } catch (error) {
      console.error("Error fetching user cards:", error);
    }
  };

  return (
    <div>
      <NavBar />
      <div className="cards-container">
        <h2>Bank Cards</h2>
        <ul className="card-list">
          {cards.map((card, index) => (
            <li key={index}>
              <p className="first">{card.number}</p>
              <p>{card.expiry_date}</p>
            </li>
          ))}
          <li>
            <Link to="/add_card">+ Add new bank card</Link>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default BankAccounts;
