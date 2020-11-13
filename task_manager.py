#Capstone Project IV
#imports
from datetime import date
from datetime import datetime
import os.path

today = date.today().strftime("%d %b %Y") #Getting and saving today's date, then formatting it as 'dd mon yyy'
current_user = ''                         #Creating empty variable to keep track of user for later usage

generated_tasks = 0
generated_users = 0

report_generated = False

#Login
print("Login")
print("=============")

"""login function - Takes the user's username and checks if that name is in the user.txt file, 
if so (and the password is correct) the program proceeds to the next menu
If the user does not exist or the password is incorrect the program asks the user to input their credentials again, until they are correct.
The user is not made aware of which of their credentials is incorrect as it is a security concern, however, that can be added if needed.
"""
def try_login():
    username = input("Enter username:\n> ")
    password = input("Enter password:\n> ")
    loggedin = False
    with open("user.txt", "r") as userfile:         #Reads the file
        for line in userfile:
            user = line.split()[0].strip(",")       #loops through the file
            user_password = line.split()[1]
            if username == user:
                if password == user_password:
                    loggedin = True
                #print("Password incorrect.")      #uncomment this line to know if the password is incorrect.
    if loggedin:
        print("Log in successful.\n")
        global current_user                     #making the current user a global variable so it is not updated within the login function only
        current_user = username
        open_menu()
    else:
        print("Username/Password incorrect. Please try again.\n")
        try_login()                             #Should the credentials be incorrect, the user is asked to try again
        
"""open menu function - only visible once user has logged in. Presents user with menu options 
and opens the necessary funtions depending on user input.
If the current user is the admin he has two more menu options.
"""
def open_menu():
    print("Please select one of the following options:\n===========================================")
    if current_user == 'admin':
        menu_option = input("'r' - register user\n'a' - add task\n'va' - view all tasks\n'vm' - view my tasks\n'gr' - generate reports\n's' - statistics\n'e' - exit\n> ")
    else:
        menu_option = input("'r' - register user\n'a' - add task\n'va' - view all tasks\n'vm' - view my tasks\n'e' - exit\n> ")
    if menu_option == 'r':
        register_user()
    elif menu_option == 'a':
        add_task()
    elif menu_option == "va":
        view_all_tasks()
    elif menu_option == "vm":
        view_my_tasks()
    elif menu_option == "gr":
        if current_user == "admin":
            generate_reports()
        else:                   #generate reports only functional(and visible) if the user is an admin. This is a fail safe for the explorative non admin users
            print("Nothing to see here.")
            goto_menu()
    elif menu_option == "s":
        if current_user == "admin":
            view_statistics()
        else:                   #if the non admin users select 's' as an option, which isn't available to them. the program takes them back to the menu
            print("Nothing to see here.")
            goto_menu()
    elif menu_option == "e":
        print("Goodbye")
        quit()
    else:               #If the user enter an invalid command. the program prompts them to try again. 
        print("Your input is unrecognized. Please try again.")
        goto_menu()

#register user function, creates a new user (only if you are the admin) and writes the user to the user.txt file
#Program also checks whether the user to be created already exists, asks the admin to try again with another username if so.
def register_user():
    if current_user == 'admin':
        new_username = input("Enter new username:\n> ")
        check_user_exists(new_username)                     #call the function to check if username already exists

        if not user_exists:                                 #If user doesn't exist, program continues adding the user
            new_password = input("Enter new password:\n> ")
            confirm_new_password = input("Please confirm new password: \n> ")   #ask for password again

            if new_password == confirm_new_password:        #Check if passwords match
                with open("user.txt", "a") as userfile:
                    userfile.write(f"\n{new_username}, {new_password}")
                print(f"{new_username} registered successfully.")
                global generated_users
                generated_users += 1
                goto_menu()

            elif new_username != confirm_new_password:      #If passwords do not match the user is asked to try again
                print("Passwords do not match. Please retry.")
                register_user()
        else:                                               #else if the user does exist, admin is asked to try a different name
            print(f"The user '{new_username}' already exists. Please try a different username")
            register_user()
    else:                   #If user is not an admin, they can't add users
        print("Only the admin is permitted to register new users.")
        goto_menu()

