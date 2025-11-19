import React from "react";
import "../styles/ShipmentsPage.css";

export default function DeleteAccountModal({ email, role, onConfirm, onCancel }) {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close-btn" onClick={onCancel}>×</button>
        
        <h2>⚠️ Potwierdzenie usunięcia konta</h2>
        
        <div className="shipment-info" style={{ marginTop: '1.5rem' }}>
          <p><strong>Email:</strong> {email}</p>
          <p><strong>Rola:</strong> {getRoleName(role)}</p>
        </div>

        <div style={{ 
          background: '#fff3cd', 
          border: '1px solid #ffc107',
          borderRadius: '6px',
          padding: '1rem',
          margin: '1.5rem 0',
          color: '#856404'
        }}>
          <p style={{ margin: 0, fontWeight: 600 }}>
            ⚠️ Ta operacja jest nieodwracalna!
          </p>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.95rem' }}>
            Usunięte zostaną wszystkie Twoje dane oraz powiązane przesyłki.
          </p>
        </div>

        <div className="modal-actions">
          <button 
            type="button" 
            onClick={onCancel}
            className="btn-cancel"
          >
            Anuluj
          </button>
          <button 
            type="button"
            onClick={onConfirm}
            style={{
              padding: '0.75rem 1.5rem',
              background: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: '600'
            }}
          >
            Usuń konto na zawsze
          </button>
        </div>
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
