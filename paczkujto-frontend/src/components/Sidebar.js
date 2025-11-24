import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import logo from "../assets/logo.png";
import "../styles/Sidebar.css";
import { logout, isLoggedIn } from "../services/authService";
import { getUserRole } from "../services/authService";
import { FaSignOutAlt, FaPhone, FaThLarge, FaComments, FaTruck, FaCalendarAlt, FaUser, FaUserShield } from "react-icons/fa";

const menuItems = [
  { 
    id: "contact",
    icon: <FaPhone />, 
    path: "/contact", 
    allowedRoles: ["client", "courier", "admin", "manager"] 
  },
  { 
    id: "shipments",
    icon: <FaTruck />, 
    pathByRole: {
      client: "/shipments",
      courier: "/courier-shipments",
      admin: "/manager-shipments",
      manager: "/manager-shipments"
    },
    allowedRoles: ["client", "courier", "admin", "manager"] 
  },
  { 
    id: "messages",
    icon: <FaComments />, 
    path: "/messages", 
    allowedRoles: ["client", "manager", "admin"] 
  },
  { 
    id: "calendar",
    icon: <FaCalendarAlt />, 
    path: "/calendar", 
    allowedRoles: ["client", "courier", "admin"]
  },
  { 
    id: "profile",
    icon: <FaUser />, 
    path: "/profile", 
    allowedRoles: ["client", "courier", "admin", "manager"]
  },
  { 
    id: "admin",
    icon: <FaUserShield />, 
    path: "/admin", 
    allowedRoles: ["admin"]
  },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const userRole = getUserRole() || ""; 

  return (
    <div className="sidebar">
      <div className="sidebar-logo" onClick={() => navigate("/")}>
        <img src={logo} alt="Logo" style={{ cursor: "pointer" }} />
      </div>
      {isLoggedIn() && (
      <nav className="sidebar-nav">
        {menuItems
          .filter(item => item.allowedRoles.includes(userRole))
          .map((item) => {
            const itemPath = item.pathByRole ? item.pathByRole[userRole] : item.path;
            const isActive = location.pathname === itemPath;
            return (
              <button
                key={item.id}
                className={`sidebar-btn${isActive ? " active" : ""}`}
                onClick={() => navigate(itemPath)}
                title={item.id.charAt(0).toUpperCase() + item.id.slice(1)}
              >
                {item.icon}
              </button>
            );
          })
        }
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