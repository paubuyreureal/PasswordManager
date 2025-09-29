import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import api from "../api";
import "../styles/Login.css";

function ResetPassword() {
    const { token } = useParams();
    const navigate = useNavigate();
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [tokenValid, setTokenValid] = useState(null);

    useEffect(() => {
        validateToken();
    }, [token]);

    const validateToken = async () => {
        try {
            const response = await api.post("/api/password-reset/validate-token/", { token });
            if (response.status === 200) {
                setTokenValid(true);
            }
        } catch (error) {
            console.error("Token validation error:", error);
            setTokenValid(false);
            setError("Invalid or expired reset token.");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setMessage("");

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            setLoading(false);
            return;
        }


        try {
            const response = await api.post("/api/password-reset/confirm/", {
                token,
                password
            });
            if (response.status === 200) {
                setMessage("Password reset successfully! Redirecting to login...");
                setTimeout(() => {
                    navigate("/login");
                }, 2000);
            }
        } catch (error) {
            console.error("Password reset error:", error);
            
            let errorMessage = "Failed to reset password. Please try again.";
            
            if (error.response?.data?.error) {
                errorMessage = error.response.data.error;
            } else if (error.response?.status === 400) {
                errorMessage = "Invalid request. Please check your input and try again.";
            } else if (error.response?.status === 401) {
                errorMessage = "Reset link has expired or is invalid. Please request a new password reset.";
            }
            
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    if (tokenValid === null) {
        return (
            <div className="auth-container">
                <div className="auth-content">
                    <div className="loading-message">
                        <p>Validating reset token...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (tokenValid === false) {
        return (
            <div className="auth-container">
                <div className="auth-content">
                    <div className="auth-header">
                        <h1 className="auth-title">Invalid Token</h1>
                        <p className="auth-subtitle">This reset link is invalid or has expired</p>
                    </div>

                    <div className="error-message">
                        {error}
                    </div>

                    <div className="auth-footer">
                        <Link className="auth-link" to="/forgot-password">Request a new reset link</Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="auth-container">
            <div className="auth-content">
                <div className="auth-header">
                    <h1 className="auth-title">Set New Password</h1>
                    <p className="auth-subtitle">Enter your new password below</p>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="password">New Password</label>
                        <input
                            id="password"
                            className="form-input"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your new password"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="confirmPassword">Confirm Password</label>
                        <input
                            id="confirmPassword"
                            className="form-input"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Confirm your new password"
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
                        {loading ? "Resetting..." : "Reset Password"}
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

export default ResetPassword;
