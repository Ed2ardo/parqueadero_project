import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/HomePage";
import RegistroParqueo from "./pages/RegistroParqueoPage";
import RegistroDetalle from "./pages/RegistroDetallePage"
import HistoricoParqueo from "./pages/HistoricoParqueoPage";


function App() {
  return (
    <Router>
      <div className="container mx-auto p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/registro-parqueo" element={<RegistroParqueo />} />
          <Route path="/registros/:id" element={<RegistroDetalle />} />
          <Route path="/historico" element={<HistoricoParqueo />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
