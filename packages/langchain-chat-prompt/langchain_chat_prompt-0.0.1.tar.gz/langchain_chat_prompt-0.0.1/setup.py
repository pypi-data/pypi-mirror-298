from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Langchain chat prompt'
LONG_DESCRIPTION = 'A package that allows to build prompt engineering with easy steps.'
LONG_DESCRIPTION = 'A package that allows to build prompt engineering with easy steps.'

# Setting up
setup(
    name="langchain_chat_prompt",
    version=VERSION,
    author="Kamal Bahadur Shahi",
    author_email="<kamal.shahi@olivegroup.io>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['langchain_openai', 'langchain'],
    keywords=['python', "lang chain", "openai",
              "package", "prompt engineering"],
)
