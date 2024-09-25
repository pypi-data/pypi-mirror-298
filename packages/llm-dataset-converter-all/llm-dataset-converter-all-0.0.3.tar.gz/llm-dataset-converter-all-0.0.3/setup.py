from setuptools import setup


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="llm-dataset-converter-all",
    description="Meta-library that combines all llm-dataset-converter libraries.",
    long_description=(
            _read('DESCRIPTION.rst') + b'\n' +
            _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-llm/audio-dataset-converter-all",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
    ],
    license='MIT License',
    install_requires=[
        "llm-dataset-converter>=0.2.4",
        "ldc-doc>=0.0.2",
        "ldc-docx>=0.0.2",
        "ldc-faster-whisper>=0.0.1",
        "ldc-google>=0.0.1",
        "ldc-html>=0.0.2",
        "ldc-openai>=0.0.1",
        "ldc-pdf>=0.0.2",
        "ldc-tint>=0.0.2",
    ],
    version="0.0.3",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
)
