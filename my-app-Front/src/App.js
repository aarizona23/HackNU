import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Registration from "./register.js";
import LoginPage from "./login";
import BankAccounts from "./bank_accounts";
import AddCard from "./add_card.js";
import CashbackPage from "./cashback.js";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route exact path="/" Component={LoginPage} />
          <Route path="/register" Component={Registration} />
          <Route path="/login" Component={LoginPage} />
          <Route path="/my_cards" Component={BankAccounts} />
          <Route path="/add_card" Component={AddCard}></Route>
          <Route path="/cashbacks" Component={CashbackPage}></Route>
        </Routes>
      </div>
    </Router>

    // <BankAccounts/>
    // <LoginPage/>
    /* {} */
  );
}

export default App;
