import subprocess

#* Python path
python_path = "venv\Scripts\python.exe"

def run_tests():
    print("Running register_test.py...")
    subprocess.run([python_path, "home/register_test.py"], check=True)

    print("Running login_send_bug_test.py...")
    subprocess.run([python_path, "home/login_send_bug_test.py"], check=True)
    
    print("Running reasignacion_test.py...")
    subprocess.run([python_path, "database/reasignacion_test.py"], check=True)
    
    print("Running asignacion_reportebug_test.py...")
    subprocess.run([python_path, "database/asignacion_reportebug_test.py"], check=True)
    
    print("Running crear_casodebug_test.py...")
    subprocess.run([python_path, "database/crear_casodebug_test.py"], check=True)
    
    

if __name__ == "__main__":
    run_tests()