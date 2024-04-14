import React, { useState } from "react";
import RegisterWindowMain from "./register_main.js";
import RegisterWindowExtra from "./register_extra.js";

function Registration() {
  const [showExtra, setShowExtra] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    setShowExtra(true);
  };
  
  return (
    <div>
      {showExtra ? (
        <RegisterWindowExtra />
      ) : (
        <RegisterWindowMain onSubmit={handleSubmit} />
      )}
    </div>
  );
}

export default Registration;
