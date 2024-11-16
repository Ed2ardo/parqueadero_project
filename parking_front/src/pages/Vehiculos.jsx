import { useEffect, useState } from "react";
import axios from 'axios';

function Vehiculos() {
  const [vehiculos, setVehiculos] = useState([]);
  const [error, setError] = useState(null);

  // Campos para agregar un nuevo vehículo
  const [placa, setPlaca] = useState('');
  const [tipo, setTipo] = useState('');
  const [hora_entrada, setHoraEntrada] = useState('');
  const [cliente, setCliente] = useState('');
  const [espacio, setEspacio] = useState('');


  // Obtener lista de vehículos
  useEffect(() => {
    fetchVehiculos();
  }, []);

  const fetchVehiculos = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/gestion_parqueadero/vehiculos/');
      setVehiculos(response.data);
    } catch (error) {
      console.error("Error al obtener vehículos:", error);
      setError("Error al obtener vehículos");
    }
  };

  // Crear nuevo vehículo
  const handleAddVehiculo = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/gestion_parqueadero/vehiculos/', {
        placa,
        tipo,
        hora_entrada,
        cliente,
        espacio
      });
      setVehiculos([...vehiculos, response.data]);
      setPlaca('');
      setTipo('');
      setHoraEntrada('');
      setCliente('');
      setEspacio('');
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
            <p>{vehiculo.placa} - {vehiculo.tipo} -{vehiculo.hora_entrada} - {vehiculo.cliente} - {vehiculo.espacio ? vehiculo.espacio.numero_espacio : "espacio sin asignar"}</p>
          </li>
        ))}
      </ul>

      <h3>Agregar Vehículo</h3>
      <input
        type="text"
        value={placa}
        onChange={(e) => setPlaca(e.target.value)}
        placeholder="Placa"
      />
      <input
        type="text"
        value={tipo}
        onChange={(e) => setTipo(e.target.value)}
        placeholder="Tipo"
      />
      <input
        type="text"
        value={hora_entrada}
        onChange={(e) => setHoraEntrada(e.target.value)}
        placeholder="Hora entrada"
      />
      <input
        type="text"
        value={cliente}
        onChange={(e) => setCliente(e.target.value)}
        placeholder="Cliente"
      />
      <input
        type="text"
        value={espacio}
        onChange={(e) => setEspacio(e.target.value)}
        placeholder="espacio"
      />
      <button onClick={handleAddVehiculo}>Agregar</button>
    </div>
  );
}

export default Vehiculos;
