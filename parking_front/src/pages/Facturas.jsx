import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Facturas = () => {
  const [facturas, setFacturas] = useState([]);

  useEffect(() => {
    axios.get('/api/facturas/')
      .then(response => setFacturas(response.data))
      .catch(error => console.error('Error al cargar facturas:', error));
  }, []);

  return (
    <div>
      <h2>Listado de Facturas</h2>
      <table>
        <thead>
          <tr>
            <th>Cliente</th>
            <th>Registro de Parqueo</th>
            <th>Tarifa</th>
            <th>Tiempo Total</th>
            <th>Monto</th>
            <th>Fecha de Emisión</th>
          </tr>
        </thead>
        <tbody>
          {facturas.map(factura => (
            <tr key={factura.id}>
              <td>{factura.cliente}</td>
              <td>{factura.registro_parqueo}</td>
              <td>{factura.tarifa}</td>
              <td>{factura.tiempo_total}</td>
              <td>{factura.monto}</td>
              <td>{new Date(factura.fecha_emision).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Facturas;
