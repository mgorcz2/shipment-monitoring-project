import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import logo from "../assets/logo.png";
import "../styles/Sidebar.css";
import { logout, isLoggedIn } from "../services/authService";
import { FaSignOutAlt, FaPhone, FaThLarge, FaComments, FaTruck, FaCalendarAlt, FaUser, FaCog } from "react-icons/fa";

const menuItems = [
  { icon: <FaPhone />, path: "/contact" },
  { icon: <FaThLarge />, path: "/shipments" },
  { icon: <FaComments />, path: "/messages" },
  { icon: <FaTruck />, path: "/courier" },
  { icon: <FaCalendarAlt />, path: "/calendar" },
  { icon: <FaUser />, path: "/profile" },
  { icon: <FaCog />, path: "/settings" },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="sidebar">
      <div className="sidebar-logo" onClick={() => navigate("/")}>
        <img src={logo} alt="Logo" style={{ cursor: "pointer" }} />
      </div>
      {isLoggedIn() && (
      <nav className="sidebar-nav">
        {menuItems.map((item, idx) => (
          <button
            key={idx}
            className={`sidebar-btn${location.pathname.startsWith(item.path) ? " active" : ""}`}
            onClick={() => navigate(item.path)}
          >
            {item.icon}
          </button>
        ))}
      </nav>
      )}
      {isLoggedIn() && (
        <button className="sidebar-btn" onClick={logout} title="Wyloguj" style={{ marginBottom: 24 }}>
          <FaSignOutAlt />
        </button>
      )}
    </div>
  );
}