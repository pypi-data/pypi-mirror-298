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
    const [localCompleted, setLocalCompleted] = useState(completed);
    const toggleCompleted = async () => {
        const nextState = !localCompleted;
        setLocalCompleted(nextState);
        const response = await fetch(`${import.meta.env.VITE_API_URL}/tasks/${id}`, {
            method: "PATCH",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"completed": nextState}),
        });
        if (!response.ok) {
            setLocalCompleted(!nextState);
            alert("There was an error toggling the task state.");
        }
    };
    const expand = async () => {
        const removeLoadingModal = FRM.loading();
        const response = await fetch(`${import.meta.env.VITE_API_URL}/tasks/${id}/expand`, {
            method: "PATCH",
        });
        removeLoadingModal();
        if (response.ok) {
            reloadProject();
        } else {
            alert("There was an expanding the task");
        }
    };
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
