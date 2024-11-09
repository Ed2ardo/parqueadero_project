import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from './pages/Login';
import Clientes from './pages/Clientes';
import Facturas from './pages/Facturas';
import Parqueo from './pages/Parqueo';

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/clientes" element={<Clientes />} />
        <Route path="/facturas" element={<Facturas />} />
        <Route path="/parqueo" element={<Parqueo />} />
      </Routes>
    </Router>
  )
}

export default App
