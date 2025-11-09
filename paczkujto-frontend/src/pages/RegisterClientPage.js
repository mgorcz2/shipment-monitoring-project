import React, { useState } from "react";
import logo from "../assets/logo.png";
import "../styles/RegisterClientPage.css";
import { registerUser } from "../services/userService";
import { registerClient } from "../services/clientService.js";
import { translate } from "../i18n/index.js";

export default function RegisterClientPage() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    address: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

const handleRegister = async e => {
  e.preventDefault();
  setError("");
  setSuccess("");
  setLoading(true);
  
  try {
    const userData = {
      email: form.email,
      password: form.password,
      role: "client"
    };

    const clientData = {
      first_name: form.first_name,
      last_name: form.last_name,
      phone_number: form.phone_number,
      address: form.address
    };

    await registerClient(userData, clientData);

    setSuccess("Rejestracja zakończona sukcesem! Możesz się zalogować.");
    setForm({
      email: "",
      password: "",
      first_name: "",
      last_name: "",
      phone_number: "",
      address: "",
    });
    setTimeout(() => {
      window.location.href = "/login";
    }, 2000);
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      const detail = err.response.data.detail;
      if (Array.isArray(detail)) {
        setError(
          detail
            .map((item) =>
              typeof item === "object" && item.msg
                ? item.msg
                : String(item)
            )
            .join(" | ")
        );
      } else {
        setError(translate(detail));
      }
    } else if (err.response) {
      setError("Błąd: " + translate(err.response.status));
    } else {
      setError("Brak połączenia z serwerem");
    }
  } finally {
    setLoading(false);
  }
  };

  return (
    <div className="register-container">
      <img src={logo} alt="Logo" className="register-logo" />
      <h2 className="register-title">Rejestracja klienta</h2>
      <form onSubmit={handleRegister} className="register-form">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
          className="register-input"
          disabled={loading}
        />
        <input
          type="password"
          name="password"
          placeholder="Hasło"
          value={form.password}
          onChange={handleChange}
          required
          className="register-input"
          disabled={loading}
        />
        <input
          type="text"
          name="first_name"
          placeholder="Imię"
          value={form.first_name}
          onChange={handleChange}
          required
          className="register-input"
          disabled={loading}
        />
        <input
          type="text"
          name="last_name"
          placeholder="Nazwisko"
          value={form.last_name}
          onChange={handleChange}
          required
          className="register-input"
          disabled={loading}
        />
        <input
          type="text"
          name="phone_number"
          placeholder="Telefon"
          value={form.phone_number}
          onChange={handleChange}
          required
          className="register-input"
          disabled={loading}
        />
        <input
          type="text"
          name="address"
          placeholder="Adres"
          value={form.address}
          onChange={handleChange}
          className="register-input"
          disabled={loading}
        />
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Rejestracja..." : "Zarejestruj się"}
        </button>
        {error && <div className="register-error">{error}</div>}
        {success && <div className="register-success">{success}</div>}
      </form>
      {loading && <div style={{ marginTop: 16 }}>⏳</div>}
    </div>
  );
}