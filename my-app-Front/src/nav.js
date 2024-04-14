import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./nav.css";

function NavBar() {
  return (
    <div className="nav-bar">
      <ul>
        <li>
          <Link to="/cashbacks">Home</Link>
        </li>
        <li>
          <button>Ariana</button>
        </li>
      </ul>
    </div>
  );
}

export default NavBar;
