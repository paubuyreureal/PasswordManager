import React, { useState } from "react";
import "../styles/CreateAccountModal.css";

function CreateAccountModal({ isOpen, onClose, onSubmit }) {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        url: "",
        notes: "",
        icon: ""
    });
    const [isLoading, setIsLoading] = useState(false);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        
        try {
            await onSubmit(formData);
            // Reset form on success
            setFormData({
                username: "",
                password: "",
                url: "",
                notes: "",
                icon: ""
            });
            onClose();
        } catch (error) {
            console.error("Error creating account:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClose = () => {
        if (!isLoading) {
            setFormData({
                username: "",
                password: "",
                url: "",
                notes: "",
                icon: ""
            });
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h2>Create New Account</h2>
                    <button 
                        className="close-button" 
                        onClick={handleClose}
                        disabled={isLoading}
                    >
                        ×
                    </button>
                </div>
                
                <form onSubmit={handleSubmit} className="account-form">
                    <div className="form-group">
                        <label htmlFor="username">Username/Email *</label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={formData.username}
                            onChange={handleInputChange}
                            required
                            disabled={isLoading}
                            placeholder="Enter username or email"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password *</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            required
                            disabled={isLoading}
                            placeholder="Enter password"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="url">Website URL *</label>
                        <input
                            type="url"
                            id="url"
                            name="url"
                            value={formData.url}
                            onChange={handleInputChange}
                            required
                            disabled={isLoading}
                            placeholder="https://example.com"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="notes">Notes</label>
                        <textarea
                            id="notes"
                            name="notes"
                            value={formData.notes}
                            onChange={handleInputChange}
                            disabled={isLoading}
                            placeholder="Optional notes about this account"
                            rows="3"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="icon">Custom Icon URL</label>
                        <input
                            type="url"
                            id="icon"
                            name="icon"
                            value={formData.icon}
                            onChange={handleInputChange}
                            disabled={isLoading}
                            placeholder="https://example.com/icon.png (optional)"
                        />
                    </div>

                    <div className="form-actions">
                        <button 
                            type="button" 
                            className="cancel-button"
                            onClick={handleClose}
                            disabled={isLoading}
                        >
                            Cancel
                        </button>
                        <button 
                            type="submit" 
                            className="submit-button"
                            disabled={isLoading}
                        >
                            {isLoading ? "Creating..." : "Create Account"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default CreateAccountModal;
