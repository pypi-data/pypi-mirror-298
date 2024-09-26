from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Robocon_24',
    version='0.3.4',
    author='Charan A A',
    author_email='mariswarycharan@gmail.com',
    description='This project is designed to detect balls and make decisions based on their positions in the context of a Robocon competition.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mariswarycharan/Robocon_24_version',  # Update with your GitHub repository URL
    packages=find_packages(),
    keywords=['Robocon', 'Ball', 'Detection', 'Decision', 'Making', 'Computer Vision', 'YOLO', 'Ultralytics', 'OpenCV', 'Python','Ball Detection','Ball Decision Making','Robocon 2024','Robocon 24'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", 

    ],  # Specify the Python versions you support here. In particular, ensure
    install_requires=[
        'opencv-python',
        'ultralytics',
],
    project_urls={
        'Homepage': 'https://github.com/mariswarycharan/Robocon_24_version',  # Replace with your homepage URL
        'Download': 'https://github.com/mariswarycharan/Robocon_24_version.git',  # Replace with your download URL
        'Documentation': 'https://github.com/mariswarycharan/Robocon_24_version/blob/main/README.md',  # Replace with your documentation URL
        'Issue tracker': 'https://github.com/mariswarycharan/Robocon_24_version/issues',  # Replace with your issue tracker URL
        'Source code': 'https://github.com/mariswarycharan/Robocon_24_version',  # Replace with your source code URL
        'GitHub Statistics': 'https://github.com/mariswarycharan/Robocon_24_version',  # Replace with your GitHub repository URL
    },
)