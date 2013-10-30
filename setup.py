try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django_linotp',
    version='0.1',
    description='linotp authentication for django',
    author='Cornelius Koelbel',
    license='GPL v3, (C) Cornelius Koelbel',
    author_email='corny@cornelinux.de',
    url='http://www.github.com/cornelinux/django-linotp-auth',
    install_requires=[
        "django",
    ],
    classifiers=[
		"License :: OSI Approved :: GNU General Public License v3",
		"Programming Language :: Python",
		"Topic :: Internet",
		"Topic :: Security",
	],
    packages = [ 'django_linotp' ]
)
