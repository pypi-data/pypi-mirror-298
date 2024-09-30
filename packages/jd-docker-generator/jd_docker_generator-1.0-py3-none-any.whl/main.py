import argparse
from jinja2 import Template

# Define a base Dockerfile template
DOCKERFILE_TEMPLATE = """
# Generated Dockerfile
FROM {{ base_image }}

{% if maintainer %}MAINTAINER {{ maintainer }}{% endif %}

# Set working directory
WORKDIR /app

# Copy current directory contents into the container
COPY . /app

# Install dependencies
RUN {{ package_manager }} install -y {{ dependencies }}

# Expose port
EXPOSE {{ port }}

# Run the application
CMD ["{{ cmd }}"]
"""

# Function to generate Dockerfile
def generate_dockerfile(base_image, maintainer, package_manager, dependencies, port, cmd):
    template = Template(DOCKERFILE_TEMPLATE)
    return template.render(
        base_image=base_image,
        maintainer=maintainer,
        package_manager=package_manager,
        dependencies=dependencies,
        port=port,
        cmd=cmd
    )

# Function to ask for user input with default values
def prompt_user_input():
    base_image = input("Enter the base image (default: python:3.9): ") or "python:3.9"
    maintainer = input("Enter the maintainer name (optional): ")
    package_manager = input("Enter the package manager (default: apt-get): ") or "apt-get"
    dependencies = input("Enter dependencies to install (default: python3-pip): ") or "python3-pip"
    port = input("Enter the port to expose (default: 5000): ") or "5000"
    cmd = input("Enter the command to run the application (default: python app.py): ") or "python app.py"

    return base_image, maintainer, package_manager, dependencies, port, cmd

# CLI for the generator
def main():
    print("Welcome to jd-docker-create!")
    base_image, maintainer, package_manager, dependencies, port, cmd = prompt_user_input()

    # Generate the Dockerfile content
    dockerfile_content = generate_dockerfile(
        base_image=base_image,
        maintainer=maintainer,
        package_manager=package_manager,
        dependencies=dependencies,
        port=port,
        cmd=cmd
    )

    # Write the Dockerfile to disk
    with open("Dockerfile", "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    print("Dockerfile has been generated successfully!")

if __name__ == '__main__':
    main()
