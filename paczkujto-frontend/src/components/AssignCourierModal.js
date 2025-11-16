import React, { useState, useEffect } from "react";
import { getUsersByRole } from "../services/userService";
import { assignCourierToShipment } from "../services/shipmentService";
import "../styles/ShipmentsPage.css";

export default function AssignCourierModal({ shipment, onClose, onSuccess }) {
  const [couriers, setCouriers] = useState([]);
  const [selectedCourierId, setSelectedCourierId] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCouriers = async () => {
      try {
        const response = await getUsersByRole("courier");
        setCouriers(response.data);
        
        if (shipment?.courier_id) {
          setSelectedCourierId(shipment.courier_id);
        }
      } catch (err) {
        console.error("Błąd pobierania kurierów:", err);
        setError("Nie udało się pobrać listy kurierów");
      } finally {
        setLoading(false);
      }
    };

    fetchCouriers();
  }, [shipment]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedCourierId) {
      setError("Wybierz kuriera");
      return;
    }

    setSubmitting(true);
    setError("");

    try {
      await assignCourierToShipment(shipment.id, selectedCourierId);
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || "Błąd przypisywania kuriera");
    } finally {
      setSubmitting(false);
    }
  };

  if (!shipment) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close-btn" onClick={onClose}>×</button>
        
        <h2>Przypisz kuriera do przesyłki #{shipment.id}</h2>
        
        {loading ? (
          <div className="loading-text">Ładowanie kurierów...</div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="shipment-info">
              <p><strong>Nadawca:</strong> {shipment.sender_fullname || shipment.sender_email}</p>
              <p><strong>Odbiorca:</strong> {shipment.recipient_fullname || shipment.recipient_email}</p>
              <p><strong>Trasa:</strong> {shipment.origin} → {shipment.destination}</p>
              {shipment.courier_fullname && (
                <p><strong>Obecny kurier:</strong> {shipment.courier_fullname}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="courier-select">Wybierz kuriera:</label>
              <select
                id="courier-select"
                value={selectedCourierId}
                onChange={(e) => setSelectedCourierId(e.target.value)}
                required
                className="status-select"
              >
                <option value="">-- Wybierz kuriera --</option>
                {couriers.map((courier) => (
                  <option key={courier.id} value={courier.id}>
                    {courier.email} (ID: {courier.id.slice(0, 8)}...)
                  </option>
                ))}
              </select>
              <small style={{ color: '#666', marginTop: '0.5rem', display: 'block' }}>
                Wybierz kuriera z listy dostępnych kurierów w systemie
              </small>
            </div>

            {error && <div className="error-text">{error}</div>}
            
            <div className="modal-actions">
              <button 
                type="button" 
                onClick={onClose} 
                disabled={submitting} 
                className="btn-cancel"
              >
                Anuluj
              </button>
              <button 
                type="submit" 
                disabled={submitting || !selectedCourierId} 
                className="btn-submit"
              >
                {submitting ? "Przypisywanie..." : "Przypisz"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
