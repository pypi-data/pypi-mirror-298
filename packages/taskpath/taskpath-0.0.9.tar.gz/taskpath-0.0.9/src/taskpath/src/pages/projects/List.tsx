import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const ListProjects = () => {
    const [loading, setLoading] = useState(true);
    const [projects, setProjects] = useState<any>();

    const loadProjects = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/projects`);
            if (response.ok) {
                setProjects(await response.json());
            } else {
                alert("There was an error loading the projects.");
            }
        } catch {
            alert("There was an error loading the projects.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadProjects();
    }, []);

    if (loading) {
        return <div id="loading"></div>;
    }

    return (
        <>
            <h2>Projects</h2>
            {projects && projects.map((project: any) => (
                <p className="center">
                    <Link to={`/projects/${project.id}`}>{project.title}</Link>
                </p>
            ))}
            <p className="center margin-top-2em">
                <Link to="/projects/create" className="button">New Project</Link>
            </p>
        </>
    );
};

export default ListProjects;
