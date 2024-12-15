import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-blue-500 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Gestión de Parqueadero</h1>
        <ul className="flex space-x-4">
          <li>
            <Link to="/" className="hover:text-gray-100">
              Inicio
            </Link>
          </li>
          <li>
            <Link to="/registro-parqueo" className="hover:text-gray-100">
              Registros de Parqueo
            </Link>
          </li>
          <li>
            <Link to="/historico" className="hover:text-gray-100">
              Historico de Parqueo
            </Link>
          </li>
          {/* Agrega más enlaces aquí si es necesario */}
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;