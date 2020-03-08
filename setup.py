#This python file is used to import the neccessary files for Whatsapp play.


from setuptools import setup, find_packages

#Imports setup and find_packages module from setup tools
with open("README.md", "r") as f:
    long_description = f.read()

#Requirements are the various libraries along with their version.
setup(
    name="wplay",
    version="5.0.2",
    install_requires=["python-telegram-bot >= 11.1.0",
                      "datetime >= 4.3",
                      "playsound >= 1.2.2",
                      "argparse >= 1.4.0",
                      "beautifulsoup4 >= 4.8.1",
                      "pyppeteer >= 0.0.25",
                      "whaaaaat>=0.5.2",
                      "prompt_toolkit==1.0.14",
                      "pyfiglet>=0.8.post1",
                      "requests>=2.22.0",
                      "psutil>=5.7.0",
                      "flake8"
                      ],
    # Checks for the above library packages.
    packages=find_packages(),
    description="command line software to play with your WhatsApp",
    long_description=long_description,
    
    # all about the software description
    
    long_description_content_type="text/markdown",
    author="Rohit Potter, Alexandre Calil",
    author_email="rohitpotter12@gmail.com, alexandrecalilmf@gmail.com",
    license="MIT",
    
    #The minimum python version requirement
    python_requires=">=3.6",
    
    # The url where the software files are located.
    url="https://github.com/rpotter12/whatsapp-play/",
    download_url="https://pypi.org/project/wplay/",
    keywords=[
        "whatsapp",
        "whatsapp-cli",
        "whatsapp-chat",
        "message-blast",
        "message-timer",
        "tracker",
        "online tracking",
        "save-chat"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # This tells about the starting point of software which is the main script as usual.
    entry_points={"console_scripts": ["wplay = wplay.__main__:main"]},
)
