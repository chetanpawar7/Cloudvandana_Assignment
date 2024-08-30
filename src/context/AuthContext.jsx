import { createContext, useState, useEffect } from 'react';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [authTokens, setAuthTokens] = useState(() => {
        return localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null;
    });

    useEffect(() => {
        if (authTokens) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${authTokens.access}`;
        }
    }, [authTokens]);

    const loginUser = async (username, password) => {
        try {
            const response = await axios.post(`${BASE_URL}/login/`, { username, password });
            setAuthTokens(response.data);
            setUser(username);
            localStorage.setItem('authTokens', JSON.stringify(response.data));
        } catch (error) {
            console.error("Login failed:", error);
        }
    };

    const registerUser = async (username, email, password) => {
        try {
            const response = await axios.post(`${BASE_URL}/register/`, { username, email, password });
            setAuthTokens(response.data);
            setUser(username);
            localStorage.setItem('authTokens', JSON.stringify(response.data));
        } catch (error) {
            console.error("Registration failed:", error);
        }
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    };

    const contextValue = {
        user,
        authTokens,
        loginUser,
        registerUser,
        logoutUser,
    };

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;
