import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css"
import LoadingIndicator from "./LoadingIndicator";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            let requestData;
            if (method === "login") {
                requestData = { username, password };
            } else {
                requestData = { username, email, password };
            }
            
            const res = await api.post(route, requestData);
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/")
            } else {
                navigate("/login")
            }
        } catch (error) {
            console.error("Form submission error:", error);
            
            let errorMessage = "An unexpected error occurred. Please try again.";
            
            if (error.response?.data?.error) {
                // Handle specific error messages from backend
                errorMessage = error.response.data.error;
            } else if (error.response?.data?.username) {
                // Handle field-specific errors (like duplicate username)
                errorMessage = error.response.data.username[0];
            } else if (error.response?.data?.non_field_errors) {
                // Handle general validation errors
                errorMessage = error.response.data.non_field_errors[0];
            } else if (error.response?.status === 401) {
                // Handle authentication errors
                errorMessage = "Invalid username or password. Please check your credentials and try again.";
            } else if (error.response?.status === 400) {
                // Handle bad request errors
                errorMessage = "Please check your input and try again.";
            }
            
            alert(errorMessage);
        } finally {
            setLoading(false)
        }
    };

    return (
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
            {method === "register" && (
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                        id="email"
                        className="form-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        required
                    />
                </div>
            )}
            <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    className="form-input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    required
                />
            </div>
            {loading && <LoadingIndicator />}
            <button className="auth-button" type="submit" disabled={loading}>
                {loading ? "Please wait..." : name}
            </button>
        </form>
    );
}

export default Form