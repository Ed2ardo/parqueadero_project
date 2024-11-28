import { useEffect, useState } from "react";
import axios from 'axios';

function Parqueo() {
  const [disponibilidad, setDisponibilidad] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDisponibilidad();
  }, []);

  const fetchDisponibilidad = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/gestion_parqueadero/espacios/');
      setDisponibilidad(response.data);
    } catch (error) {
      console.error("Error al obtener disponibilidad:", error);
      setError("Error al obtener disponibilidad de espacios.");
    }
  };

  return (
    <div className="parqueo">
      <h2>Espacios de Parqueo</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Tipo de Vehículo</th>
            <th>Total Espacios</th>
            <th>Ocupados</th>
            <th>Disponibles</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(disponibilidad).map(([tipo, datos]) => (
            <tr key={tipo}>
              <td>{tipo.charAt(0).toUpperCase() + tipo.slice(1)}</td>
              <td>{datos.total}</td>
              <td>{datos.ocupados}</td>
              <td>{datos.disponibles}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Parqueo;
