import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import Layout from "../components/Layout";

function HomePage() {
  return (
    <div>
    </div>
  );
}

export default function Home() {
  return (
    <Layout> {/* Envuelve el contenido de HomePage con el Layout */}
      <HomePage />
    </Layout>
  )
}