import React, { useState, useEffect } from "react";
import { getUserRole } from "../services/authService";
import { getMyProfile, deleteMyAccount } from "../services/userService";
import { getClientById, updateClient } from "../services/clientService";
import { getStaffById, updateStaff } from "../services/staffService";
import { useNavigate } from "react-router-dom";
import DeleteAccountModal from "../components/DeleteAccountModal";
import "../styles/ProfilePage.css";

export default function ProfilePage() {
  const navigate = useNavigate();
  const userRole = getUserRole();
  
  const [userData, setUserData] = useState(null);
  const [profileData, setProfileData] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    phone_number: "",
    address: ""
  });

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const userResponse = await getMyProfile();
      const user = userResponse.data;
      setUserData(user);

      if (user.role === "client") {
        const clientResponse = await getClientById(user.id);
        const client = clientResponse.data;
        setProfileData(client);
        setFormData({
          first_name: client.first_name || "",
          last_name: client.last_name || "",
          phone_number: client.phone_number || "",
          address: client.address || ""
        });
      } else if (user.role === "courier" || user.role === "manager") {
        const staffResponse = await getStaffById(user.id);
        const staff = staffResponse.data;
        setProfileData(staff);
        setFormData({
          first_name: staff.first_name || "",
          last_name: staff.last_name || "",
          phone_number: staff.phone_number || "",
          address: ""
        });
      } else if (user.role === "admin") {
        setProfileData({ admin: true });
        setFormData({
          first_name: "",
          last_name: "",
          phone_number: "",
          address: ""
        });
      }
    } catch (err) {
      console.error("Błąd pobierania profilu:", err);
      setError("Nie udało się pobrać danych profilu");
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

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      if (userRole === "client") {
        await updateClient(userData.id, formData);
      } else if (userRole === "courier" || userRole === "manager") {
        const { address, ...staffData } = formData;
        await updateStaff(userData.id, staffData);
      }
      
      setSuccess("Dane zostały zaktualizowane pomyślnie!");
      setIsEditing(false);
      await fetchProfileData();
      
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error("Błąd zapisywania:", err);
      setError(err.response?.data?.detail || "Nie udało się zapisać zmian");
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await deleteMyAccount();
      localStorage.removeItem("token");
      navigate("/login");
    } catch (err) {
      console.error("Błąd usuwania konta:", err);
      setError(err.response?.data?.detail || "Nie udało się usunąć konta");
      setShowDeleteModal(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setError(null);
    setSuccess(null);
    
    if (profileData) {
      setFormData({
        first_name: profileData.first_name || "",
        last_name: profileData.last_name || "",
        phone_number: profileData.phone_number || "",
        address: profileData.address || ""
      });
    }
  };

  if (loading) {
    return (
      <div className="profile-page">
        <div className="loading-container">Ładowanie profilu...</div>
      </div>
    );
  }

  if (!userData) {
    return (
      <div className="profile-page">
        <div className="error-container">Nie udało się załadować profilu</div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <h1>Mój profil</h1>
          <div className="profile-role-badge">{getRoleName(userRole)}</div>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <div className="profile-content">
          <div className="profile-section">
            <h2>Informacje o koncie</h2>
            <div className="info-grid">
              <div className="info-item">
                <label>Email:</label>
                <div className="info-value">{userData.email}</div>
              </div>
              <div className="info-item">
                <label>Rola:</label>
                <div className="info-value">{getRoleName(userRole)}</div>
              </div>
            </div>
          </div>

          {userRole !== "admin" && profileData && (
            <div className="profile-section">
              <div className="section-header">
                <h2>Dane osobowe</h2>
                {!isEditing && (
                  <button 
                    className="btn-edit" 
                    onClick={() => setIsEditing(true)}
                  >
                    ✏️ Edytuj
                  </button>
                )}
              </div>

            <div className="info-grid">
              <div className="info-item">
                <label>Imię:</label>
                {isEditing ? (
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                ) : (
                  <div className="info-value">{profileData.first_name}</div>
                )}
              </div>

              <div className="info-item">
                <label>Nazwisko:</label>
                {isEditing ? (
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    className="form-input"
                    required
                  />
                ) : (
                  <div className="info-value">{profileData.last_name}</div>
                )}
              </div>

              <div className="info-item">
                <label>Telefon:</label>
                {isEditing ? (
                  <input
                    type="tel"
                    name="phone_number"
                    value={formData.phone_number}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="+48123456789"
                    required
                  />
                ) : (
                  <div className="info-value">{profileData.phone_number}</div>
                )}
              </div>

              {userRole === "client" && (
                <div className="info-item">
                  <label>Adres:</label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="address"
                      value={formData.address}
                      onChange={handleInputChange}
                      className="form-input"
                      placeholder="Opcjonalnie"
                    />
                  ) : (
                    <div className="info-value">{profileData.address || "—"}</div>
                  )}
                </div>
              )}
            </div>

            {isEditing && (
              <div className="form-actions">
                <button 
                  className="btn-cancel" 
                  onClick={handleCancel}
                  disabled={saving}
                >
                  Anuluj
                </button>
                <button 
                  className="btn-save" 
                  onClick={handleSave}
                  disabled={saving}
                >
                  {saving ? "Zapisywanie..." : "Zapisz zmiany"}
                </button>
              </div>
            )}
            </div>
          )}

          {userRole === "admin" && (
            <div className="profile-section">
              <h2>Dane osobowe</h2>
              <p className="admin-info">
                Jako administrator nie masz profilu klienta ani pracownika. 
                Zarządzasz systemem i innymi użytkownikami.
              </p>
            </div>
          )}

          {userRole !== "admin" && (
          <div className="profile-section danger-zone">
            <h2>Strefa niebezpieczna</h2>
            <p className="danger-description">
              Usuń swoje konto i wszystkie powiązane dane. Ta akcja jest nieodwracalna.
            </p>
            <button 
              className="btn-delete-account" 
              onClick={() => setShowDeleteModal(true)}
            >
              🗑️ Usuń konto
            </button>
          </div>
          )}
        </div>
      </div>

      {showDeleteModal && (
        <DeleteAccountModal
          email={userData.email}
          role={userRole}
          onConfirm={handleDeleteAccount}
          onCancel={() => setShowDeleteModal(false)}
        />
      )}
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