"""Add task function, the program checks if the user(who the task will be added under) exists first and if not, it prompts the user to try again,
if the user does exist, then the program gets the required details for the task and proceeds to write them into the task.txt file
"""
def add_task():
    task_user = input("Enter username of the person the task is to be assigned to:\n> ")
    check_user_exists(task_user)                            #Check if user exists
            
    if user_exists:
        print(f"Adding task for {task_user}:")
        task_title = input("Enter the title of the task:\n> ")
        task_description = input("Enter the description of the task:\n> ")
        task_duedate = input("Enter the due date(e.g. 07 Mar 2020) for the task:\n> ")
        task_dateassigned = today
        task_complete = "No"    
        with open("tasks.txt", "a") as taskfile:
            taskfile.write(f"\n{task_user}, {task_title}, {task_description}, {task_dateassigned}, {task_duedate}, {task_complete}")
            print("Task added successfully.\n")
            global generated_tasks
            generated_tasks += 1

        goto_menu()

    else:
        print(f"{task_user} does not exist. Try again")
        add_task()

#view all tasks function - gets and displays all the tasks currently in the task.txt file
def view_all_tasks():
    print(f"Showing all tasks\n========================")
    with open("tasks.txt", "r") as taskfile:            #Reads the file
        for line in taskfile:
            task_user = line.split(",")[0]              #Splits the different string parts into variables
            task_title = line.split(",")[1]         
            task_description = line.split(",")[2]
            task_dateassigned = line.split(",")[3]
            task_duedate = line.split(",")[4]
            task_complete = line.split(",")[5]
            #Printing and organizing the parts into a user friendly format 
            print(f"User\t\t:{task_user}\nTitle\t\t:{task_title}\nDescription\t:{task_description}\nDate assigned\t:{task_dateassigned}\nDate due\t:{task_duedate}\nComplete\t:{task_complete}")
    goto_menu()
            
#view my tasks function checks the current user and displays their relevant tasks from task.txt. 
def view_my_tasks():
    print(f"Showing tasks for {current_user} \n========================")
    task_counter = 1                                        #Task counter to see the task number
    with open("tasks.txt", "r") as taskfile:
        for line in taskfile:
            task_user = line.split(",")[0]                  #Checks which user the task belongs to
            if task_user == current_user:                   #If task user is the current user, display the task
                task_title = line.split(",")[1]
                task_description = line.split(",")[2]
                task_dateassigned = line.split(",")[3]
                task_duedate = line.split(",")[4]
                task_complete = line.split(",")[5]
                print(f"Task : {task_counter}")
                print(f"Title\t\t:{task_title}\nDescription\t:{task_description}\nDate assigned\t:{task_dateassigned}\nDate due\t:{task_duedate}\nComplete\t:{task_complete}")
                task_counter += 1                           #Increment task counter after every task displayed
    open_task()

    if task_number <= task_counter -1:                  #chosen task number is compared to existing tasks.. Display an error if user chooses tasks that aren't presented
        with open("tasks.txt", "r") as taskfile:
            content = taskfile.readlines()
            current_task = content[task_number - 1]       #If chosen task exits, only that task is diplayed

            task_title = current_task.split(",")[1]
            task_description = current_task.split(",")[2]
            task_dateassigned = current_task.split(",")[3]
            task_duedate = current_task.split(",")[4]
            task_complete = current_task.split(",")[5]
            print(f"Task : {task_number}")
            print(f"Title\t\t:{task_title}\nDescription\t:{task_description}\nDate assigned\t:{task_dateassigned}\nDate due\t:{task_duedate}\nComplete\t:{task_complete}")
        
        complete_or_edit_task = int(input(f"1. Mark task as completed\n2. Edit task {task_number}\n> "))    #User asked to complete or edit task

        if complete_or_edit_task == 1:                  #If user chooses to complete task
        
            with open("tasks.txt", "r") as taskfile:
                content = taskfile.readlines()
                line_to_edit = content[task_number-1]
                line_to_edit = line_to_edit.replace(", No", ", Yes")    #The tasked is then edited to show it being complete
                content[task_number - 1] = line_to_edit

                with open("tasks.txt", "w") as taskfile:    
                    taskfile.writelines(content)                #Completed task written back into task file

        
        elif complete_or_edit_task == 2:                #If user chooses to edit the task
            
            with open("tasks.txt", "r") as taskfile:
                content = taskfile.readlines()
                current_task = content[task_number-1]
                is_task_completed = False                   #Initializing a task complete variable(To false)

                if current_task.find(", No") > 0 :      #If the task is stated as not complete in the task file
                    is_task_completed = False               #the task complete variable is set to false
                else:
                    is_task_completed = True                #else, the task complete is set to true
                
                if is_task_completed:               #If task complete, user isn't allowed to edit it, program goes back to task viewer
                    input("Task has already been completed. Press Enter")
                    view_my_tasks()
                else:   
                    edit_user_or_date = int(input("1. Edit user\n2. Edit date\n> "))    #presenting options for editing the task(if not complete)
                    if edit_user_or_date == 1:              #If user chooses to change task user
                        edited_user = input("Enter name of new user :\n> ").lower()     
                        #Check if the user exists in the users file, if so replace the old user and write the new user back into the users file
                        check_user_exists(edited_user)      
                        if user_exists:
                            old_user = current_task.split(",")[0]
                            current_task = current_task.replace(old_user, edited_user)
                            content[task_number - 1] = current_task
                            with open("tasks.txt", "w") as taskfile:
                                taskfile.writelines(content)
                            input("User successfully changed. Press Enter")
                            open_menu()
                        #else if the user doesn't exist go back to task viewer
                        else:
                            input("User does not exist. Press Enter")
                            view_my_tasks()

                    elif edit_user_or_date == 2:            #If user chooses to change task due date
                        edited_date = input("Enter new due date (e.g. 25 Oct 2019):\n> ")
                        old_duedate = current_task.split(",")[4]
                        current_task = current_task.replace(old_duedate, f" {edited_date}")     #old date replaced with new date
                        content[task_number - 1] = current_task
                        with open("tasks.txt", "w") as taskfile:
                            taskfile.writelines(content)        #Writing task with new date back into the task file
                        input("Due date successfully changed. Press Enter")
                        open_menu()

                    else :                      #Else if the user enters an invalid option, go back to task viewer
                        print("Invalid input. Press Enter")
                        view_my_tasks()

    


        else:               #Else if the user enters an invalid option(if not complete or edit task), go back to task viewer
            print("Invalid input. Press Enter")
            view_my_tasks()

    else:       #else if the user chooses an task number that isn't presented to them.
        print("That task number does not exist. Please try again.")
        view_my_tasks()

