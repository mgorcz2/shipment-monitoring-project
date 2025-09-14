import React from "react";
import "../styles/ShipmentCard.css";

export default function ShipmentCard({ shipment, onDetails }) {
  return (
    <div className="shipment-card">
      <div className="shipment-header">
        <span className="shipment-id">#{shipment.id}</span>
        <span className={`shipment-status status-${shipment.status?.toLowerCase()}`}>
          {shipment.status}
        </span>
      </div>
      <div className="shipment-info">
        <div><strong>Nadawca:</strong> {shipment.sender_email}</div>
        <div><strong>Odbiorca:</strong> {shipment.recipient_email}</div>
        <div><strong>Adres nadania:</strong> {shipment.origin}</div>
        <div><strong>Adres odbioru:</strong> {shipment.destination}</div>
      </div>
      <div className="shipment-actions">
        <button onClick={() => onDetails(shipment)}>Szczegóły</button>
      </div>
    </div>
  );
}