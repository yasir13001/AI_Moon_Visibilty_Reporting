import React from 'react';
import './Header.css'; // import stylesheet

const Header = () => {
  return (
    <header className="header">
      <h1 className="header-title">MoonAI</h1>
      <p className="header-subtitle">
An open-source organization dedicated to developing AI tools for lunar astronomical calculations.
      </p>
    </header>
  );
};

export default Header;
