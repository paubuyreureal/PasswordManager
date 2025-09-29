import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import "../styles/Login.css";

function ForgotPassword() {
    const [username, setUsername] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");

        try {
            const response = await api.post("/api/password-reset/", { username });
            if (response.status === 200) {
                setMessage("Password reset email sent to backend logs! Please check them in Codespaces.");
            }
        } catch (error) {
            console.error("Password reset error:", error);
            setError("Failed to send reset email. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-content">
                <div className="auth-header">
                    <h1 className="auth-title">Reset Password</h1>
                    <p className="auth-subtitle">Enter your username to receive a reset link</p>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            className="form-input"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                        />
                    </div>

                    {message && (
                        <div className="success-message">
                            {message}
                        </div>
                    )}

                    {error && (
                        <div className="error-message">
                            {error}
                        </div>
                    )}

                    <button className="auth-button" type="submit" disabled={loading}>
                        {loading ? "Sending..." : "Send Reset Link"}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>Remember your password?</p>
                    <Link className="auth-link" to="/login">Back to Login</Link>
                </div>
            </div>
        </div>
    );
}

export default ForgotPassword;
