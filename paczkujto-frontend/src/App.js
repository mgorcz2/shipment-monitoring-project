import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import ShipmentsPage from "./pages/ShipmentsPage";
import RegisterClientPage from "./pages/RegisterClientPage";
import CreatePackagePage from "./pages/CreatePackagePage";
import ProtectedRoute from "./services/authService";
import AdminPanel from "./pages/AdminPanel";
import './styles/globals.css'; 

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register-client" element={<RegisterClientPage />} />
        
          <Route element={<ProtectedRoute allowedRoles={["client"]} />}>
            <Route path="shipments" element={<ShipmentsPage />} />
            <Route path="create-shipment" element={<CreatePackagePage />} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={["courier"]} />}>
            <Route path="courier-dashboard" element={<p>Panel Kuriera</p>} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
            <Route path="admin" element={<AdminPanel />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
export default App;