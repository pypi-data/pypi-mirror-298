import setuptools

import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_component/pypi_readme.md'), 'r') as f:
  long_des = f.read()

setuptools.setup(
    name="streamlit-marshal-helloworld",
    version="0.0.1",
    author="Marshal Wu",
    author_email="marshal.wu@gmail.com",
    description="使用 vite 和 vanillajs 编写的 Streamlit hello world 示例",
    long_description=long_des,
    long_description_content_type="text/markdown",
    url="https://github.com/MarshalW/streamlit-demo/tree/main/src/5.custom-components-dynamic-simple",
    keywords = ['some', 'key', 'word'],
    project_urls={
        'Source': 'https://github.com/MarshalW/streamlit-demo/tree/main/src/5.custom-components-dynamic-simple',  
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.10",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.38.0",
    ],
)