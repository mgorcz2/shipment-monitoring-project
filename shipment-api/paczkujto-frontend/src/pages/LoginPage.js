import React, { useState, useEffect } from "react";
import logo from "../assets/logo.png";
import "../styles/LoginPage.css";
import { translate } from "../i18n/index.js";
import { login, isTokenValid } from "../services/authService";
import { getUserByEmail } from "../services/userService";
import { getClientById } from "../services/clientService.js";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isTokenValid()) {
      localStorage.removeItem("token");
    }
  }, []);


  const navigate = useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await login(email, password);
      localStorage.setItem("token", res.data.access_token);

      const userRes = await getUserByEmail(email, res.data.access_token);
      localStorage.setItem("user", JSON.stringify(userRes.data));

    if (userRes.data.role === "client") {
      const clientRes = await getClientById(userRes.data.id, res.data.access_token);
      localStorage.setItem("client_data", JSON.stringify(clientRes.data));
      navigate("/");
    } else {
      window.location.href = "/";
    }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(translate(err.response.data.detail));
      } else if (err.response) {
        setError("Błąd: " + translate(err.response.status));
      } else {
        setError("Brak połączenia z serwerem");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterClick = () => {
    window.location.href = "/register-client";
  };

  return (
    <div className="login-container">
      <img src={logo} alt="Logo" className="login-logo" />
      <h2 className="login-title">Zaloguj się do paczkuj.to</h2>
      <form onSubmit={handleLogin} className="login-form">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
          className="login-input"
          disabled={loading}
        />
        <input
          type="password"
          placeholder="Hasło"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          className="login-input"
          disabled={loading}
        />
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Logowanie..." : "Zaloguj"}
        </button>
        {error && <div className="login-error">{error}</div>}
      </form>
      {loading && <div style={{ marginTop: 16 }}>⏳</div>}
      <div style={{ marginTop: 24, textAlign: "center" }}>
        <button
          type="button"
          className="btn btn-outline"
          style={{
            background: "#fff",
            color: "#00b359",
            border: "1.5px solid #00b359",
            marginTop: 8,
            fontWeight: "bold",
          }}
          onClick={handleRegisterClick}
          disabled={loading}
        >
          Nie masz konta? Zarejestruj się jako klient
        </button>
      </div>
    </div>
  );
}