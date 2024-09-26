import { HashRouter as Router, Routes, Route } from 'react-router-dom';

import PublicRoute from './components/PublicRoute';

import Layout from './Layout';

import LandingPage from './pages/LandingPage';
import HowItWorks from './pages/HowItWorks';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';
import CheckEmail from './pages/CheckEmail';
import SignedIn from './pages/SignedIn';
import ContactUs from './pages/ContactUs';
import PrivacyPolicy from './pages/PrivacyPolicy';
import CreateProject from './pages/projects/Create';
import ReadProject from './pages/projects/Read';

import privateRoutes from './privateRoutes';

import { AuthProvider } from './AuthContext';
import './global.css';

const App = () => {
    return (
        <Router>
            <AuthProvider>
                <Layout>
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/how-it-works" element={<HowItWorks />} />
                        <Route path="/sign-in" element={<PublicRoute element={<SignIn />} />} />
                        <Route path="/sign-up" element={<PublicRoute element={<SignUp />} />} />
                        <Route path="/check-email/:type" element={<PublicRoute element={<CheckEmail />} />} />
                        <Route path="/signed-in" element={<SignedIn />} />
                        <Route path="/contact-us" element={<ContactUs />} />
                        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
                        <Route path="/projects/create" element={<CreateProject />} />
                        <Route path="/projects/:projectId" element={<ReadProject />} />
                        {privateRoutes.map(({path, element}) => (
                            <Route key={path} path={path} element={element} />
                        ))}
                    </Routes>
                </Layout>
            </AuthProvider>
        </Router>
  );
};

export default App;
