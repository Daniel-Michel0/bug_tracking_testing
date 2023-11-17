import subprocess

#* Python path
python_path = "venv\Scripts\python.exe"

def run_tests():
    print("Running register_test.py...")
    subprocess.run(["venv\Scripts\python.exe", "home/register_test.py"], check=True)

    print("Running login_send_bug_test.py...")
    subprocess.run(["venv\Scripts\python.exe", "home/login_send_bug_test.py"], check=True)
    
    print("Running reasignacion_test.py...")
    subprocess.run(["venv\Scripts\python.exe", "database/reasignacion_test.py"], check=True)
    
    print("Running asignacion_reportebug_test.py...")
    subprocess.run(["venv\Scripts\python.exe", "database/asignacion_reportebug_test.py"], check=True)
    
    

if __name__ == "__main__":
    run_tests()