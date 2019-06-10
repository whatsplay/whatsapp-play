from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name="wplay",
	version="1.0.6",
	install_requires=["selenium >= 3.141.0",
                    "python-telegram-bot >= 11.1.0",
                    "datetime >= 4.3",
                    "webdriver-manager >= 1.7"],
	packages=find_packages(),
	description="command line software to play with your WhatsApp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rohit Potter",
    author_email="rohitpotter12@gmail.com",
    license="MIT",
    python_requires=">=3.4",
    url="https://github.com/rpotter12/whatsapp-play/",
    download_url="https://pypi.org/project/wplay/",
    keywords=[
        "whatsapp",
        "whatsapp-cli",
        "whatsapp-chat",
        "message-blast",
        "tracker"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["wplay = wplay.wplay:main"]},
	)