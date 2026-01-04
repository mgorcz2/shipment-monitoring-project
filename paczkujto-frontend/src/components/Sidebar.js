import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import logo from "../assets/logo_small.png";
import "../styles/Sidebar.css";
import { logout, isLoggedIn } from "../services/authService";
import { getUserRole } from "../services/authService";
import { FaSignOutAlt, FaPhone, FaTruck, FaUser, FaUserShield } from "react-icons/fa";

const menuItems = [
  {
    id: "contact",
    icon: <FaPhone />,
    path: "/contact",
    allowedRoles: ["", "client", "courier", "admin", "manager"],
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
        <img src={logo} alt="Logo" style={{ cursor: "pointer" , width: "70%"}} />
      </div>
      <nav className="sidebar-nav">
        {menuItems
          .filter(item => item.allowedRoles.includes(userRole))
          .map((item) => {
            const itemPath = item.pathByRole ? item.pathByRole[userRole] : item.path;
            const isActive = Boolean(itemPath) && location.pathname === itemPath;
            return (
              <button
                key={item.id}
                className={`sidebar-btn${isActive ? " active" : ""}`}
                onClick={() => {
                  if (itemPath) navigate(itemPath);
                }}
                title={item.id.charAt(0).toUpperCase() + item.id.slice(1)}
              >
                {item.icon}
              </button>
            );
          })
        }
      </nav>

      {isLoggedIn() && (
        <button className="sidebar-btn" onClick={logout} title="Wyloguj" style={{ marginBottom: 24 }}>
          <FaSignOutAlt />
        </button>
      )}
    </div>
  );
}