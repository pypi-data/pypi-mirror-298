import json
from json import JSONDecodeError
from datetime import date
from typing import List, Dict, Union, Optional
import os
class TaskManager():
    """
    A class to manage tasks, providing functionality for adding, removing, and marking tasks
    as done, as well as saving/loading tasks to/from a JSON file and generating reports.
    """
    def __init__(self) -> None: 
        """
        Initializes a new instance of the TaskManager class.

        Attributes:
        to_do : list
            A list of tasks that are yet to be completed.
        done : list
            A list of tasks that have been completed.
        daily_added_tasks : list
            A list of tasks that were added to the to-do list for the current day, used for reporting.
        daily_completed_tasks : list
            A list of tasks that were completed during the current day, used for reporting.
        data : dict
            A dictionary to store the current state of tasks, including to-do and done lists.
        """
        self.daily_added_tasks: List[str] = []
        self.daily_completed_tasks: List[str] = []
        self.to_do: List[str] = []
        self.done: List[str] = []
        self.data: Dict[str, List[str]] = {
            'to_do' : self.to_do,
            'done' : self.done,
            'daily added tasks':self.daily_added_tasks,
            'daily completed tasks':self.daily_completed_tasks
        }
        
    def save_current_state(self) -> str:        
        """
        Saves the current state of the task manager to a JSON file.

        Returns:
            str: A message indicating whether the data was written successfully.
        """
        current_working_dir = os.getcwd()
        data_file_path = os.path.join(current_working_dir, 'data.json')
        with open(data_file_path, 'w') as data_safe:
            json.dump(self.data, data_safe, indent=2)
        return f"Data written succesfully at {data_file_path}."
    
    def load_recent_state(self) -> str:
        """
        Loads the most recent task manager state from a JSON file, updating the to-do,
        done, and reporting lists.

        Returns:
            str: A message confirming the data was loaded successfully, or an error message if no data is found.
        """
        try:
            current_working_dir = os.getcwd()
            file_path = os.path.join(current_working_dir, 'data.json')
            with open(file_path, 'r') as data_safe:
                data = json.load(data_safe)
            self.to_do = data.get('to_do', [])
            self.done = data.get('done', [])
            self.daily_added_tasks = data.get('daily added tasks', [])
            self.daily_completed_tasks = data.get('daily completed tasks', [])

            return "Data loaded succesfully, ready to go!"
        except FileNotFoundError:
            self.reset()
            return 'No saved data found starting fresh.'  
        except JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            self.reset()
            return "Error loading data. Starting fresh."       

    def add_task(self,*tasks: str) -> str:  
        """
        Adds one or more tasks to the to-do list if they are not already present.

        Args:
            *tasks: The tasks to be added to the to-do list.

        Returns:
            str: A message indicating which tasks were added or already exist in the list.
        """
        added_tasks: List[str] = []
        not_added: List[str] = []
        for task in tasks:
            if task.lower() not in self.to_do:
                self.to_do.append(task.lower())
                self.daily_added_tasks.append(task.lower())
                added_tasks.append(task)
            else:
                not_added.append(task)
        response = []
        if added_tasks:
            response.append(f"{', '.join(added_tasks)} added successfully.")
        if not_added:
            response.append(f"{', '.join(not_added)} already in the to-do list:\n {self.to_do}")
        return " ".join(response)
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
            if task.lower() in self.to_do:
                self.to_do.remove(task.lower())
                self.daily_added_tasks.remove(task.lower())
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
        Marks one or more tasks as done by moving them from the to-do list to the done list.

        Args:
            *tasks: The tasks to be marked as done.

        Returns:
            str: A message indicating which tasks were successfully marked as done or already completed.
        """
        done_tasks = []
        already_done_tasks = []
        absent_task = []
        for task in tasks:
            if task.lower() not in self.done and task.lower() in self.to_do:
                self.done.append(task.lower())
                self.daily_completed_tasks.append(task.lower())
                self.to_do.remove(task.lower())
                done_tasks.append(task)
            elif task.lower() in self.done:
                already_done_tasks.append(task)
            else            :
                absent_task.append(task)
        response = []
        if done_tasks:
            response.append(f"{', '.join(done_tasks)} marked as done.")
        if already_done_tasks:
            response.append(f"{', '.join(already_done_tasks)} already done.")
        if absent_task:
            response.append(f"{', '.join(absent_task)} not in to-do list.")
        return " ".join(response)

    def _format_task_list(self, tasks: List[str], list_type: str) -> str :
        """
        Formats a list of tasks for display, numbering them and indicating the type (to-do or done).

        Args:
            tasks (List[str]): The tasks to be formatted.
            list_type (str): The type of tasks (e.g., 'to-do' or 'done') for display purposes.

        Returns:
            str: A formatted string representation of the tasks.
        """
        if not tasks:
            return f"No {list_type} tasks."
    
        formatted_list = f"{list_type.capitalize()} Tasks:\n"
        for idx, task in enumerate(tasks, 1):
            formatted_list += f"{idx}. {task.capitalize()}\n"
        return formatted_list.strip()

    def report(self, file_name : Optional[str]=f"{date.today()}_tasks.txt") :
        """
        Generates and saves a report of the day's to-do and completed tasks to a text file.

        Args:
            file_name (str, optional): The name of the file where the report will be saved.
            Defaults to a file named with the current date.

        Returns:
            str: A message confirming the report was saved or if both task lists are empty.
        """
        if not self.daily_added_tasks and not self.daily_completed_tasks:
            return "Both lists are empty, are you willing to save nothing? Do somrthing, you Panda."
        else:
            todo_final = self._format_task_list(self.daily_added_tasks, 'To-Do')
            done_final = self._format_task_list(self.daily_completed_tasks, 'Done')
            report = f'''{date.today()} Tasks were:

{todo_final}

{done_final}
            '''
            with open(file_name, 'w') as report_file:
                report_file.write(report)
            return f"Report wrote succesfuly. And saved at the current directory with the following name:{file_name}"

    def current_state(self,option: str = 'both') -> str:
        """ 
        Displays the current state of the task manager, showing either the to-do, done, or both lists.

        Args:
            option (str, optional): The task list(s) to display ('to-do', 'done', or 'both'). Defaults to 'both'.

        Returns:
            str: A formatted string representing the requested task list(s).
        """
        if option == 'both':
            return f"{self._format_task_list(self.to_do, 'to-do')}\n\n{self._format_task_list(self.done, 'done')}"
        elif option == 'to-do':
            return self._format_task_list(self.to_do, 'to-do')
        elif option == 'done':
            return self._format_task_list(self.done, ('done'))
        else:
            return "Invalid option."

    def clear_todo_list(self) -> str:
        """
        Clears the to-do list.

        Returns:
            str: A message indicating whether the to-do list was cleared successfully.
        """
        if not self.to_do :
            return "It's already empty."
        else:
            self.to_do.clear()
            self.daily_added_tasks.clear()
            return "To-Do list cleared."

    def clear_done_list(self) -> str:
        """
        Clears the done list.

        Returns:
            str: A message indicating whether the done list was cleared successfully.
        """
        if not self.done :
            return "It's already empty."
        else:
            self.done.clear()
            self.daily_completed_tasks.clear()
            return "Done list cleared."

    def reset(self) -> str:
        """
        Resets both lists.

        Returns:
            str: A message indicating whether both lists were reset successfully.
        """
        if self.to_do or self.done:
            self.to_do.clear()
            self.done.clear()
            self.daily_completed_tasks.clear()
            self.daily_added_tasks.clear()
            return "Both lists reseted and cleaned."
        else:
            return "The lists are already empty."

