// src/components/Layout.js
import Navbar from "./Navbar"; // Importa el componente Navbar

function Layout({ children }) {
  return (
    <div>
      <Navbar /> {/* Incluye la barra de navegación */}
      <main className="container mx-auto mt-8">
        {/* {children} representa el contenido específico de cada página */}
        {children}
      </main>
    </div>
  );
}

export default Layout;