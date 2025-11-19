import React, { useState, useEffect } from "react";
import { getClientById, updateClient } from "../services/clientService";
import { getStaffById, updateStaff } from "../services/staffService";
import "../styles/ShipmentsPage.css";

export default function EditUserModal({ user, onClose, onSuccess }) {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [profileData, setProfileData] = useState(null);
  
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    phone_number: "",
    address: ""
  });

  useEffect(() => {
    fetchProfileData();
  }, [user]);

  const fetchProfileData = async () => {
    setLoading(true);
    setError("");
    
    try {
      if (user.role === "client") {
        const response = await getClientById(user.id);
        const client = response.data;
        setProfileData(client);
        setFormData({
          first_name: client.first_name || "",
          last_name: client.last_name || "",
          phone_number: client.phone_number || "",
          address: client.address || ""
        });
      } else if (user.role === "courier" || user.role === "manager") {
        const response = await getStaffById(user.id);
        const staff = response.data;
        setProfileData(staff);
        setFormData({
          first_name: staff.first_name || "",
          last_name: staff.last_name || "",
          phone_number: staff.phone_number || "",
          address: ""
        });
      } else {
        setError("Nie można edytować użytkownika z rolą: " + user.role);
      }
    } catch (err) {
      console.error("Błąd pobierania danych:", err);
      setError("Nie udało się pobrać danych użytkownika");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");

    try {
      if (user.role === "client") {
        await updateClient(user.id, formData);
      } else if (user.role === "courier" || user.role === "manager") {
        const { address, ...staffData } = formData;
        await updateStaff(user.id, staffData);
      }
      
      onSuccess();
      onClose();
    } catch (err) {
      console.error("Błąd zapisywania:", err);
      setError(err.response?.data?.detail || "Nie udało się zapisać zmian");
    } finally {
      setSaving(false);
    }
  };

  if (!user) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close-btn" onClick={onClose}>×</button>
        
        <h2>Edytuj użytkownika</h2>
        
        <div className="shipment-info" style={{ marginBottom: '1.5rem' }}>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Rola:</strong> {getRoleName(user.role)}</p>
        </div>

        {loading ? (
          <div className="loading-text">Ładowanie danych...</div>
        ) : error && !profileData ? (
          <div className="error-text">{error}</div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="first_name">Imię:</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="form-input"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="last_name">Nazwisko:</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="form-input"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="phone_number">Telefon:</label>
              <input
                type="tel"
                id="phone_number"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleInputChange}
                className="form-input"
                placeholder="+48123456789"
                required
              />
            </div>

            {user.role === "client" && (
              <div className="form-group">
                <label htmlFor="address">Adres:</label>
                <input
                  type="text"
                  id="address"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Opcjonalnie"
                />
              </div>
            )}

            {error && <div className="error-text">{error}</div>}
            
            <div className="modal-actions">
              <button 
                type="button" 
                onClick={onClose}
                disabled={saving}
                className="btn-cancel"
              >
                Anuluj
              </button>
              <button 
                type="submit"
                disabled={saving}
                className="btn-submit"
              >
                {saving ? "Zapisywanie..." : "Zapisz zmiany"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

function getRoleName(role) {
  const roleNames = {
    client: "Klient",
    courier: "Kurier",
    manager: "Menadżer",
    admin: "Administrator"
  };
  return roleNames[role] || role;
}
