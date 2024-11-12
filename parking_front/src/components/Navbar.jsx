import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <ul>
        <li><Link to="/">Inicio</Link></li>
        <li><Link to="/clientes">Clientes</Link></li>
        <li><Link to="/facturas">Facturas</Link></li>
        <li><Link to="/parqueo">Parqueo</Link></li>
        <li><Link to="/vehiculos">Vehículos</Link></li>
        <li><Link to="/login">Login</Link></li>
      </ul>
    </nav>
  );
}


export default Navbar;

