import React, { useState, useEffect } from "react";
import { getClientById } from "../services/clientService";
import { getStaffById } from "../services/staffService";
import "../styles/AdminPanel.css";

const UserDetailsModal = ({ user, onClose }) => {
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user) {
      fetchUserDetails();
    }
  }, [user]);

  const fetchUserDetails = async () => {
    if (!user) return;

    setLoading(true);
    setError(null);

    try {
      let response;
      
      if (user.role === "client") {
        response = await getClientById(user.id);
      } else if (["courier", "manager"].includes(user.role)) {
        response = await getStaffById (user.id);
      } else {
        setDetails(null);
        setLoading(false);
        return;
      }
      
      setDetails(response.data);
    } catch (err) {
      console.error("Błąd podczas pobierania szczegółów:", err);
      setError("Nie udało się pobrać szczegółów użytkownika");
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content user-details-modal">
        <button className="modal-close-btn" onClick={onClose}>
          ×
        </button>
        
        <h2>Szczegóły użytkownika</h2>
        
        <div className="user-basic-info">
          <div className="info-row">
            <div className="info-label">Email:</div>
            <div className="info-value">{user.email}</div>
          </div>
          
          <div className="info-row">
            <div className="info-label">Rola:</div>
            <div className="info-value">
              <span className={`role-badge role-${user.role}`}>{user.role}</span>
            </div>
          </div>
          
          <div className="info-row">
            <div className="info-label">Data utworzenia:</div>
            <div className="info-value">{formatDate(user.created_at)}</div>
          </div>
          
          <div className="info-row">
            <div className="info-label">UUID:</div>
            <div className="info-value user-id">{user.id}</div>
          </div>
        </div>
        
        <hr className="divider" />
        
        {loading ? (
          <div className="loading-state">Ładowanie szczegółów...</div>
        ) : error ? (
          <div className="error-state">{error}</div>
        ) : details ? (
          <div className="user-extended-info">
            <h3>Dodatkowe informacje</h3>
            
    
            {user.role === "client" && (
              <>
                <div className="info-row">
                  <div className="info-label">Imię:</div>
                  <div className="info-value">{details.first_name || "-"}</div>
                </div>
                
                <div className="info-row">
                  <div className="info-label">Nazwisko:</div>
                  <div className="info-value">{details.last_name || "-"}</div>
                </div>
                
                <div className="info-row">
                  <div className="info-label">Telefon:</div>
                  <div className="info-value">{details.phone_number || "-"}</div>
                </div>
              </>
            )}
            
            {["courier", "manager"].includes(user.role) && (
              <>
                <div className="info-row">
                  <div className="info-label">Imię:</div>
                  <div className="info-value">{details.first_name || "-"}</div>
                </div>
                
                <div className="info-row">
                  <div className="info-label">Nazwisko:</div>
                  <div className="info-value">{details.last_name || "-"}</div>
                </div>
                
                <div className="info-row">
                  <div className="info-label">Telefon:</div>
                  <div className="info-value">{details.phone_number || "-"}</div>
                </div>
                
                {details.region && (
                  <div className="info-row">
                    <div className="info-label">Region:</div>
                    <div className="info-value">{details.region}</div>
                  </div>
                )}
              </>
            )}
          </div>
        ) : (
          <div className="no-details-state">
            Brak dodatkowych szczegółów dla tego użytkownika
          </div>
        )}
      </div>
    </div>
  );
};

export default UserDetailsModal;