import { useEffect, useState } from "react";
import axios from "../services/axiosInstance";
import { format } from "date-fns";
import Layout from "../components/Layout";
import { Link } from "react-router-dom";


function HistoricoParqueoPage() {
  const [registros, setRegistros] = useState([]);

  useEffect(() => {
    const fetchRegistros = async () => {
      try {
        const response = await axios.get("/gestion_parqueadero/registros/");
        setRegistros(response.data);
      } catch (error) {
        console.error("Error al cargar los registros:", error);
      }
    };

    fetchRegistros();
  }, []);

  const formatearFecha = (fecha) => {
    return fecha ? format(new Date(fecha), "dd/MM/yyyy, hh:mm a") : "Pendiente";
  };

  const formatearCobro = (cobro) => {
    return `$${Number(cobro).toFixed(2)}`;
  };


  const registrosActivos = registros.filter((registro) => registro.fecha_salida);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Registros de Parqueo</h2>
      <table className="table-auto w-full border-collapse border border-gray-300">
        <thead>
          <tr>
            <th className="border border-gray-300 p-2">Placa</th>
            <th className="border border-gray-300 p-2">Entrada</th>
            <th className="border border-gray-300 p-2">Cobro</th>
            <th className="border border-gray-300 p-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {registrosActivos.map((registro) => (
            <tr key={registro.id}>
              <td className="border border-gray-300 p-2">
                <Link
                  to={`/registros/${registro.id}`}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
                >
                  {registro.vehiculo.placa}
                </Link>
              </td>
              <td className="border border-gray-300 p-2">
                {formatearFecha(registro.fecha_entrada)}
              </td>
              <td className="border border-gray-300 p-2">
                {formatearCobro(registro.total_cobro)}
              </td>
              <td className="border border-gray-300 p-2">
                {formatearFecha(registro.fecha_entrada)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function HistoricoParqueo() {
  return (
    <Layout>
      <HistoricoParqueoPage />
    </Layout>
  );
}
