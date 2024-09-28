import pathlib, setuptools

setuptools.setup(
    name='j2gpt-template',
    version='0.2.1',
    description='Create LLM pipelines with ease!',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/yaz008/j2gpt-template',
    author='Emelianov Artem',
    author_email='yaz008.yaz008@yandex.ru',
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True
)