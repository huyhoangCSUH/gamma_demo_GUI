import subprocess
subprocess.check_call(['Rscript', 'linreg.R', 'diabetes', '9'], shell=False)