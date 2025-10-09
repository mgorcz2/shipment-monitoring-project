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

// Funkcja obliczająca odległość między punktami geograficznymi (w km)
function calculateDistance(lat1, lon1, lat2, lon2) {
  if (!lat1 || !lon1 || !lat2 || !lon2) return null;
  
  const R = 6371; // Promień Ziemi w km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c; // Odległość w km
}

// Funkcja obliczająca koszt przesyłki - zmodyfikowany model degresywny
function calculateShippingCost(weight, length, width, height, distance, isFragile) {
  // Konwersja na liczby
  weight = parseFloat(weight) || 0;
  length = parseFloat(length) || 0;
  width = parseFloat(width) || 0;
  height = parseFloat(height) || 0;
  distance = parseFloat(distance) || 0;
  
  // Podstawowy koszt przesyłki
  let cost = 15;
  
  // Dopłata za wagę - nowy model degresywny:
  // - pierwsze 10kg powyżej 1kg: 2 zł/kg
  // - kolejne 20kg: 1 zł/kg
  // - powyżej 30kg: 0.5 zł/kg
  let weightCost = 0;
  if (weight > 1) {
    if (weight <= 11) {
      // Do 11 kg (czyli do 10 kg nadwagi)
      weightCost = (weight - 1) * 2;
    } else if (weight <= 31) {
      // Do 31 kg (10kg po 2zł i reszta po 1zł)
      weightCost = 10 * 2 + (weight - 11) * 1;
    } else {
      // Powyżej 31 kg (10kg po 2zł, 20kg po 1zł i reszta po 0.5zł)
      weightCost = 10 * 2 + 20 * 1 + (weight - 31) * 0.5;
    }
    cost += weightCost;
  }
  
  // Obliczenie objętości w cm³
  const volume = length * width * height;
  
  // Dopłata za objętość (0.5 zł za każde 1000 cm³ powyżej 5000 cm³)
  let volumeCost = 0;
  if (volume > 5000) {
    volumeCost = ((volume - 5000) / 1000) * 0.5;
    cost += volumeCost;
  }
  
  // Dopłata za odległość - nowy model degresywny:
  // - pierwsze 50km powyżej 10km: 0.5 zł/km
  // - kolejne kilometry: 0.3 zł/km
  let distanceCost = 0;
  if (distance > 10) {
    if (distance <= 60) {
      // Do 60 km (czyli do 50 km nadwyżki)
      distanceCost = (distance - 10) * 0.5;
    } else {
      // Powyżej 60 km
      distanceCost = 50 * 0.5 + (distance - 60) * 0.3;
    }
    cost += distanceCost;
  }
  
  // Opłata za przesyłkę delikatną (fragile): +20% do ceny końcowej
  if (isFragile) {
    cost *= 1.2;
  }
  
  // Zachowujemy również informacje o poszczególnych kosztach
  return {
    total: cost.toFixed(2),
    weightCost: weightCost.toFixed(2),
    volumeCost: volumeCost.toFixed(2),
    distanceCost: distanceCost.toFixed(2),
    basicCost: 15.00,
    fragileMultiplier: isFragile ? 1.2 : 1
  };
}

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
  const [geocodingOriginLoading, setGeocodingOriginLoading] = useState(false);
  const [geocodingDestLoading, setGeocodingDestLoading] = useState(false);
  const [geocodingOriginError, setGeocodingOriginError] = useState("");
  const [geocodingDestError, setGeocodingDestError] = useState("");
  const [distance, setDistance] = useState(null);
  const [shippingCost, setShippingCost] = useState(null);
  const navigate = useNavigate();

  // Funkcja sprawdzająca czy wszystkie wymagane pola do obliczenia kosztu są wypełnione
  const canCalculateCost = () => {
    return (
      distance !== null &&
      form.weight && parseFloat(form.weight) >= 1 &&
      form.length && parseFloat(form.length) >= 1 &&
      form.width && parseFloat(form.width) >= 1 &&
      form.height && parseFloat(form.height) >= 1
    );
  };

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    
    let validatedValue = value;
    
    // Walidacja dla pól numerycznych
    if (type === "number") {
      // Jeśli pole jest puste, zachowaj pustą wartość
      if (value === "") {
        validatedValue = "";
      } else {
        const numValue = parseFloat(value);
        
        // Określ limity dla różnych pól
        let min = 1;
        let max = Infinity;
        
        switch (name) {
          case "weight":
            min = 1;
            max = 1000;
            break;
          case "length":
          case "width":
          case "height":
            min = 1;
            max = 400;
            break;
          default:
            break;
        }
        
        // Aplikuj limity tylko jeśli wartość nie jest pusta
        if (!isNaN(numValue)) {
          validatedValue = Math.min(Math.max(numValue, min), max).toString();
        }
      }
    }
    
    // Aktualizuj formularz z nową wartością
    const updatedForm = {
      ...form,
      [name]: type === "checkbox" ? checked : validatedValue
    };
    
    setForm(updatedForm);

    // Resetuj koordynaty przy zmianie adresów
    if (name.startsWith("origin_")) {
      setCoords(null);
      setGeocodingOriginError("");
      setDistance(null);
      setShippingCost(null);
      return; // Wyjdź wcześniej, bo nie ma sensu kontynuować
    } 
    else if (name.startsWith("destination_")) {
      setDestCoords(null);
      setGeocodingDestError("");
      setDistance(null);
      setShippingCost(null);
      return; // Wyjdź wcześniej, bo nie ma sensu kontynuować
    }
    
    // Resetuj cenę jeśli jakieś pole wymiarów lub wagi zostało opróżnione
    if (["weight", "length", "width", "height"].includes(name) && validatedValue === "") {
      setShippingCost(null);
      return;
    }
    
    // Aktualizuj cenę po zmianie dowolnego pola - włączając w to checkbox fragile
    if (distance !== null) {
      // Sprawdź czy istnieją wszystkie niezbędne dane do kalkulacji
      if (
        updatedForm.weight && parseFloat(updatedForm.weight) >= 1 &&
        updatedForm.length && parseFloat(updatedForm.length) >= 1 &&
        updatedForm.width && parseFloat(updatedForm.width) >= 1 &&
        updatedForm.height && parseFloat(updatedForm.height) >= 1
      ) {
        const costResult = calculateShippingCost(
          updatedForm.weight,
          updatedForm.length,
          updatedForm.width,
          updatedForm.height,
          distance,
          updatedForm.fragile
        );
        setShippingCost(costResult);
        
        console.log("Aktualizacja ceny:", {
          weight: updatedForm.weight,
          dimensions: `${updatedForm.length}x${updatedForm.width}x${updatedForm.height}`,
          distance: distance,
          fragile: updatedForm.fragile,
          cost: costResult.total
        });
      } else {
        // Jeśli brakuje danych do obliczenia ceny, resetuj
        setShippingCost(null);
      }
    }
  };

  // Efekt dla geokodowania adresu nadania
  useEffect(() => {
    const timer = setTimeout(() => {
      if (form.origin_street && form.origin_city && form.origin_postcode) {
        // Walidacja kodu pocztowego (dla Polski: xx-xxx)
        const postcodePattern = /^\d{2}-\d{3}$/;
        if (!postcodePattern.test(form.origin_postcode)) {
          setGeocodingOriginError("Niepoprawny format kodu pocztowego (xx-xxx)");
          setCoords(null);
          return;
        }
        
        setGeocodingOriginLoading(true);
        setGeocodingOriginError("");
        const address = formatAddress(
          form.origin_street, 
          form.origin_street_number, 
          form.origin_city, 
          form.origin_postcode
        );
        geocodeAddress(address).then(coordinates => {
          if (coordinates) {
            setCoords(coordinates);
            setGeocodingOriginError("");
          } else {
            setCoords(null);
            setGeocodingOriginError("Nie znaleziono adresu");
          }
        }).catch(err => {
          setCoords(null);
          setGeocodingOriginError("Błąd wyszukiwania adresu");
          console.error("Geocoding error:", err);
        }).finally(() => {
          setGeocodingOriginLoading(false);
        });
      } else {
        setCoords(null);
        setGeocodingOriginError("");
      }
    }, 500);
    
    return () => clearTimeout(timer);
  }, [form.origin_street, form.origin_street_number, form.origin_city, form.origin_postcode]);

  // Efekt dla geokodowania adresu odbioru
  useEffect(() => {
    const timer = setTimeout(() => {
      if (form.destination_street && form.destination_city && form.destination_postcode) {
        // Walidacja kodu pocztowego (dla Polski: xx-xxx)
        const postcodePattern = /^\d{2}-\d{3}$/;
        if (!postcodePattern.test(form.destination_postcode)) {
          setGeocodingDestError("Niepoprawny format kodu pocztowego (xx-xxx)");
          setDestCoords(null);
          return;
        }
        
        setGeocodingDestLoading(true);
        setGeocodingDestError("");
        const address = formatAddress(
          form.destination_street, 
          form.destination_street_number, 
          form.destination_city, 
          form.destination_postcode
        );
        geocodeAddress(address).then(coordinates => {
          if (coordinates) {
            setDestCoords(coordinates);
            setGeocodingDestError("");
          } else {
            setDestCoords(null);
            setGeocodingDestError("Nie znaleziono adresu");
          }
        }).catch(err => {
          setDestCoords(null);
          setGeocodingDestError("Błąd wyszukiwania adresu");
          console.error("Geocoding error:", err);
        }).finally(() => {
          setGeocodingDestLoading(false);
        });
      } else {
        setDestCoords(null);
        setGeocodingDestError("");
      }
    }, 500);
    
    return () => clearTimeout(timer);
  }, [form.destination_street, form.destination_street_number, form.destination_city, form.destination_postcode]);

  // Efekt dla obliczania odległości i aktualizacji ceny
  useEffect(() => {
    if (coords && destCoords) {
      const calculatedDistance = calculateDistance(
        coords[0], coords[1], 
        destCoords[0], destCoords[1]
      );
      setDistance(calculatedDistance);
      
      // Po zmianie odległości, aktualizuj cenę tylko jeśli wszystkie dane są dostępne
      if (calculatedDistance !== null && canCalculateCost()) {
        const costResult = calculateShippingCost(
          form.weight, 
          form.length, 
          form.width, 
          form.height, 
          calculatedDistance,
          form.fragile
        );
        setShippingCost(costResult);
      } else {
        setShippingCost(null);
      }
    } else {
      setDistance(null);
      setShippingCost(null);
    }
  }, [coords, destCoords]);

  // Efekt do monitorowania zmian w formularzu które wpływają na cenę
  useEffect(() => {
    // Sprawdź czy wszystkie potrzebne dane są dostępne
    if (canCalculateCost()) {
      const costResult = calculateShippingCost(
        form.weight,
        form.length,
        form.width,
        form.height,
        distance,
        form.fragile
      );
      setShippingCost(costResult);
    }
  }, [form.weight, form.length, form.width, form.height, form.fragile]);

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");
    setSuccess("");
    
    // Walidacja adresów
    if (!coords || !destCoords) {
      setError("Nie można nadać paczki bez poprawnych adresów. Sprawdź poprawność adresów nadania i odbioru.");
      return;
    }
    
    // Walidacja wymiarów i wagi paczki
    const weight = parseFloat(form.weight);
    const length = parseFloat(form.length);
    const width = parseFloat(form.width);
    const height = parseFloat(form.height);
    
    if (isNaN(weight) || weight < 1 || weight > 1000) {
      setError("Waga paczki musi wynosić od 1kg do 1000kg");
      return;
    }
    
    if (isNaN(length) || length < 1 || length > 400 || 
        isNaN(width) || width < 1 || width > 400 || 
        isNaN(height) || height < 1 || height > 400) {
      setError("Wymiary paczki muszą mieścić się w przedziale od 1cm do 400cm");
      return;
    }
    
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

  // Pomocnicze funkcje do wyświetlania informacji o opłatach
  const getWeightCostDescription = () => {
    const weight = parseFloat(form.weight);
    
    if (weight <= 1) return "";
    
    if (weight <= 11) {
      // Do 10 kg nadwagi po 2 zł/kg
      return `Dopłata za wagę (${(weight - 1).toFixed(2)} kg powyżej 1 kg @ 2 zł/kg):`;
    } else if (weight <= 31) {
      // 10kg po 2zł + reszta po 1zł
      return `Dopłata za wagę (10 kg @ 2 zł/kg + ${(weight - 11).toFixed(2)} kg @ 1 zł/kg):`;
    } else {
      // 10kg po 2zł + 20kg po 1zł + reszta po 0.5zł
      return `Dopłata za wagę (10 kg @ 2 zł/kg + 20 kg @ 1 zł/kg + ${(weight - 31).toFixed(2)} kg @ 0.5 zł/kg):`;
    }
  };
  
  const getDistanceCostDescription = () => {
    if (!distance || distance <= 10) return "";
    
    if (distance <= 60) {
      // Do 50 km nadwyżki po 0.5 zł/km
      return `Dopłata za odległość (${(distance - 10).toFixed(2)} km powyżej 10 km @ 0.5 zł/km):`;
    } else {
      // 50km po 0.5 zł + reszta po 0.3 zł
      return `Dopłata za odległość (50 km @ 0.5 zł/km + ${(distance - 60).toFixed(2)} km @ 0.3 zł/km):`;
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
          placeholder="Kod pocztowy (xx-xxx)"
          value={form.origin_postcode}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />

        {geocodingOriginLoading && (
          <div className="geocoding-status loading">Wyszukiwanie adresu...</div>
        )}
        {geocodingOriginError && (
          <div className="geocoding-status error">{geocodingOriginError}</div>
        )}
        {coords && !geocodingOriginLoading && !geocodingOriginError && (
          <div className="geocoding-status success">Adres znaleziony ✓</div>
        )}

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
          placeholder="Kod pocztowy (xx-xxx)"
          value={form.destination_postcode}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />

        {geocodingDestLoading && (
          <div className="geocoding-status loading">Wyszukiwanie adresu...</div>
        )}
        {geocodingDestError && (
          <div className="geocoding-status error">{geocodingDestError}</div>
        )}
        {destCoords && !geocodingDestLoading && !geocodingDestError && (
          <div className="geocoding-status success">Adres znaleziony ✓</div>
        )}

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

        {distance !== null && (
          <div className="distance-info">
            <span className="distance-label">Odległość:</span>
            <span className="distance-value">{distance.toFixed(2)} km</span>
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
          min="1"
          max="1000"
          step="1"
          value={form.weight}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <div className="input-hint">Waga musi być w zakresie 1-1000 kg</div>
        
        <input
          type="number"
          name="length"
          placeholder="Długość (cm)"
          min="1"
          max="400"
          step="1"
          value={form.length}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <div className="input-hint">Długość musi być w zakresie 1-400 cm</div>
        
        <input
          type="number"
          name="width"
          placeholder="Szerokość (cm)"
          min="1"
          max="400"
          step="1"
          value={form.width}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <div className="input-hint">Szerokość musi być w zakresie 1-400 cm</div>
        
        <input
          type="number"
          name="height"
          placeholder="Wysokość (cm)"
          min="1"
          max="400"
          step="1"
          value={form.height}
          onChange={handleChange}
          required
          className="create-package-input"
          disabled={loading}
        />
        <div className="input-hint">Wysokość musi być w zakresie 1-400 cm</div>
        
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
        
        {/* Informacja o szacowanym koszcie przesyłki */}
        {shippingCost !== null && (
          <div className="shipping-cost-container">
            <h3>Szacowany koszt przesyłki</h3>
            <div className="shipping-cost-details">
              <div className="cost-row">
                <span className="cost-item">Cena podstawowa:</span>
                <span className="cost-value">15.00 zł</span>
              </div>
              
              {parseFloat(form.weight) > 1 && (
                <div className="cost-row">
                  <span className="cost-item">{getWeightCostDescription()}</span>
                  <span className="cost-value">{shippingCost.weightCost} zł</span>
                </div>
              )}
              
              {parseFloat(form.length) * parseFloat(form.width) * parseFloat(form.height) > 5000 && (
                <div className="cost-row">
                  <span className="cost-item">Dopłata za objętość ({((parseFloat(form.length) * parseFloat(form.width) * parseFloat(form.height) - 5000) / 1000).toFixed(2)} ponad limit):</span>
                  <span className="cost-value">{shippingCost.volumeCost} zł</span>
                </div>
              )}
              
              {distance > 10 && (
                <div className="cost-row">
                  <span className="cost-item">{getDistanceCostDescription()}</span>
                  <span className="cost-value">{shippingCost.distanceCost} zł</span>
                </div>
              )}
              
              {form.fragile && (
                <div className="cost-row">
                  <span className="cost-item">Dopłata za przesyłkę delikatną (20%):</span>
                  <span className="cost-value">+20%</span>
                </div>
              )}
              
              <div className="cost-row total">
                <span className="cost-item">ŁĄCZNY KOSZT:</span>
                <span className="cost-value">{shippingCost.total} zł</span>
              </div>
            </div>
          </div>
        )}
        
        <button
          type="submit"
          className="create-package-button"
          disabled={loading || !coords || !destCoords}
        >
          {loading ? "Nadaję..." : "Nadaj paczkę"}
        </button>
        {error && <div className="create-package-error">{error}</div>}
        {success && <div className="create-package-success">{success}</div>}
      </form>
    </div>
  );
}