import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reinvent_hitl",
    version="0.0.4",
    license="MIT",
    author="Yasmine Nahal",
    author_email="yasmine.nahal@aalto.fi",
    description="Source code of Reinvent adapted to HITL_AL_GOMG workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yasminenahal/reinvent-hitl.git",
    download_url = 'https://github.com/yasminenahal/reinvent-hitl/archive/v_04.tar.gz',
    keywords = ['REINVENT', 'HITL', 'HITL_AL_GOMG'],
    packages=setuptools.find_packages(exclude='unittest_reinvent'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
