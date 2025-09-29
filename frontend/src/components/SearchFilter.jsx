import React, { useState, useEffect, useRef } from "react";
import "../styles/SearchFilter.css";

function SearchFilter({ onSearch, onFilter, onClear }) {
    const [searchTerm, setSearchTerm] = useState("");
    const [domainFilter, setDomainFilter] = useState("");
    const [showFilters, setShowFilters] = useState(false);
    const searchTimeoutRef = useRef(null);

    const handleSearchChange = (e) => {
        const value = e.target.value;
        setSearchTerm(value);
        
        // Clear existing timeout
        if (searchTimeoutRef.current) {
            clearTimeout(searchTimeoutRef.current);
        }
        
        // Set new timeout for debounced search
        searchTimeoutRef.current = setTimeout(() => {
            onSearch(value);
        }, 300); // 300ms delay
    };

    const handleDomainChange = (e) => {
        const value = e.target.value;
        setDomainFilter(value);
        onFilter({ domain: value });
    };

    const handleClear = () => {
        // Clear timeout if it exists
        if (searchTimeoutRef.current) {
            clearTimeout(searchTimeoutRef.current);
        }
        
        setSearchTerm("");
        setDomainFilter("");
        onClear();
    };

    // Cleanup timeout on unmount
    useEffect(() => {
        return () => {
            if (searchTimeoutRef.current) {
                clearTimeout(searchTimeoutRef.current);
            }
        };
    }, []);

    const hasActiveFilters = searchTerm || domainFilter;

    return (
        <div className="search-filter-container">
            <div className="search-section">
                <div className="search-input-container">
                    <input
                        type="text"
                        placeholder="Search accounts by username, URL, or notes..."
                        value={searchTerm}
                        onChange={handleSearchChange}
                        className="search-input"
                    />
                    <span className="search-icon">🔍</span>
                </div>
                
                <div className="filter-actions">
                    <button
                        className={`filter-toggle ${showFilters ? 'active' : ''}`}
                        onClick={() => setShowFilters(!showFilters)}
                    >
                        Filters {hasActiveFilters && <span className="filter-badge">●</span>}
                    </button>
                    
                    {hasActiveFilters && (
                        <button
                            className="clear-filters"
                            onClick={handleClear}
                        >
                            Clear
                        </button>
                    )}
                </div>
            </div>

            {showFilters && (
                <div className="filters-section">
                    <div className="filter-group">
                        <label htmlFor="domain-filter">Domain:</label>
                        <input
                            type="text"
                            id="domain-filter"
                            placeholder="e.g., github.com, gmail.com"
                            value={domainFilter}
                            onChange={handleDomainChange}
                            className="filter-input"
                        />
                    </div>
                </div>
            )}
        </div>
    );
}

export default SearchFilter;
