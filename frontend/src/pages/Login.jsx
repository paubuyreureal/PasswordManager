import Form from "../components/Form"
import { Link } from "react-router-dom"
import "../styles/Login.css"

function Login() {
    return (
        <div className="auth-container">
            <div className="auth-content">
                <div className="auth-header">
                    <h1 className="auth-title">Password Manager</h1>
                    <p className="auth-subtitle">Sign in to your account</p>
                </div>
                
                <Form route="/api/login/" method="login" />
                
                <div className="auth-footer">
                    <div className="auth-footer-links">
                        <Link className="auth-link" to="/forgot-password">Forgot password?</Link>
                    </div>
                    <p>Don't have an account?</p>
                    <Link className="auth-link" to="/register">Create an account</Link>
                </div>
            </div>
        </div>
    )
}

export default Login