#function for creating reports/overview of the tasks and users
def generate_reports():
    #Task reports
    total_tasks = 0                 #Initializing counters and empty strings to be used later in the code.
    tasks_completed = 0
    tasks_not_completed = 0
    tasks_overdue = 0
    task_data = ''
    #opening task file, reading contents, then looping through the content
    with open("tasks.txt", "r") as taskfile:
        content = taskfile.readlines()
        for task in content:
            if task.find(", Yes") > 0:
                tasks_completed += 1                #incrementing task completed counter if tasks contain the completed indication
            #getting due date from task and pasrsing it (along with todays date) so the dates can be compared to see if a task is overdue
            task_duedate = task.split(", ")[4]
            task_duedate = datetime.strptime(task_duedate, "%d %b %Y")
            date_today = datetime.strptime(today, "%d %b %Y")
            if task.find(", No") > 0 and task_duedate < date_today:
                tasks_overdue += 1

            total_tasks += 1                    #incrementing task counter for every task in the content
        #calculating the tasks not completed and overdue and their percentage against the total tasks
        tasks_not_completed = total_tasks - tasks_completed
        percentage_incomplete = round((tasks_not_completed / total_tasks) * 100, 2)
        percentage_overdue = round((tasks_overdue / total_tasks) * 100, 2)
    
    #empty string from before is then populated in a user friendly manner with information on the tasks
    task_data += f"Total tasks \t\t\t\t:{total_tasks}\n"
    task_data += f"Tasks generated using Task manager \t:{generated_tasks}\n"
    task_data += f"Tasks completed \t\t\t:{tasks_completed}\n"
    task_data += f"Tasks not completed \t\t\t:{tasks_not_completed}\n"
    task_data += f"Tasks not completed and overdue \t:{tasks_overdue}\n"
    task_data += f"% Tasks incomplete \t\t\t:{percentage_incomplete}%\n"
    task_data += f"% Tasks overdue \t\t\t:{percentage_overdue}%\n"


    #user reports
    user_data = ''                  #initializing empty variables
    total_users = 0
    users_list = []
    #Initializing empty dictionaries to keep track of user data
    users_dict = {}                 #this is the total tasks per user dicitonary
    user_taskcomplete_dict = {}
    user_taskoverdue = {}
    #opening user file and parsing the text into usable data
    with open("user.txt", "r") as userfile:
        for line in userfile:
            total_users += 1                #increment number of users for every line in user file
            user = line.split(",")[0]
            if user not in users_list:
                users_list.append(user)     #creating a list with all the users, the check is done to ensure no duplicates are added, as the list will be used in conjuction with the dictionaries
    #using the created list, the users are then added to the dictionaries as keys 
    for user in users_list:
        users_dict[user] = 0
        user_taskcomplete_dict[user] = 0
        user_taskoverdue[user] = 0
         
    #opening task file and parsing the data
    with open("tasks.txt", "r") as taskfile:
        for line in taskfile:
            task_user = line.split(",")[0]
            for user in users_list:         
                if user == task_user:               #if user in list == user on the task, 
                    users_dict[user] += 1           #append the amount of tasks the user has in the relevant dictionary
                    if line.find(", Yes") > 0:
                        user_taskcomplete_dict[user] += 1   #append number of completed tasks
                    #parsing the dates to check which user's tasks are overdue    
                    task_duedate = line.split(", ")[4]
                    task_duedate = datetime.strptime(task_duedate, "%d %b %Y")
                    date_today = datetime.strptime(today, "%d %b %Y")
                    if task_duedate < date_today and line.find(", No") > 0:     #if task is overdue and incomplete
                        user_taskoverdue[user] += 1         #appending user's overdue tasks
            
    #The information is then appended to a user_data string in a neat manner
    user_data += f"Total users \t\t\t\t:{total_users}\n"
    user_data += f"Users Generated with Task manager \t:{generated_users}\n"
    user_data += "\n"
    #number of total tasks are retrieved from the relevant dictionary 
    user_data += "Total tasks assigned to user\n"
    for user, tasks in users_dict.items():
        user_data += f"{user} \t\t\t\t:{tasks} total tasks\n"
    user_data += "\n"
    #percentage of tasks assigned to user is calculated using their tasks divided by total tasks(calculated earlier on)
    user_data += "Percentage of Total tasks assigned to user\n"
    for user, tasks in users_dict.items():
        user_data += f"{user} \t\t\t\t:{round((tasks/total_tasks)*100, 2)} %\n"
    user_data += "\n"
    #percentage of tasks completed by a user = their completed tasks divided by their total tasks
    user_data += "Percentage of tasks completed by user\n"
    for user in users_list:
        if user_taskcomplete_dict[user] != 0:       #added to ensure there is no zerodivision error if a user doesn't have completed tasks
            percentage_complete = round((user_taskcomplete_dict[user]/users_dict[user])*100, 2)
        else:
            percentage_complete = 0         
        user_data += f"{user} \t\t\t\t:{percentage_complete} %\n"
    user_data += "\n"
    # % of tasks incomplete by a user = (their tasks - completed tasks) divided by their total tasks
    user_data += "Percentage of tasks that must still be completed by user\n"
    for user in users_list:
        if users_dict[user] != 0:           #Added to prevent a zerodivision error if user doesn't have any tasks assigned to them
            percentage_to_complete = round(((users_dict[user]-user_taskcomplete_dict[user])/users_dict[user])*100, 2)
        else:
            percentage_to_complete = 0
        user_data += f"{user} \t\t\t\t:{percentage_to_complete} %\n"
    user_data += "\n"
    # % tasks incomplete and overdue = overdue tasks divided by their total tasks
    user_data += "Percentage of tasks not yet completed and overdue\n"
    for user in users_list:
        if users_dict[user] != 0:           #Preventing zerodivision error if user has no tasks,. 
            percentage_to_complete_and_overdue = round((user_taskoverdue[user]/users_dict[user])*100, 2)
        else:
            percentage_to_complete_and_overdue = 0      #Their tasks are therefore assigned to zero
        user_data += f"{user} \t\t\t\t:{percentage_to_complete_and_overdue} %\n"

    #Writing the task and user data strings into the relevant txt files
    with open("task_overview.txt", "w") as task_overview:
        task_overview.writelines(task_data)
    with open("user_overview.txt", "w") as user_overview:
        user_overview.writelines(user_data)
    
    #show report generated the return back to menu
    print("Report generated.")

    goto_menu()


