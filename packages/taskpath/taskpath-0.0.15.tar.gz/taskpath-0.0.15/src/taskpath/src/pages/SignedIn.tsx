const SignedIn = () => {
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = 'taskpath:///';
    document.body.appendChild(iframe);
    return <p className="center">You have successfully signed in.</p>;
};

export default SignedIn;
