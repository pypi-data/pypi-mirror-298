from setuptools import setup, find_packages

setup(
    name="uz-ai",  # Kutubxonangiz nomi
    version="0.0.1",  # Versiya raqami
    author="Salohiddin Esanbekov",  # Muallif ismi
    author_email="email@manzil.com",  # Muallif emaili
    description="siz UzAi da sun'iy intelektlar yarata olasiz",  # Kutubxonangiz tavsifi
    long_description=open('README.md').read(),  # Batafsil tavsif (README.md faylidan olinadi)
    long_description_content_type="text/markdown",
    url="https://github.com/UzCoder123",  # GitHub havolangiz
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
