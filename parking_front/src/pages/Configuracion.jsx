import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Configuracion = () => {
  const [tarifas, setTarifas] = useState([]);
  const [tipoVehiculo, setTipoVehiculo] = useState('');
  const [costoPorHora, setCostoPorHora] = useState('');

  useEffect(() => {
    axios.get('/api/tarifas/')
      .then(response => setTarifas(response.data))
      .catch(error => console.error('Error al cargar tarifas:', error));
  }, []);

  const handleAgregarTarifa = (e) => {
    e.preventDefault();
    axios.post('/api/tarifas/', { tipo_vehiculo: tipoVehiculo, costo_por_hora: costoPorHora })
      .then(response => {
        setTarifas([...tarifas, response.data]);
        setTipoVehiculo('');
        setCostoPorHora('');
      })
      .catch(error => console.error('Error al agregar tarifa:', error));
  };

  return (
    <div>
      <h2>Configuración de Tarifas</h2>
      <form onSubmit={handleAgregarTarifa}>
        <label>
          Tipo de Vehículo:
          <select value={tipoVehiculo} onChange={(e) => setTipoVehiculo(e.target.value)}>
            <option value="">Seleccione un tipo</option>
            <option value="carro">Carro</option>
            <option value="moto">Moto</option>
            <option value="camioneta">Camioneta</option>
            <option value="bici">Bicicleta</option>
            <option value="otro">Otro</option>
          </select>
        </label>
        <label>
          Costo por Hora:
          <input type="number" value={costoPorHora} onChange={(e) => setCostoPorHora(e.target.value)} />
        </label>
        <button type="submit">Agregar Tarifa</button>
      </form>

      <h3>Listado de Tarifas</h3>
      <table>
        <thead>
          <tr>
            <th>Tipo de Vehículo</th>
            <th>Costo por Hora</th>
          </tr>
        </thead>
        <tbody>
          {tarifas.map(tarifa => (
            <tr key={tarifa.id}>
              <td>{tarifa.tipo_vehiculo}</td>
              <td>{tarifa.costo_por_hora}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Configuracion;
