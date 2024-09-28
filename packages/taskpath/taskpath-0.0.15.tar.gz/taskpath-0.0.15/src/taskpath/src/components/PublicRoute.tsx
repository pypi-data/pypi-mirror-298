import { ReactElement } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

interface PublicRouteProps {
    element: ReactElement;
}

const PublicRoute: React.FC<PublicRouteProps> = ({ element }) => {
    const { currentUser, signOut } = useAuth();

    const authenticatedMessage = (
        <div className="center">
            <p>You are already signed in.</p>
            <p>
                Go to your <Link to="/projects">projects</Link> page or
                {' '}<button className="link" onClick={signOut}>sign out</button>.
            </p>
        </div>
    );

    return !currentUser ? element : authenticatedMessage;
};

export default PublicRoute;
