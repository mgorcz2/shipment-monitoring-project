import React, { useState, useEffect } from "react";
import logo from "../assets/logo.png";
import "../styles/CreatePackagePage.css";
import { createShipment } from "../services/shipmentService";
import { createPackage } from "../services/packageService";
import { geocodeAddress, formatAddress } from "../services/geocodingService";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

export default function CreatePackagePage() {
  const [form, setForm] = useState({
    origin_street: "",
    origin_street_number: "",
    origin_city: "",
    origin_postcode: "",
    destination_street: "",
    destination_street_number: "",
    destination_city: "",
    destination_postcode: "",
    recipient_email: "",
    weight: "",
    length: "",
    width: "",
    height: "",
    fragile: false,
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [coords, setCoords] = useState(null);
  const [destCoords, setDestCoords] = useState(null);
  const navigate = useNavigate();

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  useEffect(() => {
    if (form.origin_street && form.origin_city && form.origin_postcode) {
      const address = formatAddress(
        form.origin_street, 
        form.origin_street_number, 
        form.origin_city, 
        form.origin_postcode
      );
      geocodeAddress(address).then(coordinates => {
        if (coordinates) setCoords(coordinates);
      });
    } else {
      setCoords(null);
    }
  }, [form.origin_street, form.origin_street_number, form.origin_city, form.origin_postcode]);

  useEffect(() => {
    if (form.destination_street && form.destination_city && form.destination_postcode) {
      const address = formatAddress(
        form.destination_street, 
        form.destination_street_number, 
        form.destination_city, 
        form.destination_postcode
      );
      geocodeAddress(address).then(coordinates => {
        if (coordinates) setDestCoords(coordinates);
      });
    } else {
      setDestCoords(null);
    }
  }, [form.destination_street, form.destination_street_number, form.destination_city, form.destination_postcode]);

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      const token = localStorage.getItem("token");
      const shipmentRes = await createShipment(
        {
          origin: {
            street: form.origin_street,
            street_number: form.origin_street_number,
            city: form.origin_city,
            postcode: form.origin_postcode,
          },
          destination: {
            street: form.destination_street,
            street_number: form.destination_street_number,
            city: form.destination_city,
            postcode: form.destination_postcode,
          },
          recipient_email: form.recipient_email,
          origin_coords: coords,
          destination_coords: destCoords
        },
        token
      );
      const shipment_id = shipmentRes.data.id;
      await createPackage(
        {
          weight: form.weight,
          length: form.length,
          width: form.width,
          height: form.height,
          fragile: form.fragile,
        },
        shipment_id,
        token
      );
      setSuccess("Paczka została nadana!");
      setTimeout(() => {
        navigate("/shipments");
      }, 2000);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        if (Array.isArray(err.response.data.detail)) {
          setError(
            err.response.data.detail
              .map(e => `${e.loc?.join(".")}: ${e.msg}`)
              .join(", ")
          );
        } else if (typeof err.response.data.detail === "string") {
          setError(err.response.data.detail);
        } else {
          setError("Wystąpił nieznany błąd.");
        }
      } else if (err.response) {
        setError("Błąd: " + err.response.status);
      } else {
        setError("Brak połączenia z serwerem");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-package-container">
      <img src={logo} alt="Logo" style={{ width: 80, marginBottom: 16 }} />
      <h2 className="create-package-title">Nadaj paczkę</h2>
      <form className="create-package-form" onSubmit={handleSubmit}>
        <h3 className="section-header">Adres nadania</h3>
        <input
          type="text"
          name="origin_street"
          placeholder="Ulica"
          value={form.origin_street}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="text"
          name="origin_street_number"
          placeholder="Numer"
          value={form.origin_street_number}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="text"
          name="origin_city"
          placeholder="Miasto"
          value={form.origin_city}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="text"
          name="origin_postcode"
          placeholder="Kod pocztowy"
          value={form.origin_postcode}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />

        {coords && (
          <div className="map-container">
            <MapContainer 
              center={coords} 
              zoom={15} 
              className="leaflet-container"
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
              />
              <Marker position={coords} />
            </MapContainer>
          </div>
        )}

        <h3 className="section-header">Adres odbioru</h3>
        <input
          type="text"
          name="destination_street"
          placeholder="Ulica"
          value={form.destination_street}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="text"
          name="destination_street_number"
          placeholder="Numer"
          value={form.destination_street_number}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="text"
          name="destination_city"
          placeholder="Miasto"
          value={form.destination_city}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="text"
          name="destination_postcode"
          placeholder="Kod pocztowy"
          value={form.destination_postcode}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />

        {destCoords && (
          <div className="map-container">
            <MapContainer 
              center={destCoords} 
              zoom={15} 
              className="leaflet-container"
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
              />
              <Marker position={destCoords} />
            </MapContainer>
          </div>
        )}

        <input
          type="email"
          name="recipient_email"
          placeholder="Email odbiorcy"
          value={form.recipient_email}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />

        <h3 className="section-header">Dane paczki</h3>
        <input
          type="number"
          name="weight"
          placeholder="Waga (kg)"
          value={form.weight}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="number"
          name="length"
          placeholder="Długość (cm)"
          value={form.length}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="number"
          name="width"
          placeholder="Szerokość (cm)"
          value={form.width}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <input
          type="number"
          name="height"
          placeholder="Wysokość (cm)"
          value={form.height}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <input
            type="checkbox"
            name="fragile"
            checked={form.fragile}
            onChange={handleChange}
            disabled={loading}
          />
          Czy paczka jest krucha?
        </label>
        <button
          type="submit"
          className="create-package-button"
          disabled={loading}
        >
          {loading ? "Nadaję..." : "Nadaj paczkę"}
        </button>
        {error && <div className="create-package-error">{error}</div>}
        {success && <div className="create-package-success">{success}</div>}
      </form>
    </div>
  );
}