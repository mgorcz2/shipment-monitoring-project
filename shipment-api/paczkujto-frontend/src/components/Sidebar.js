import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import "../styles/Sidebar.css";
import { logout, isLoggedIn } from "../services/authService";
import { FaSignOutAlt, FaPhone, FaThLarge, FaComments, FaTruck, FaCalendarAlt, FaUser, FaCog } from "react-icons/fa";



export default function Sidebar() {
  const [active, setActive] = useState(1);
  const navigate = useNavigate();

  return (
    <div className="sidebar">
      <div className="sidebar-logo" onClick={() => navigate("/")}>
        <img src={logo} alt="Logo" style={{ cursor: "pointer" }} />
      </div>
      <nav className="sidebar-nav">
        <button className={`sidebar-btn${active === 0 ? " active" : ""}`} onClick={() => setActive(0)}><FaPhone /></button>
        <button className={`sidebar-btn${active === 1 ? " active" : ""}`} onClick={() => setActive(1)}><FaThLarge /></button>
        <button className={`sidebar-btn${active === 2 ? " active" : ""}`} onClick={() => setActive(2)}><FaComments /></button>
        <button className={`sidebar-btn${active === 3 ? " active" : ""}`} onClick={() => setActive(3)}><FaTruck /></button>
        <button className={`sidebar-btn${active === 4 ? " active" : ""}`} onClick={() => setActive(4)}><FaCalendarAlt /></button>
        <button className={`sidebar-btn${active === 5 ? " active" : ""}`} onClick={() => setActive(5)}><FaUser /></button>
        <button className={`sidebar-btn${active === 6 ? " active" : ""}`} onClick={() => setActive(6)}><FaCog /></button>
      </nav>

{isLoggedIn() && (
  <button className="sidebar-btn" onClick={logout} title="Wyloguj" style={{ marginBottom: 24 }}>
    <FaSignOutAlt />
  </button>
)}
    </div>
  );
}