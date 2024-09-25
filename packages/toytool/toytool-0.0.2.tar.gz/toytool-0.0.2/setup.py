import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def read_version():
    import subprocess
    result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
    print(result.stdout)
    with open("VERSION", "r", encoding="utf-8") as fh:
        version = fh.read()
    return version

setuptools.setup(
    name="toytool",
    version=read_version(),
    author="HandsomeBoy",
    author_email="putaoisapig@163.com",
    description="toy-tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pillow", "opencv-python", "opencv-python-headless"]
)
