import { useContext } from 'react';
import { Redirect } from 'react-router-dom';
import AuthContext from './AuthContext';

const ProtectedRoute = ({ children }) => {
    const { user } = useContext(AuthContext);
    return user ? children : <Redirect to="/login" />;
};

export default ProtectedRoute;