import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Account.css";

function Account({ account, onDelete }) {
    const navigate = useNavigate();
    const formattedDate = new Date(account.created_at).toLocaleDateString("en-US");

    const handleAccountClick = () => {
        navigate(`/account/${account.id}`);
    };

    const handleDeleteClick = (e) => {
        e.stopPropagation(); // Prevent navigation when clicking delete
        onDelete(account.id);
    };

    return (
        <div className="account-container" onClick={handleAccountClick}>
            <div className="account-header">
                <div className="account-icon">
                    {account.favicon_url ? (
                        <img 
                            src={account.favicon_url} 
                            alt={`${account.username} icon`}
                            className="favicon"
                        />
                    ) : (
                        <div className="default-icon">
                            <span>🌐</span>
                        </div>
                    )}
                </div>
                <div className="account-info">
                    <h3 className="account-username">{account.username}</h3>
                    <p className="account-url">{account.url}</p>
                </div>
                <div className="account-actions">
                    <button 
                        className="delete-button" 
                        onClick={handleDeleteClick}
                        title="Delete account"
                    >
                        🗑️
                    </button>
                </div>
            </div>
            <div className="account-footer">
                <span className="account-date">Created: {formattedDate}</span>
            </div>
        </div>
    );
}

export default Account;
