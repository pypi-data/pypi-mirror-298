from setuptools import setup, find_packages


def main():
    requires = [
        'requests',
        'paramiko',
        'pyyaml',
        'prodict',
    ]

    setup(
        name='sbutils-remote',
        version='0.0.2',
        packages=find_packages(exclude=[]),
        include_package_data=True,
        install_requires=requires,
        author='Stonebranch',
        description='SBUtils but for remote servers',
        entry_points={
            'console_scripts': [
                'rconf=src.uconf:main',
                'rinstall=src.uinstall:main',
            ]
        },
        python_requires='>=2.7',
        classifiers=[
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3'
        ],
        long_description='',
        long_description_content_type="text/x-rst"
    )


if __name__ == '__main__':
    main()
