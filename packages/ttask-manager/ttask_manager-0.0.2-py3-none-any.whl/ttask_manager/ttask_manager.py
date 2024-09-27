class TaskManager():
    """
    TaskManager manages tasks that need to be done and tasks that are already completed.

    Attributes:
    ----------
    to_do : list
        A list of tasks that are yet to be completed.
        This list tracks the current tasks that the user needs to work on.

    done : list
        A list of tasks that have been completed.
        This list tracks tasks that the user has already marked as done.
    """
    def __init__(self) -> None:
        self.to_do = []
        self.done = []
    def add_task(self,*tasks: str) -> str:
        """
        Adds one or more tasks to the to-do list.

        Args:
            *tasks: One or more tasks to add to the to-do list.

        Returns:
            A message indicating whether the tasks were added successfully.
        """
        added_tasks = []
        for task in tasks:
            if task.lower() not in [content.lower() for content in self.to_do]:
                self.to_do.append(task)
                added_tasks.append(task)
        if added_tasks:
            return f"{', '.join(added_tasks)} added successfully. "
        else:
            return f"{task} already in the to-do list:\n {self.to_do}"
    def remove_task(self,*tasks: str) -> str:
        """
        Removes one or more tasks from the to-do list.

        Args:
            *tasks: One or more tasks to remove from the to-do list.

        Returns:
            A message indicating whether the tasks were removed successfully.
        """
        removed_tasks = []
        not_found_tasks = []

        for task in tasks:
            if task in self.to_do:
                self.to_do.remove(task)
                removed_tasks.append(task)
            else:
                not_found_tasks.append(task)

        if removed_tasks and not_found_tasks:
            return f"{', '.join(removed_tasks)} removed successfully. However, {', '.join(not_found_tasks)} not found in the to-do list."
        elif removed_tasks:
            return f"{', '.join(removed_tasks)} removed successfully."
        elif not_found_tasks:
            return f"{', '.join(not_found_tasks)} not found in the to-do list."
    def task_done(self, *tasks: str) -> str:
        """
        Marks one or more tasks as done.

        Args:
            *tasks: One or more tasks to mark as done.

        Returns:
            A message indicating whether the tasks were marked as done successfully.
        """
        done_tasks = []
        for task in tasks:
            if task in self.to_do and task not in self.done:
                self.done.append(task)
                self.to_do.remove(task)
                done_tasks.append(task)
            elif task in self.done:
                return "Already done."
            elif task not in self.to_do:
                return f"{task} not in the to-do list."

        if done_tasks:
            return f"{', '.join(done_tasks)} marked as done."
        else:
            return "No tasks were marked as done."
    def _format_task_list(self, tasks, list_type):
        if not tasks:
            return f"No {list_type} tasks."
    
        formatted_list = f"{list_type.capitalize()} Tasks:\n"
        for idx, task in enumerate(tasks, 1):
            formatted_list += f"{idx}. {task}\n"
        return formatted_list.strip()

    def current_state(self,option: str = 'both') -> str:
        """
        Returns the current state of the task manager.

        Args:
            option: The option to specify the type of state to return. Can be 'to-do', 'done', or 'both'.

        Returns:
            A string representing the current state of the task manager.
        """
        if option == 'both':
            to_do_list = self._format_task_list(self.to_do, "to-do")
            done_list = self._format_task_list(self.done, "done")
            return f"{to_do_list}\n\n{done_list}"
        elif option == 'to-do':
            return self._format_task_list(self.to_do, "to-do")
        elif option == 'done':
            return self._format_task_list(self.done, "done")
        else:
            return "Invalid option."
    def clear_todo_list(self) -> str:
        """
        Clears the to-do list.

        Returns:
            A message indicating whether the to-do list was cleared successfully.
        """
        if self.to_do == []:
            return "It's already empty."
        else:
            self.to_do.clear()
            return "To-Do list cleared."
    def clear_done_list(self) -> str:
        """
        Clears the done list.

        Returns:
            A message indicating whether the done list was cleared successfully.
        """
        if self.to_do == []:
            return "It's already empty."
        else:
            self.done.clear()
            return "Done list cleared."
    def reset(self) -> str:
        """
        Resets both lists.

        Returns:
            A message indicating whether both lists were reset successfully.
        """
        if self.to_do or self.done:
            self.to_do.clear()
            self.done.clear()
            return "Both lists reseted and cleaned."
        else:
            return "The lists are already empty"

