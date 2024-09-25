from setuptools import setup, find_packages

setup(
    name='bixnox',  # Tên module của bạn
    version='0.1.12',  # Phiên bản
    author='NhoxTom',  # Tên tác giả
    author_email='24hamg@gmail.com',  # Email tác giả
    description='A package for automatically claiming airdrops.',  # Mô tả ngắn
    long_description=open('README.md').read(),  # Đọc mô tả dài từ file README
    long_description_content_type='text/markdown',  # Định dạng mô tả dài
    url='https://github.com/yourusername/yourrepository',  # Đường dẫn đến repo
    packages=find_packages(),  # Tìm và bao gồm tất cả các package
    install_requires=[  # Các phụ thuộc cần thiết
        'colorama',
        'requests',
    ],
    classifiers=[  # Thông tin phân loại
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Chọn giấy phép phù hợp
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Phiên bản Python tối thiểu
)