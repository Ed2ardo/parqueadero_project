import { useEffect, useState } from "react";
import axios from "../services/axiosInstance";
import { format } from "date-fns";
import RegistroParqueoForm from "../components/RegistroParqueoForm";
import Layout from "../components/Layout";
import { Link } from "react-router-dom";
import RegistrarSalidaButton from "../components/RegistrarSalidaButton";

function RegistroParqueoPage() {
  const [registros, setRegistros] = useState([]);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);

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
    return cobro !== null ? `$${cobro.toFixed(2)}` : "Pendiente";
  };

  const onSalidaRegistrada = (registroId) => {
    setRegistros((prev) =>
      prev.map((registro) =>
        registro.id === registroId
          ? { ...registro, fecha_salida: new Date() } // Actualiza solo este registro
          : registro
      )
    );
  };

  const handleRegistroCreado = (nuevoRegistro) => {
    setRegistros((prev) => [nuevoRegistro, ...prev]);
  };

  const registrosActivos = registros.filter((registro) => !registro.fecha_salida);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Registros de Parqueo</h2>
      <button
        onClick={() => setMostrarFormulario(true)}
        className="bg-green-500 text-white px-4 py-2 rounded mb-4"
      >
        Nuevo Registro
      </button>
      {registrosActivos.length === 0 ? (
        <p className="text-gray-500">No hay vehículos actualmente parqueados.</p>
      ) : (
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
                  {registro && !registro.fecha_salida && (
                    <RegistrarSalidaButton
                      registroId={registro.id}
                      onSalidaRegistrada={onSalidaRegistrada}
                    />
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {mostrarFormulario && (
        <RegistroParqueoForm
          onClose={() => setMostrarFormulario(false)}
          onRegistroCreado={handleRegistroCreado}
        />
      )}
    </div>
  );
}

export default function RegistroParqueo() {
  return (
    <Layout>
      <RegistroParqueoPage />
    </Layout>
  );
}