#view statistics function, displays data from the generated report files form above 
def view_statistics():
    if os.path.exists("task_overview.txt"): #check if generated files exist first then read and display the content
        with open("task_overview.txt", "r") as task_report:
            task_content = task_report.read()
        with open("user_overview.txt", "r") as user_report:
            user_content = user_report.read()

        print(f"Task overview:\n{task_content}")
        print(f"User overview:\n{user_content}")
    else:               #else if files dont exist, inform user then generate the files
        print("Report not yet generated. Please view statistics again after it is generated.")
        generate_reports()

    goto_menu()

#go to menu function created to allow the user to go back to the main menu when they are ready to, using an empty input to confirm
def goto_menu():
    input("\n(Press Enter to go back.)")
    open_menu()

"""Check if user exists function for when a new user is being created, or a task is being created for a user,
takes the username as an argument and returns whether that user exists or not."""
def check_user_exists(username):
    global user_exists
    user_exists = False
    with open("user.txt", 'r') as userfile:
        for line in userfile:
            user = line.split(",")[0]
            if user == username:
                user_exists = True

    return user_exists

def open_task():
    global task_number
    task_number = int(input("Enter the number of the task you want to view. '-1' to go back to the main menu.\n> "))
    if task_number == -1:
        open_menu()
    else:
        return task_number

#After defining functions, program can now run, calling the login function to begin.
try_login()

