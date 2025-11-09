import React from "react";
import "../styles/AdminPanel.css";

const DeleteConfirmModal = ({ user, onConfirm, onCancel, isDeleting }) => {
  if (!user) return null;

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content delete-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header delete-header">
          <h2>⚠️ Potwierdzenie usunięcia</h2>
        </div>

        <div className="modal-body">
          <p className="warning-text">
            Czy na pewno chcesz usunąć użytkownika?
          </p>
          
          <div className="user-info-box">
            <div className="info-row">
              <strong>Email:</strong> {user.email}
            </div>
            <div className="info-row">
              <strong>Rola:</strong> 
              <span className={`role-badge role-${user.role}`}>
                {user.role}
              </span>
            </div>
            <div className="info-row">
              <strong>Utworzony:</strong> {new Date(user.created_at).toLocaleString()}
            </div>
          </div>

          <p className="danger-text">
            ⚠️ Ta operacja jest <strong>nieodwracalna</strong> i usunie:
          </p>
          <ul className="delete-list">
            <li>Dane użytkownika</li>
            {user.role === "client" && <li>Dane klienta</li>}
            {(user.role === "courier" || user.role === "manager") && <li>Dane pracownika</li>}
            <li>Wszystkie powiązane informacje</li>
          </ul>
        </div>

        <div className="modal-footer">
          <button 
            className="btn btn-secondary" 
            onClick={onCancel}
            disabled={isDeleting}
          >
            Anuluj
          </button>
          <button 
            className="btn btn-danger" 
            onClick={onConfirm}
            disabled={isDeleting}
          >
            {isDeleting ? "Usuwanie..." : "Usuń użytkownika"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;