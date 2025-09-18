import React, { useState } from 'react';
import { MdMenu, MdClose, MdExpandMore, MdExpandLess } from 'react-icons/md';
import './Sidebar.css';
import logo from '../assets/logofundo.png';  // importe a logo

const Sidebar = ({ isOpen, toggleSidebar }) => {
  const [cadastroOpen, setCadastroOpen] = useState(false);
  const [historicoOpen, setHistoricoOpen] = useState(false);
  const [doacoesOpen, setDoacoesOpen] = useState(false); // novo submenu

  const toggleCadastro = () => {
    setCadastroOpen(!cadastroOpen);
  };

  const toggleDoacoes = () => {
    setDoacoesOpen(!doacoesOpen);
  };

  const toggleHistorico = () => {
    setHistoricoOpen(!historicoOpen);
  };

  return (
    <>
      <button className="toggle-button" onClick={toggleSidebar} aria-label={isOpen ? 'Fechar sidebar' : 'Abrir sidebar'}>
        {isOpen ? <MdClose size={24} /> : <MdMenu size={24} />}
      </button>

      <nav className={`sidebar ${isOpen ? 'open' : ''}`}>

        <div
          className="sidebar-link with-submenu"
          onClick={toggleCadastro}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => { if(e.key === 'Enter') toggleCadastro(); }}
        >
          Cadastro
          <span className="submenu-icon">
            {cadastroOpen ? <MdExpandLess /> : <MdExpandMore />}
          </span>
        </div>
        {cadastroOpen && (
          <div className="submenu">
            <a href="#" className="sidebar-sublink">Campanhas</a>
            <a href="#" className="sidebar-sublink">Doações</a>
            <a href="#" className="sidebar-sublink">Doador</a>
          </div>
        )}

        {/* Novo submenu Relatórios */}
        <div
          className="sidebar-link with-submenu"
          onClick={toggleDoacoes}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => { if(e.key === 'Enter') toggleDoacoes(); }}
        >
          Doações
          <span className="submenu-icon">
            {doacoesOpen ? <MdExpandLess /> : <MdExpandMore />}
          </span>
        </div>
        {doacoesOpen && (
          <div className="submenu">
            <a href="#" className="sidebar-sublink">Listar</a>
            <a href="#" className="sidebar-sublink">Últimas doações</a>
          </div>
        )}

         <div
          className="sidebar-link with-submenu"
          onClick={toggleHistorico}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => { if(e.key === 'Enter') toggleHistorico(); }}
        >
          Histórico
          <span className="submenu-icon">
            {doacoesOpen ? <MdExpandLess /> : <MdExpandMore />}
          </span>
        </div>
        {historicoOpen && (
          <div className="submenu">
            <a href="#" className="sidebar-sublink">Campanhas</a>
            <a href="#" className="sidebar-sublink">Doações</a>
          </div>
        )}

      </nav>
    </>
  );
};

export default Sidebar;
