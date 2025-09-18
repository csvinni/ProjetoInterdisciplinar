                                                                         import React from 'react';
import './Historico.css';

const Historico = () => {
  return (
    <div className="historico-wrapper">
      <section className="historico-section">
        <h2>Histórico</h2>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Nome Doador</th>
                <th>Campanha</th>
                <th>Data doação</th>
                <th>Tipo doação</th>
                <th>Valor</th>
                <th>Quantidade de itens</th>
                <th>Descrição</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Nome</td>
                <td>Qual campanha</td>
                <td>DD/MM/AAAA</td>
                <td>itens/valor</td>
                <td>$</td>
                <td>Quantidade de itens</td>
                <td>Descrição</td>
              </tr>
              <tr>
                <td>Nome</td>
                <td>Qual campanha</td>
                <td>DD/MM/AAAA</td>
                <td>itens/valor</td>
                <td>$</td>
                <td>Quantidade de itens</td>
                <td>Descrição</td>
              </tr>
              <tr>
                <td>Nome</td>
                <td>Qual campanha</td>
                <td>DD/MM/AAAA</td>
                <td>itens/valor</td>
                <td>$</td>
                <td>Quantidade de itens</td>
                <td>Descrição</td>
              </tr>
              <tr>
                <td>Nome</td>
                <td>Qual campanha</td>
                <td>DD/MM/AAAA</td>
                <td>itens/valor</td>
                <td>$</td>
                <td>Quantidade de itens</td>
                <td>Descrição</td>
              </tr>
              <tr>
                <td>Nome</td>
                <td>Qual campanha</td>
                <td>DD/MM/AAAA</td>
                <td>itens/valor</td>
                <td>$</td>
                <td>Quantidade de itens</td>
                <td>Descrição</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};

export default Historico;