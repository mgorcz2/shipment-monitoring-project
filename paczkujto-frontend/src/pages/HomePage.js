import React from "react";
import logo from "../assets/logo.png";
import "../styles/HomePage.css";
import { useNavigate } from "react-router-dom";
import { isTokenValid, getUserRole } from "../services/authService";

export default function HomePage() {
  const navigate = useNavigate();
  const user = isTokenValid() ? JSON.parse(localStorage.getItem("user")) : null;
  const client_data = isTokenValid() ? JSON.parse(localStorage.getItem("client_data")) : null;
  const userRole = getUserRole();

  const getWelcomeMessage = () => {
    if (!user) return "Witamy w paczkuj.to";
    
    if (client_data && client_data.first_name) {
      return `Witaj, ${client_data.first_name}!`;
    }
    
    if (userRole === "admin") {
      return `Witaj, ${user.email}!`;
    }

    if (userRole === "manager") {
      return `Witaj, ${user.email}!`;
    }

    return `Witaj, ${user.email}!`;
  };

  return (
    <div className="home-container">
      <img src={logo} alt="Logo" className="home-logo" />
      <h1 className="home-title">{getWelcomeMessage()}</h1>
      <p style={{ color: "#444", marginBottom: 32, fontSize: 18, textAlign: "center" }}>
        Szybko i wygodnie nadaj przesyłkę lub sprawdź status swoich paczek.
      </p>
      {isTokenValid() ? (
        <div style={{ display: "flex", gap: 24 }}>
          {userRole === "client" && (
            <>
              <button
                className="btn btn-primary"
                style={{ fontSize: 20, padding: "18px 40px" }}
                onClick={() => navigate("/create-shipment")}
              >
                Nadaj paczkę
              </button>
              <button
                className="btn btn-primary"
                style={{ fontSize: 20, padding: "18px 40px" }}
                onClick={() => navigate("/shipments")}
              >
                Moje paczki
              </button>
            </>
          )}

          {(userRole === "courier" || userRole === "manager" || userRole === "admin") && (
            <button
              className="btn btn-primary"
              style={{ fontSize: 20, padding: "18px 40px" }}
              onClick={() =>
                navigate(userRole === "courier" ? "/courier-shipments" : "/manager-shipments")
              }
            >
              Zarządzaj przesyłkami
            </button>
          )}

          <button
            className="btn btn-primary"
            style={{ fontSize: 20, padding: "18px 40px" }}
            onClick={() => navigate("/track")}
          >
            Śledź przesyłkę
          </button>
          {userRole === "admin" && (
            <button
              className="btn btn-primary"
              style={{ fontSize: 20, padding: "18px 40px" }}
              onClick={() => navigate("/admin")}
            >
              Zarządzaj użytkownikami
            </button>
          )}
        </div>
      ) : (
        <div style={{ display: "flex", gap: 24 }}>
          <button
            className="btn btn-primary"
            style={{ fontSize: 20, padding: "18px 40px" }}
            onClick={() => navigate("/login")}
          >
            Zaloguj się
          </button>
          <button
            className="btn btn-primary"
            style={{ fontSize: 20, padding: "18px 40px" }}
            onClick={() => navigate("/track")}
          >
            Śledź przesyłkę
          </button>
        </div>
      )}
    </div>
  );
}