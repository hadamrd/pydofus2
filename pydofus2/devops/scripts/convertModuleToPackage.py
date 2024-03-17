import os

path="../pyd2bot/pyd2bot"

for root, dirs, files in os.walk(path):
    for dir in dirs:
        if not os.path.exists(os.path.join(root, dir, "__init__.py")):
            with open(os.path.join(root, dir, "__init__.py"), "w") as f:
                f.write("")