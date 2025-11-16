import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import { registerLocale } from "react-datepicker";
import pl from "date-fns/locale/pl";
import "react-datepicker/dist/react-datepicker.css";
import { updateShipmentStatus } from "../services/shipmentService";
import { updatePackage, getPackageByShipmentId } from "../services/packageService";
import { getUserRole } from "../services/authService";
import "../styles/ShipmentsPage.css";

registerLocale("pl", pl);       

const STATUS_OPTIONS_ADMIN = [
  { value: "ready_for_pickup", label: "Gotowa do odbioru" },
  { value: "picked_up", label: "Odebrana od nadawcy" },
  { value: "out_for_delivery", label: "W drodze" },
  { value: "delivered", label: "Dostarczona" },
  { value: "failed_attempt", label: "Nieudana próba" },
  { value: "returned_to_sender", label: "Zwrócona do nadawcy" },
  { value: "lost", label: "Zagubiona" },
  { value: "damaged", label: "Uszkodzona" }
];

const STATUS_OPTIONS_COURIER = [
  { value: "picked_up", label: "Odebrana od nadawcy" },
  { value: "delivered", label: "Dostarczona" },
  { value: "failed_attempt", label: "Nieudana próba" },
  { value: "returned_to_sender", label: "Zwrócona do nadawcy" }
];

export default function UpdateShipmentStatusModal({ shipment, onClose, onSuccess }) {
  const userRole = getUserRole();
  const isAdminOrManager = userRole === "admin" || userRole === "manager";
  
  const STATUS_OPTIONS = isAdminOrManager ? STATUS_OPTIONS_ADMIN : STATUS_OPTIONS_COURIER;
  
  const [selectedStatus, setSelectedStatus] = useState(
    shipment?.status === "pending" ? "ready_for_pickup" : (shipment?.status || "ready_for_pickup")
  );
  const [packageData, setPackageData] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPackage = async () => {
      try {
        const response = await getPackageByShipmentId(shipment.id);
        setPackageData(response.data);
      } catch (err) {
        console.error("Błąd pobierania paczki:", err);
      }
    };
    
    if (shipment?.id) {
      fetchPackage();
    }
  }, [shipment]);


  const getDateFieldLabel = () => {
    switch(selectedStatus) {
    case "pending":
        return "Data:";
    case "ready_for_pickup":
        return "Planowana data odbioru od nadawcy:";
    case "picked_up":
        return "Faktyczna data odbioru od nadawcy:";
    case "out_for_delivery":
        return "Planowana data dostawy do odbiorcy:";
    case "delivered":
        return "Faktyczna data dostawy do odbiorcy:";
    case "failed_attempt":
        return "Data kolejnej próby dostawy:";
    case "returned_to_sender":
        return "Data zwrotu do nadawcy:";
    case "lost":
    case "damaged":
        return "Data anulowania:";
    default:
        return "Wybierz datę:";
    }
  };

  const handleStatusChange = (e) => {
    const status = e.target.value;
    setSelectedStatus(status);
    
    if (status === "out_for_delivery") {
      setSelectedDate(new Date(Date.now() + 2 * 24 * 60 * 60 * 1000));
    } else {
      setSelectedDate(new Date());
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    try {
      await updateShipmentStatus(shipment.id, selectedStatus);
      
      const updatedPackage = {
        ...packageData,
        pickup_scheduled_date: packageData.pickup_scheduled_date,
        pickup_actual_date: packageData.pickup_actual_date,
        delivery_scheduled_date: packageData.delivery_scheduled_date,
        delivery_actual_date: packageData.delivery_actual_date,
        cancelled_at: packageData.cancelled_at
      };

      switch(selectedStatus) {
        case "pending":
          break;
        case "ready_for_pickup":
          updatedPackage.pickup_scheduled_date = selectedDate.toISOString();
          break;
        case "picked_up":
          updatedPackage.pickup_actual_date = selectedDate.toISOString();
          break;
        case "out_for_delivery":
          updatedPackage.delivery_scheduled_date = selectedDate.toISOString();
          break;
        case "delivered":
          updatedPackage.delivery_actual_date = selectedDate.toISOString();
          break;
        case "failed_attempt":
          updatedPackage.delivery_scheduled_date = selectedDate.toISOString();
          break;
        case "returned_to_sender":
        case "lost":
        case "damaged":
          updatedPackage.cancelled_at = selectedDate.toISOString();
          break;
      }
      
      await updatePackage(packageData.id, updatedPackage);
      
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || "Błąd aktualizacji");
    } finally {
      setLoading(false);
    }
  };

  if (!shipment || !packageData) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close-btn" onClick={onClose}>×</button>
        
        <h2>Zmień status przesyłki #{shipment.id}</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nowy status:</label>
            <select 
              value={selectedStatus} 
              onChange={handleStatusChange}
              required
              className="status-select"
            >
              {STATUS_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>{getDateFieldLabel()}</label>
            <DatePicker
              selected={selectedDate}
              onChange={(date) => setSelectedDate(date)}
              showTimeSelect
              timeFormat="HH:mm"
              timeIntervals={15}
              dateFormat="Pp"
              locale="pl"
              className="date-picker-input"
              required
            />
          </div>

          {error && <div className="error-text">{error}</div>}
          
          <div className="modal-actions">
            <button type="button" onClick={onClose} disabled={loading} className="btn-cancel">
              Anuluj
            </button>
            <button type="submit" disabled={loading} className="btn-submit">
              {loading ? "Zapisywanie..." : "Zapisz"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}