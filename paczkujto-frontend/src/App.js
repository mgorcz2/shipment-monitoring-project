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
import CourierShipmentsPage from "./pages/CourierShipmentsPage";
import ManagerShipmentsPage from "./pages/ManagerShipmentsPage";
import ProfilePage from "./pages/ProfilePage";
import TrackShipmentPage from "./pages/TrackShipmentPage";
import './styles/globals.css'; 

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public route without Layout */}
        <Route path="/track" element={<TrackShipmentPage />} />
        <Route path="/track/:id" element={<TrackShipmentPage />} />
        
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register-client" element={<RegisterClientPage />} />
        
          <Route element={<ProtectedRoute allowedRoles={["client", "admin", "manager"]} />}>
            <Route path="shipments" element={<ShipmentsPage />} />
            <Route path="create-shipment" element={<CreatePackagePage />} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={["courier"]} />}>
            <Route path="/courier-shipments" element={<CourierShipmentsPage />} />
            <Route path="courier-dashboard" element={<p>Panel Kuriera</p>} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={["admin", "manager"]} />}>
            <Route path="admin" element={<AdminPanel />} />
            <Route path="manager-shipments" element={<ManagerShipmentsPage />} />
          </Route>

          <Route element={<ProtectedRoute allowedRoles={["client", "courier", "manager", "admin"]} />}>
            <Route path="profile" element={<ProfilePage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
export default App;