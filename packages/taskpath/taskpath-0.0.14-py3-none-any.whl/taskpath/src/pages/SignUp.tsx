import { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { formToJson } from '../utils';

const SignUp = () => {
    const navigate = useNavigate();

    const handleSignUp = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const removeLoadingModal = FRM.loading();
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth`, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: formToJson(e.currentTarget),
        });
        removeLoadingModal();
        if (response.ok) {
            navigate('/check-email/sign-up');
        } else {
            console.log(response.text());
            alert("There was an error signing up.");
        }
    };

    return (
        <>
            <h2>Sign up</h2>
            <form className="little" onSubmit={handleSignUp}>
                <input type="email" name="email" placeholder="Email address" required/>
                <button className="center" type="submit">Sign Up</button>
            </form>
        </>
    );
};

export default SignUp;
