import ReactDOM from "react-dom";
import { useState } from "react";
import axios from "../services/axiosInstance";

function RegistroParqueoForm({ onClose, onRegistroCreado }) {
  const [placa, setPlaca] = useState("");
  const [tipoVehiculo, setTipoVehiculo] = useState("carro");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/gestion_parqueadero/registros/", {
        vehiculo: { placa, tipo: tipoVehiculo },
      });
      onRegistroCreado(response.data);
      setPlaca("");
      setTipoVehiculo("carro");
      onClose();
    } catch (err) {
      setError("Error al crear el registro. Verifica los datos ingresados.");
      console.error(err);
    }
  };

  const modalContent = (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg w-96">
        <h2 className="text-xl font-bold mb-4">Nuevo Registro de Parqueo</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-bold mb-2">Placa del Vehículo</label>
            <input
              type="text"
              value={placa}
              onChange={(e) => setPlaca(e.target.value)}
              className="w-full border border-gray-300 px-3 py-2 rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-bold mb-2">Tipo de Vehículo</label>
            <select
              value={tipoVehiculo}
              onChange={(e) => setTipoVehiculo(e.target.value)}
              className="w-full border border-gray-300 px-3 py-2 rounded"
            >
              <option value="carro">Carro</option>
              <option value="moto">Moto</option>
              <option value="bicicleta">Bicicleta</option>
              <option value="otro">Otro</option>
            </select>
          </div>
          <div className="flex justify-end">
            <button
              type="button"
              onClick={onClose}
              className="bg-gray-500 text-white px-4 py-2 rounded mr-2"
            >
              Cancelar
            </button>
            <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  return ReactDOM.createPortal(modalContent, document.body);
}

export default RegistroParqueoForm;
