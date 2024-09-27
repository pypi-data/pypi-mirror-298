import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const ListProjects = () => {
    const [projects, setProjects] = useState<any>();

    const loadProjects = async () => {
        const removeLoadingModal = FRM.loading();
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
            removeLoadingModal();
        }
    };

    const deleteProject = async (project: any) => {
        const removeLoadingModal = FRM.loading();
        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/projects/${project.id}`,
                {
                    method: 'DELETE',
                },
            );
            if (response.ok) {
                loadProjects();
            } else {
                alert("There was an error deleting the project.");
            }
        } catch {
            alert("There was an error deleting the project.");
        } finally {
            removeLoadingModal();
        }
    };

    const deleteProjectModal = (project: any) => {
        FRM.modal(
            `<h2>Delete ${project.title}</h2><p>Are you sure you want to delete this project?</p>`,
            {
                isConfirmationModal: true,
                successFunc: () => deleteProject(project),
            },
        );
    };

    useEffect(() => {
        loadProjects();
    }, []);

    return (
        <>
            <h2>Projects</h2>
            {projects && projects.map((project: any) => (
                <p className="center">
                    <Link to={`/projects/${project.id}`}>{project.title}</Link>
                    {' '}
                    (<button className='link' onClick={() => deleteProjectModal(project)}>
                        Delete
                    </button>)
                </p>
            ))}
            <p className="center margin-top-2em">
                <Link to="/projects/create" className="button">New Project</Link>
            </p>
        </>
    );
};

export default ListProjects;
