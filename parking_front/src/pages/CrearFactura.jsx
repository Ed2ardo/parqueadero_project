import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CrearFactura = () => {
  const [clientes, setClientes] = useState([]);
  const [registros, setRegistros] = useState([]);
  const [clienteSeleccionado, setClienteSeleccionado] = useState('');
  const [registroSeleccionado, setRegistroSeleccionado] = useState('');

  useEffect(() => {
    axios.get('/api/clientes/')
      .then(response => setClientes(response.data))
      .catch(error => console.error('Error al cargar clientes:', error));

    axios.get('/api/registros_parqueo/')
      .then(response => setRegistros(response.data))
      .catch(error => console.error('Error al cargar registros de parqueo:', error));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('/api/facturas/', {
      cliente: clienteSeleccionado,
      registro_parqueo: registroSeleccionado
    })
      .then(response => {
        console.log('Factura creada:', response.data);
      })
      .catch(error => console.error('Error al crear factura:', error));
  };

  return (
    <div>
      <h2>Crear Factura</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Cliente:
          <select onChange={e => setClienteSeleccionado(e.target.value)} value={clienteSeleccionado}>
            <option value="">Seleccione un cliente</option>
            {clientes.map(cliente => (
              <option key={cliente.id} value={cliente.id}>{cliente.nombre}</option>
            ))}
          </select>
        </label>
        <label>
          Registro de Parqueo:
          <select onChange={e => setRegistroSeleccionado(e.target.value)} value={registroSeleccionado}>
            <option value="">Seleccione un registro</option>
            {registros.map(registro => (
              <option key={registro.id} value={registro.id}>{registro.vehiculo} - {registro.fecha_entrada}</option>
            ))}
          </select>
        </label>
        <button type="submit">Crear Factura</button>
      </form>
    </div>
  );
};

export default CrearFactura;
