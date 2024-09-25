// src/AuthContext.js
import { createContext, useState, useEffect, useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import privateRoutes from './privateRoutes';

const AuthContext = createContext({
    currentUser: false,
    loading: true,
    signOut: () => {},
});

export const AuthProvider = ({ children }: Record<any, any>) => {
    const navigate = useNavigate();
    const [currentUser, setCurrentUser] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const location = useLocation();

    const checkAuth = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/me`);
            if (response.ok) {
                const obj = await response.json();
                setCurrentUser(obj);
            } else {
                setCurrentUser(null);
            }
        } catch (error) {
            console.error('Error checking authentication', error);
            setCurrentUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        checkAuth();
    }, []);

    useEffect(() => {
        if (privateRoutes.some(privateRoute => location.pathname === privateRoute.path) && !currentUser) {
            checkAuth();
        }
    }, [location]);

    const signOut = async () => {
        setLoading(true);
        await fetch(`${import.meta.env.VITE_API_URL}/sign_out`, {
            method: 'POST',
        });
        setLoading(false);
        setCurrentUser(false);
        navigate('/');
    };

    return (
        <AuthContext.Provider value={{ currentUser, loading, signOut }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
