import { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { formToJson } from '../utils';

const SignIn = () => {
    const navigate = useNavigate();

    const handleSignIn = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const removeLoadingModal = FRM.loading();
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth`, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: formToJson(e.currentTarget),
        });
        removeLoadingModal();
        if (response.ok) {
            navigate('/check-email/sign-in');
        } else {
            console.log(response.text());
            alert("There was an error signing in.");
        }
    };

    return (
        <>
            <h2>Sign In</h2>
            <form className="little" onSubmit={handleSignIn}>
                <label htmlFor="email">Email address:</label>
                <input id="email" type="email" name="email" placeholder="Email address" required/>
                <button className="center" type="submit">Sign In</button>
            </form>
        </>
    );
};

export default SignIn;
