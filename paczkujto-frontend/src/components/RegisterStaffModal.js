import React, { useState } from "react";
import { registerUser } from "../services/registerUserService";
import { registerStaff } from "../services/staffService";
import { translate } from "../i18n";
import "../styles/AdminPanel.css";

const RegisterStaffModal = ({ onClose, onSuccess }) => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    role: "courier",
    first_name: "",
    last_name: "",
    phone_number: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

 try {
    const userData = {
      email: form.email,
      password: form.password,
      role: form.role
    };

    const staffData = {
      first_name: form.first_name,
      last_name: form.last_name,
      phone_number: form.phone_number
    };

    await registerStaff(userData, staffData);
      
      if (onSuccess) onSuccess();
      onClose();
    } catch (err) {
      console.error("Błąd podczas rejestracji:", err);
      const detail = err.response?.data?.detail || "Nieznany błąd";
      
      if (Array.isArray(detail)) {
        setError(detail.map(item => typeof item === "object" && item.msg ? item.msg : String(item)).join(" | "));
      } else {
        setError(translate(detail));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Rejestracja Pracownika</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠</span>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <h3>Dane logowania</h3>
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              placeholder="courier@example.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Hasło</label>
            <input
              type="password"
              id="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              required
              placeholder="Minimum 8 znaków"
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">Rola</label>
            <select
              id="role"
              name="role"
              value={form.role}
              onChange={handleChange}
              required
            >
              <option value="courier">Kurier</option>
              <option value="manager">Manager</option>
            </select>
          </div>

          <h3>Dane osobowe</h3>

          <div className="form-group">
            <label htmlFor="first_name">Imię</label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              required
              placeholder="Jan"
            />
          </div>

          <div className="form-group">
            <label htmlFor="last_name">Nazwisko</label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              required
              placeholder="Kowalski"
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone_number">Telefon</label>
            <input
              type="tel"
              id="phone_number"
              name="phone_number"
              value={form.phone}
              onChange={handleChange}
              required
            />
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="cancel-button">
              Anuluj
            </button>
            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? "Rejestrowanie..." : "Zarejestruj"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterStaffModal;