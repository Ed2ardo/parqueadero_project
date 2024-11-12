import { useEffect, useState } from "react";
import axios from 'axios';

function Vehiculos() {
  const [vehiculos, setVehiculos] = useState([]);
  const [error, setError] = useState(null);

  // Campos para agregar un nuevo vehículo
  const [marca, setMarca] = useState('');
  const [modelo, setModelo] = useState('');
  const [placa, setPlaca] = useState('');

  // Obtener lista de vehículos
  useEffect(() => {
    fetchVehiculos();
  }, []);

  const fetchVehiculos = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/vehiculos/');
      setVehiculos(response.data);
    } catch (error) {
      console.error("Error al obtener vehículos:", error);
      setError("Error al obtener vehículos");
    }
  };

  // Crear nuevo vehículo
  const handleAddVehiculo = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/vehiculos/', {
        marca,
        modelo,
        placa
      });
      setVehiculos([...vehiculos, response.data]);
      setMarca('');
      setModelo('');
      setPlaca('');
    } catch (error) {
      console.error("Error al agregar vehículo:", error);
      setError("Error al agregar vehículo");
    }
  };

  return (
    <div className="vehiculos">
      <h2>Vehículos</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {vehiculos.map(vehiculo => (
          <li key={vehiculo.id}>
            {vehiculo.marca} - {vehiculo.modelo} - {vehiculo.placa}
          </li>
        ))}
      </ul>

      <h3>Agregar Vehículo</h3>
      <input
        type="text"
        value={marca}
        onChange={(e) => setMarca(e.target.value)}
        placeholder="Marca"
      />
      <input
        type="text"
        value={modelo}
        onChange={(e) => setModelo(e.target.value)}
        placeholder="Modelo"
      />
      <input
        type="text"
        value={placa}
        onChange={(e) => setPlaca(e.target.value)}
        placeholder="Placa"
      />
      <button onClick={handleAddVehiculo}>Agregar</button>
    </div>
  );
}

export default Vehiculos;
