
import React, { useState, useEffect } from "react";
import { getAllUsers, deleteUser } from "../services/userService";  
import UserList from "../components/UsersTable";
import UserDetailsModal from "../components/UserDetailsModal";
import DeleteConfirmModal from "../components/DeleteConfirmModal"; 
import RegisterStaffModal from "../components/RegisterStaffModal";
import EditUserModal from "../components/EditUserModal";
import "../styles/AdminPanel.css";


const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userToDelete, setUserToDelete] = useState(null);  
  const [isDeleting, setIsDeleting] = useState(false);    
  const [showRegisterStaff, setShowRegisterStaff] = useState(false);
  const [editModalUser, setEditModalUser] = useState(null);  

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getAllUsers();
      setUsers(response.data);
    } catch (err) {
      console.error("Błąd podczas pobierania użytkowników:", err);
      setError("Nie udało się pobrać listy użytkowników");
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = (user) => {
    setSelectedUser(user);
  };

  const handleEditUser = (user) => {
    setEditModalUser(user);
  };

  const handleDeleteUser = (user) => {
    setUserToDelete(user);  
  };

  const confirmDelete = async () => {
    if (!userToDelete) return;

    setIsDeleting(true);
    try {
      await deleteUser(userToDelete.email);
      
      setUsers(users.filter(u => u.id !== userToDelete.id));
      
      alert(`✓ Użytkownik ${userToDelete.email} został usunięty`);
      
      setUserToDelete(null);
    } catch (err) {
      console.error("Błąd podczas usuwania:", err);
      alert(`✗ Błąd: ${err.response?.data?.detail || "Nie udało się usunąć użytkownika"}`);
    } finally {
      setIsDeleting(false);
    }
  };

  const cancelDelete = () => {
    setUserToDelete(null);
  };

  const closeDetailsModal = () => {
    setSelectedUser(null);
  };

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1>Panel Administratora</h1>
        <p>Zarządzanie użytkownikami systemu</p>
          <button 
    className="btn btn-primary"
    onClick={() => setShowRegisterStaff(true)}
  >
    + Zarejestruj Pracownika
  </button>
      </div>
      
      {loading ? (
        <div className="loading-state">Ładowanie użytkowników...</div>
      ) : error ? (
        <div className="error-state">{error}</div>
      ) : (
        <UserList
          users={users}
          onViewDetails={handleViewDetails}
          onEditUser={handleEditUser}
          onDeleteUser={handleDeleteUser}
        />
      )}

      {selectedUser && (
        <UserDetailsModal user={selectedUser} onClose={closeDetailsModal} />
      )}

      {userToDelete && (
        <DeleteConfirmModal
          user={userToDelete}
          onConfirm={confirmDelete}
          onCancel={cancelDelete}
          isDeleting={isDeleting}
        />
      )}

      {showRegisterStaff && (
        <RegisterStaffModal
          onClose={() => setShowRegisterStaff(false)}
          onSuccess={fetchUsers}
        />
      )}

      {editModalUser && (
        <EditUserModal
          user={editModalUser}
          onClose={() => setEditModalUser(null)}
          onSuccess={fetchUsers}
        />
      )}
    </div>
  );
};

export default AdminPanel;