import React from 'react';
import logo from '../assets/logofundo.png';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">
        <img src={logo} alt="Logo do Site" />
      </div>
      <div className="header-search">
        <input type="text" placeholder="Pesquisar..." />
      </div>
    </header>
  );
};

export default Header;
