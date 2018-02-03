from executor.DefaultExecutor import DefaultExecutor
from Explainer import Explainer

cmd = ['enable', 'show ?', 'exit']
exp = Explainer()
exe = DefaultExecutor(None)

for each in cmd:
    cmdInstance = exp._explain_(each)
    exe = exe._execute_(cmdInstance)

