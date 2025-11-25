# generate_requirements.py
import pkg_resources

# packages for the  project
packages = ["numpy", "matplotlib", "pandas", "tabulate"]

# Open a file to write requirements
with open("requirements.txt", "w") as f:
    for package in packages:
        try:
            version = pkg_resources.get_distribution(package).version
            f.write(f"{package}=={version}\n")
            print(f"{package}=={version} added to requirements.txt")
        except pkg_resources.DistributionNotFound:
            print(f"{package} is not installed.")
