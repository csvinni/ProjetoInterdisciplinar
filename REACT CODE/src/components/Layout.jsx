import React from 'react';
import { Link } from 'react-router-dom';

const Layout = ({ children }) => {
  return (
    <div class="container">
      <header>
         <div class="logo">
            <img src="./src/assets/logo.png" alt="Logo" class="logo-img" />
            <span class="logo-text">Gerenciador de Doações e Campanhas Beneficente</span>
        </div>
        <div class="header-actions">
                <Link to="/cadastro" className="register-btn">Cadastre agora a sua ONG</Link>
                <div class="user-icon">
                    <i class="fa-solid fa-user"></i>
                </div>
        </div>
      </header>

      <main>
        {children}
      </main>

      <footer>
      </footer>
    </div>
  );
};

export default Layout;