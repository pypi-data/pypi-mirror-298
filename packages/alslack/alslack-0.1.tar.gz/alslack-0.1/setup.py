import setuptools 
setuptools.setup( 
    name='alslack', 
    version='0.1', 
    author="Autumn Leaf IT South Africa", 
    author_email="george@al.co.za", 
    url="https://al.co.za/",
    description="Provides a Slack Notification client supports custom messages and forms part of the AL Notification Modules Suite.", 
    packages=setuptools.find_packages(),  # install_requires=['pandas','pytest','black']
    long_description="Provides a Slack Notification client supports custom messages and forms part of the AL Notification Modules Suite.",
    long_description_content_type="text/markdown",
    classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent" ], 
    requires=["requests","json"]
)
