import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    apiStorageDB = threading.Thread(target=run_script, args=("../databases/createAPIstorage.py",))
    contactbook = threading.Thread(target=run_script, args=("../databases/createContactbook.py",))
    userDB = threading.Thread(target=run_script, args=("../databases/createDatabase.py",))
    projectsDB = threading.Thread(target=run_script, args=("../databases/createProjectsDB.py",))
    tasksDB = threading.Thread(target=run_script, args=("../databases/createTasksDB.py",))

    apiStorageDB.start()
    contactbook.start()
    userDB.start()
    projectsDB.start()
    tasksDB.start()

    apiStorageDB.join()
    contactbook.join()
    userDB.join()
    projectsDB.join()
    tasksDB.join()

    print("All databases have been reset.")