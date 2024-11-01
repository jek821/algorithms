# input data is structured so that each index corresponds to the indexes of other arrays
# task a at tasks[0] corresponds to the values at index[0] in process_times and potential_start_times
task_names = ['a', 'b', 'c', 'd', 'e', 'f']
task_process_times = [3, 9, 1, 17, 4, 12]
potential_start_times = [6, 2, 7, 4, 0, 3]





def plan_tasks(task_names, task_process_times, potential_start_times):
    # dictionary which will hold all info for each task in the form (potential_start_time : (task,process_times))
    # dictionary will be sorted in ascending order of process_times
    task_info = {}
    # empty array which will store all of the tasks which can currently be processed
    # this array will tore tuples (task, remaining_process_time)
    possible_tasks = []
    # task_log array, where index represents time interval and value at that index is the task processed at that time
    task_log = []

    # first I will populate the task_info dictionary
    for index in range(len(task_names)):
        task_info[potential_start_times[index]] = (task_names[index], task_process_times[index])
    # now i will sort the task_info dictionary by process time
    task_info = dict(sorted(task_info.items(), key=lambda item: item[1][1]))
    
    # Now I can iterate through all the tasks tracking the current time interval
    # the total time is equal to the sum of all the processing times so we will iterate from t = 0 through t = sum(task_process_times)
    for t in range(sum(task_process_times) + 1):
        tasks_to_remove = []
        for start_time in list(task_info.keys()):
            # if task's potential start time is less than or equal to the current time we can add it to possible_tasks
            if start_time <= t:
                # Append task to possible_tasks and remove from task_info
                task_name, task_time = task_info[start_time]
                possible_tasks.append([task_name, task_time])
                tasks_to_remove.append(start_time)
                
        # Remove tasks from task_info
        for task in tasks_to_remove:
            del task_info[task]
        
        # Sort possible_tasks by remaining process time to always choose the shortest job
        possible_tasks.sort(key=lambda x: x[1])

        if len(possible_tasks) == 0:
            task_log.append("idle")
        else:
            # current task to process is whatever is stored at index 0 of possible tasks
            curr_task = possible_tasks[0]
            # add that task to the task log so we know which task we processed at each time interval
            task_log.append(curr_task[0])
            # decrement the task's process time by one to account for processing it at this time interval 
            curr_task[1] -= 1
            if curr_task[1] == 0:
                possible_tasks.pop(0)  # remove the task if completed
    
    # Once we are finished going through each time interval, we can return the log of which tasks were processed when
    return task_log


print(plan_tasks(task_names,task_process_times,potential_start_times))

