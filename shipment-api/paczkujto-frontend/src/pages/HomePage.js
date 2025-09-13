import React, { useState } from "react";
import logo from "../assets/logo.png";
import "../styles/HomePage.css";
import { useNavigate } from "react-router-dom";
import { isTokenValid, getToken } from "../services/authService";
import axios from "axios";

export default function HomePage() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  const handleGetUsers = async () => {
    setError("");
    setUsers([]);
    try {
      const res = await axios.get("http://localhost:8000/users/all", {
        headers: {
          Authorization: `Bearer ${getToken()}`
        }
      });
      setUsers(res.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else if (err.response) {
        setError("Błąd: " + err.response.status);
      } else {
        setError("Brak połączenia z serwerem");
      }
    }
  };

  return (
    <div className="home-container">
      <img src={logo} alt="Logo" className="home-logo" />
      <h1 className="home-title">Witamy w paczkuj.to</h1>
      {!isTokenValid() && (
        <button className="home-login-btn" onClick={() => navigate("/login")}>
          Zaloguj
        </button>
      )}
      {isTokenValid() && (
        <button className="home-login-btn" onClick={handleGetUsers}>
          Pobierz wszystkich użytkowników
        </button>
      )}
      {error && <div style={{ color: "red", marginTop: 16 }}>{error}</div>}
      {users.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <h3>Użytkownicy:</h3>
          <ul>
            {users.map((user) => (
              <li key={user.id || user.email}>{user.email || JSON.stringify(user)}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}