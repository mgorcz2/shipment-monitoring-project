import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import ShipmentsPage from "./pages/ShipmentsPage";
import RegisterClientPage from "./pages/RegisterClientPage";
import CreatePackagePage from "./pages/CreatePackagePage";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="shipments" element={<ShipmentsPage />} />
          <Route index element={<HomePage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register-client" element={<RegisterClientPage />} />
          <Route path="create-shipment" element={<CreatePackagePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;