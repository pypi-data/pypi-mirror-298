import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
    return (
        <>
            <div id="hero">
                <div id="text-box">
                    <p>Turn your big ideas into actionable steps with TaskPath.</p>
                    <p>
                        <Link className="button" to="/sign-up">Sign Up</Link>
                        {' '}
                        <Link className="button" to="/projects/create">Try It Out</Link>
                    </p>
                </div>
            </div>
        </>
    );
};

export default LandingPage;
