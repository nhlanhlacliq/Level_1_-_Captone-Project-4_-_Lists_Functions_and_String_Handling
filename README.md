# Task Manager 2.0

_This program is a more developed version of the previous "Task Manager" program now using functions, lists & string handling_

This program adds the following functionality to the existing menu options:

      - register user (the program now checks whether the new user to be created exists or not, prompting the user to try a different name if so).
      - view my tasks (user can select which task to view - each displayed task now has a task number - using its number. Viewing a task brings up two further options:
                       * Mark task as complete - the completed tag on the task is changed to 'Yes'.
                       * Edit task (only if it has not been completed) - The user assigned on the task or the task due date can be changed).
      - display statistics (now displays information from task and user overview files -explained next- generated, if not yet gnerated, the program generates the files). 
A new menu option for the admin is added:                       

- generate reports 

    The program creates two text files, __task_overview.txt__ and __user_overview.txt__.
    
    In _task overview_, the following information is created:
            
      ▪ The total number of tasks in the task file.
      ▪ The total number of completed tasks.
      ▪ The total number of uncompleted tasks.
      ▪ The total number of tasks that haven’t been completed and overdue.
      ▪ The percentage of tasks incomplete.
      ▪ The percentage of tasks overdue.
      
    In _user overview_, the following is created:
            
      ▪ The total number of users registered with task_manager.py.
      ▪ The total number of tasks that have been generated using task_manager.py.
      
      ▪ Each user then has the following:
          - The total number of tasks assigned to them.
          - Percentage of the total number of tasks assigned to that user.
          - Percentage of their tasks completed.
          - Percentage of their tasks not yet completed.
          - Percentage of their tasks not yet complete and overdue.
