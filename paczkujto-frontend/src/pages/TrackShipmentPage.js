import React, { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import ShipmentDetailsModal from '../components/ShipmentDetailsModal';

const TrackShipmentPage = () => {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const email = searchParams.get('email');
  const navigate = useNavigate();
  const location = useLocation();

  const initialShipmentId = useMemo(() => (id ? String(id) : ''), [id]);
  const initialEmail = useMemo(() => (email ? String(email) : ''), [email]);

  const [shipmentIdInput, setShipmentIdInput] = useState(initialShipmentId);
  const [emailInput, setEmailInput] = useState(initialEmail);
  const [shipment, setShipment] = useState(location.state?.prefetchedShipment ?? null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const hasTrackingParams = Boolean(id) && Boolean(email);

  useEffect(() => {
    setShipmentIdInput(initialShipmentId);
  }, [initialShipmentId]);

  useEffect(() => {
    setEmailInput(initialEmail);
  }, [initialEmail]);

  useEffect(() => {
    const fetchShipment = async () => {
      try {
        if (!hasTrackingParams) {
          setShipment(null);
          setError(null);
          setLoading(false);
          return;
        }

        if (location.state?.prefetchedShipment) {
          setShipment(location.state.prefetchedShipment);
          setError(null);
          setLoading(false);
          return;
        }

        setLoading(true);
        setError(null);
        const response = await axios.get(`http://localhost:8000/shipments/check_status`, {
          params: {
            shipment_id: id,
            recipient_email: email
          }
        });
        setShipment(response.data);
        setLoading(false);
      } catch (err) {
        setError('Nie znaleziono przesyłki lub nieprawidłowy adres email.');
        setLoading(false);
      }
    };

    fetchShipment();
  }, [hasTrackingParams, id, email, location.state]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmedId = shipmentIdInput.trim();
    const trimmedEmail = emailInput.trim();

    if (!trimmedId) {
      setError('Wpisz identyfikator przesyłki.');
      return;
    }
    if (!trimmedEmail) {
      setError('Wpisz adres email odbiorcy.');
      return;
    }

    setError(null);
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/shipments/check_status`, {
        params: {
          shipment_id: trimmedId,
          recipient_email: trimmedEmail,
        },
      });

      navigate(
        `/track/${encodeURIComponent(trimmedId)}?email=${encodeURIComponent(trimmedEmail)}`,
        { state: { prefetchedShipment: response.data } }
      );
    } catch (err) {
      setError('Nie znaleziono przesyłki lub nieprawidłowy adres email.');
      setLoading(false);
    }
  };

  if (!hasTrackingParams) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f7f7f7' }}>
        <div style={{ width: '100%', maxWidth: 520, background: '#fff', padding: 24, borderRadius: 8 }}>
          <h2 style={{ marginTop: 0, marginBottom: 16 }}>Śledź przesyłkę</h2>
          <p style={{ marginTop: 0, marginBottom: 20, color: '#444' }}>
            Wpisz identyfikator przesyłki i adres email odbiorcy (taki jak w powiadomieniu mailowym).
          </p>

          <form onSubmit={handleSubmit}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <input
                value={shipmentIdInput}
                onChange={(e) => setShipmentIdInput(e.target.value)}
                placeholder="Identyfikator przesyłki"
                aria-label="Identyfikator przesyłki"
                style={{ padding: 12, borderRadius: 6, border: '1px solid #ddd' }}
              />
              <input
                value={emailInput}
                onChange={(e) => setEmailInput(e.target.value)}
                placeholder="Adres email odbiorcy"
                aria-label="Adres email odbiorcy"
                style={{ padding: 12, borderRadius: 6, border: '1px solid #ddd' }}
              />

              {error && <p style={{ margin: 0, color: '#b00020' }}>{error}</p>}

              <button
                type="submit"
                className="btn btn-primary"
                style={{ fontSize: 18, padding: '14px 20px', width: '100%' }}
                disabled={loading}
              >
                {loading ? 'Sprawdzanie…' : 'Śledź przesyłkę'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f7f7f7' }}>
        <div>
          <p>Ładowanie...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f7f7f7' }}>
        <div>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f7f7f7' }}>
      {shipment && (
        <ShipmentDetailsModal
          shipment={shipment}
          onClose={() => window.location.href = '/'}
        />
      )}
    </div>
  );
};

export default TrackShipmentPage;
