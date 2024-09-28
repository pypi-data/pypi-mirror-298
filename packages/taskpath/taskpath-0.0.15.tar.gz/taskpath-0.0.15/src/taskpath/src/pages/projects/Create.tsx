import { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { formToJson } from '../../utils';

const CreateProject = () => {
    const navigate = useNavigate();

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        const form = e.currentTarget;
        e.preventDefault();
        const removeLoadingModal = FRM.loading();
        const response = await fetch(form.action, {
            method: form.method,
            headers: { 'Content-Type': 'application/json' },
            body: formToJson(form),
        });
        removeLoadingModal();
        if (response.ok) {
            const projectId = (await response.json()).id;
            navigate(`/projects/${projectId}`);
        } else {
            console.log(response.text());
            alert("There was an error creating the project.");
        }
    };

    return (
        <>
            <form
                action={`${import.meta.env.VITE_API_URL}/projects`}
                method="POST"
                onSubmit={handleSubmit}
            >
                <label htmlFor="title">Title:</label>
                <input id="title" type="text" name="title" placeholder="Project Title" required />
                <label htmlFor="description">Description:</label>
                <textarea id="description" name="description" placeholder="Project Description"></textarea>
                <button type="submit">Create Project</button>
            </form>
        </>
    );
};

export default CreateProject;
