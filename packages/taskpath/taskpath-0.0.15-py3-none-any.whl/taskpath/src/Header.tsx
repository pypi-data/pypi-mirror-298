import { Link } from 'react-router-dom';
import Navigation from './Navigation';

const Header = () => {
    return (
        <>
            <header>
                <h1><Link to="/">TaskPath</Link></h1>
                <p>Break down tasks, build up progress.</p>
            </header>
            <Navigation />
        </>
    );
};

export default Header;
