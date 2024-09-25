import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Task from '../../components/Task';

const ReadProject = () => {
    const { projectId } = useParams<{ projectId: string }>();
    const [loading, setLoading] = useState(true);
    const [project, setProject] = useState<any>();

    const loadProject = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/projects/${projectId}`);
            if (response.ok) {
                setProject(await response.json());
            } else {
                alert("There was an error loading the project.");
            }
        } catch {
            alert("There was an error loading the project.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadProject();
    }, []);

    if (loading) {
        return <div id="loading"></div>;
    }

    return (
        <>
            <h2>{project.title}</h2>
            <p>{project.description}</p>
            {!project.tasks.length && <p className="center">This project has no tasks yet.</p>}
            {project.tasks.length > 0 && (
                <div>
                    {project.tasks.map((task: any) => <Task key={task.id} reloadProject={loadProject} {...task} level={0} />)}
                </div>
            )}
        </>
    );
};

export default ReadProject;
