import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import api from "../api";
import "../styles/AccountDetail.css";

function AccountDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [account, setAccount] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [showPassword, setShowPassword] = useState(false);
    const [showEditPassword, setShowEditPassword] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({});

    useEffect(() => {
        getAccount();
    }, [id]);

    const getAccount = () => {
        setIsLoading(true);
        api
            .get(`/api/accounts/${id}/`)
            .then((res) => res.data)
            .then((data) => {
                setAccount(data);
                setEditData({
                    username: data.username,
                    password: data.decrypted_password,
                    url: data.url,
                    notes: data.notes || "",
                    icon: data.icon || ""
                });
            })
            .catch((err) => {
                console.error("Error loading account:", err);
                alert("Failed to load account. Please try again.");
                navigate("/");
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleCancelEdit = () => {
        setIsEditing(false);
        setEditData({
            username: account.username,
            password: account.decrypted_password,
            url: account.url,
            notes: account.notes || "",
            icon: account.icon || ""
        });
    };

    const handleSave = async () => {
        try {
            const response = await api.patch(`/api/accounts/${id}/`, editData);
            if (response.status === 200) {
                alert("Account updated successfully!");
                setAccount(response.data);
                setIsEditing(false);
            } else {
                throw new Error("Failed to update account");
            }
        } catch (error) {
            console.error("Error updating account:", error);
            alert("Failed to update account. Please try again.");
        }
    };

    const handleDelete = () => {
        if (window.confirm("Are you sure you want to delete this account? This action cannot be undone.")) {
            api
                .delete(`/api/accounts/delete/${id}/`)
                .then((res) => {
                    if (res.status === 204) {
                        alert("Account deleted successfully!");
                        navigate("/");
                    } else {
                        alert("Failed to delete account.");
                    }
                })
                .catch((error) => {
                    console.error("Error deleting account:", error);
                    alert("Failed to delete account. Please try again.");
                });
        }
    };

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    const toggleEditPasswordVisibility = () => {
        setShowEditPassword(!showEditPassword);
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    if (isLoading) {
        return (
            <div className="account-detail-container">
                <div className="loading-message">
                    <p>Loading account details...</p>
                </div>
            </div>
        );
    }

    if (!account) {
        return (
            <div className="account-detail-container">
                <div className="error-message">
                    <h2>Account not found</h2>
                    <p>The account you're looking for doesn't exist or you don't have permission to view it.</p>
                    <Link to="/" className="back-button">← Back to Accounts</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="account-detail-container">
            <div className="account-detail-header">
                <Link to="/" className="back-button">← Back to Accounts</Link>
                <div className="header-actions">
                    <button 
                        className="edit-button" 
                        onClick={handleEdit}
                        disabled={isEditing}
                    >
                        {isEditing ? "Editing..." : "✏️ Edit"}
                    </button>
                    <button 
                        className="delete-button" 
                        onClick={handleDelete}
                    >
                        🗑️ Delete
                    </button>
                </div>
            </div>

            <div className="account-detail-content">
                <div className="account-info-section">
                    <div className="account-icon">
                        {account.favicon_url ? (
                            <img 
                                src={account.favicon_url} 
                                alt="Account icon" 
                                className="favicon"
                            />
                        ) : account.icon ? (
                            <img 
                                src={account.icon} 
                                alt="Account icon" 
                                className="favicon"
                            />
                        ) : (
                            <div className="default-icon">🔐</div>
                        )}
                    </div>

                    <div className="account-main-info">
                        {isEditing ? (
                            <div className="edit-form">
                                <div className="form-group">
                                    <label htmlFor="username">Username:</label>
                                    <input
                                        type="text"
                                        id="username"
                                        value={editData.username}
                                        onChange={(e) => setEditData({...editData, username: e.target.value})}
                                        className="form-input"
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="password">Password:</label>
                                    <div className="password-input-group">
                                        <input
                                            type={showEditPassword ? "text" : "password"}
                                            id="password"
                                            value={editData.password}
                                            onChange={(e) => setEditData({...editData, password: e.target.value})}
                                            className="form-input"
                                        />
                                        <button
                                            type="button"
                                            className="password-toggle-btn"
                                            onClick={toggleEditPasswordVisibility}
                                        >
                                            {showEditPassword ? "🙈" : "👁️"}
                                        </button>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="url">URL:</label>
                                    <input
                                        type="url"
                                        id="url"
                                        value={editData.url}
                                        onChange={(e) => setEditData({...editData, url: e.target.value})}
                                        className="form-input"
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="notes">Notes:</label>
                                    <textarea
                                        id="notes"
                                        value={editData.notes}
                                        onChange={(e) => setEditData({...editData, notes: e.target.value})}
                                        className="form-textarea"
                                        rows="3"
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="icon">Icon URL (optional):</label>
                                    <input
                                        type="url"
                                        id="icon"
                                        value={editData.icon}
                                        onChange={(e) => setEditData({...editData, icon: e.target.value})}
                                        className="form-input"
                                        placeholder="https://example.com/icon.png"
                                    />
                                </div>
                                <div className="form-actions">
                                    <button className="save-button" onClick={handleSave}>
                                        💾 Save Changes
                                    </button>
                                    <button className="cancel-button" onClick={handleCancelEdit}>
                                        ❌ Cancel
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <>
                                <div className="account-field">
                                    <span className="field-label">Username:</span>
                                    <span className="field-value username">{account.username}</span>
                                </div>
                                <div className="account-field">
                                    <span className="field-label">URL:</span>
                                    <span className="field-value">
                                        <a href={account.url} target="_blank" rel="noopener noreferrer">
                                            {account.url}
                                        </a>
                                    </span>
                                </div>
                                {account.notes && (
                                    <div className="account-field">
                                        <span className="field-label">Notes:</span>
                                        <span className="field-value">{account.notes}</span>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                </div>

                <div className="password-section">
                    <div className="account-field">
                        <span className="field-label">Password:</span>
                        <div className="password-display">
                            <div className="password-field">
                                {showPassword ? (
                                    <span className="password-text">{account.decrypted_password}</span>
                                ) : (
                                    <span className="password-hidden">••••••••••••</span>
                                )}
                            </div>
                            <button 
                                className="toggle-password-button"
                                onClick={togglePasswordVisibility}
                            >
                                {showPassword ? "🙈 Hide" : "👁️ Show"}
                            </button>
                        </div>
                    </div>
                </div>

                <div className="account-metadata">
                    <div className="metadata-item">
                        <span className="metadata-label">Created:</span>
                        <span className="metadata-value">{formatDate(account.created_at)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AccountDetail;
