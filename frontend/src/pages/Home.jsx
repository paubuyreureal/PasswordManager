import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import Account from "../components/Account";
import CreateAccountModal from "../components/CreateAccountModal";
import SearchFilter from "../components/SearchFilter";
import "../styles/Home.css";

function Home() {
    const [accounts, setAccounts] = useState([]);
    const [filteredAccounts, setFilteredAccounts] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [domainFilter, setDomainFilter] = useState("");

    useEffect(() => {
        getAccounts();
    }, []);


    const getAccounts = (searchParams = {}) => {
        setIsLoading(true);
        
        // Build query parameters
        const params = new URLSearchParams();
        if (searchParams.search) params.append('search', searchParams.search);
        if (searchParams.domain) params.append('domain', searchParams.domain);
        if (searchParams.ordering) params.append('ordering', searchParams.ordering);
        
        const queryString = params.toString();
        const url = queryString ? `/api/accounts/?${queryString}` : '/api/accounts/';
        
        api
            .get(url)
            .then((res) => res.data)
            .then((data) => {
                setAccounts(data);
                setFilteredAccounts(data); // Backend already filtered, so use as-is
            })
            .catch((err) => {
                console.error("Error loading accounts:", err);
                alert("Failed to load accounts. Please try again.");
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    const handleSearch = (term) => {
        setSearchTerm(term);
        getAccounts({
            search: term,
            domain: domainFilter
        });
    };

    const handleFilter = (filters) => {
        if (filters.domain !== undefined) {
            setDomainFilter(filters.domain);
            getAccounts({
                search: searchTerm,
                domain: filters.domain
            });
        }
    };

    const handleClearFilters = () => {
        setSearchTerm("");
        setDomainFilter("");
        getAccounts();
    };

    const deleteAccount = (id) => {
        if (window.confirm("Are you sure you want to delete this account? This action cannot be undone.")) {
            api
                .delete(`/api/accounts/delete/${id}/`)
                .then((res) => {
                    if (res.status === 204) {
                        alert("Account deleted successfully!");
                        getAccounts({
                            search: searchTerm,
                            domain: domainFilter
                        });
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


    const createAccount = async (accountData) => {
        try {
            const response = await api.post("/api/accounts/", accountData);
            if (response.status === 201) {
                const newAccount = response.data;
                alert("Account created successfully!");
                
                try {
                    await api.post(`/api/accounts/${newAccount.id}/fetch-favicon/`);
                } catch (faviconError) {
                    // Favicon fetch failed (this is normal for some URLs)
                }
                
                getAccounts({
                    search: searchTerm,
                    domain: domainFilter
                });
            } else {
                throw new Error("Failed to create account");
            }
        } catch (error) {
            console.error("Error creating account:", error);
            alert("Failed to create account. Please try again.");
            throw error;
        }
    };

    const openModal = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
    };

    return (
        <div className="home-container">
            <div className="topbar">
                <h1 className="page-title">Password Manager</h1>
                <Link className="logout-button" to="/logout">Log out</Link>
            </div>

            <div className="main-content">
                <div className="accounts-header">
                    <div className="accounts-title-section">
                        <h2>My Accounts</h2>
                        <button 
                            className="create-account-button"
                            onClick={openModal}
                        >
                            + Create Account
                        </button>
                    </div>
                    
                    <SearchFilter
                        onSearch={handleSearch}
                        onFilter={handleFilter}
                        onClear={handleClearFilters}
                    />
                </div>

                <div className="accounts-section">
                    {isLoading ? (
                        <div className="loading-message">
                            <p>Loading accounts...</p>
                        </div>
                    ) : filteredAccounts.length === 0 ? (
                        <div className="empty-state">
                            {accounts.length === 0 ? (
                                <>
                                    <div className="empty-icon">🔐</div>
                                    <h3>No accounts yet</h3>
                                    <p>Create your first account to get started with your password manager.</p>
                                    <button 
                                        className="create-first-account-button"
                                        onClick={openModal}
                                    >
                                        Create Your First Account
                                    </button>
                                </>
                            ) : (
                                <>
                                    <div className="empty-icon">🔍</div>
                                    <h3>No accounts found</h3>
                                    <p>Try adjusting your search or filter criteria.</p>
                                </>
                            )}
                        </div>
                    ) : (
                        <div className="accounts-list">
                            {filteredAccounts.map((account) => (
                                <Account 
                                    account={account} 
                                    onDelete={deleteAccount}
                                    key={account.id} 
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>

            <CreateAccountModal
                isOpen={isModalOpen}
                onClose={closeModal}
                onSubmit={createAccount}
            />
        </div>
    );
}

export default Home;
