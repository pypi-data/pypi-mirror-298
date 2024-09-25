import { FC, useState } from 'react';
import './Task.css';

interface ITask {
    id: string;
    description: string;
    completed: boolean;
    subtasks: ITask[];
}

interface Props extends ITask {
    reloadProject: () => {};
    level: number;
}

const Task: FC<Props> = ({ reloadProject, id, description, completed, subtasks, level }) => {
    const [loading, setLoading] = useState(false);
    const [localCompleted, setLocalCompleted] = useState(completed);
    const toggleCompleted = async () => {
        setLoading(true);
        const response = await fetch(`${import.meta.env.VITE_API_URL}/tasks/${id}`, {
            method: "PATCH",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"completed": !completed}),
        });
        setLoading(false);
        if (response.ok) {
            setLocalCompleted(!localCompleted);
        } else {
            alert("There was an error toggling the task state.");
        }
    };
    const expand = async () => {
        setLoading(true);
        const response = await fetch(`${import.meta.env.VITE_API_URL}/tasks/${id}/expand`, {
            method: "PATCH",
        });
        setLoading(false);
        if (response.ok) {
            alert("Reloading project");
            reloadProject();
        } else {
            alert("There was an expanding the task");
        }
    };
    if (loading) {
        return <div id="loading"></div>;
    }
    let className = "description";
    if (localCompleted) {
        className += " completed";
    }
    return (
        <>
            <div className="task" style={{ paddingLeft: `${level}em` }}>
                <span className={className}>{description}</span>
                <div className="controls">
                    <button className="link" onClick={toggleCompleted}>
                        {localCompleted ? "Not Done" : "Done"}
                    </button>
                    {subtasks.length == 0 && (
                        <button className="link" onClick={expand}>Expand</button>
                    )}
                </div>
            </div>
            {subtasks && subtasks.map(subtask => (
                <Task key={subtask.id} reloadProject={reloadProject} {...subtask} level={level+1} />
            ))}
        </>
    );
};

export default Task;
