import Form from "../components/Form"
import { Link } from "react-router-dom"
import "../styles/Login.css"

function Register() {
    return (
        <div className="auth-container">
            <div className="auth-content">
                <div className="auth-header">
                    <h1 className="auth-title">Password Manager</h1>
                    <p className="auth-subtitle">Create your account</p>
                </div>
                
                <Form route="/api/user/register/" method="register" />
                
                <div className="auth-footer">
                    <p>Already have an account?</p>
                    <Link className="auth-link" to="/login">Sign in</Link>
                </div>
            </div>
        </div>
    )
}

export default Register