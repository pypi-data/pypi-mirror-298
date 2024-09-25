# Changelog

### Version - 0.8.3 (2024-09-24)

- Update dependencies: add pymongo==4.8.0.

### Version - 0.8.2 (2024-09-13)

- Implement steps for version check in Publish Package action.
- Improve Publish Package action.
- Add python script to check versions.
- Add python script to install dependencies.
- Add python script to update requirements files.

### Version - 0.8.1 (2024-09-13)

- Update dev-dependencies: add twine==5.1.1.
- Update dev-dependencies: add build==1.2.2.
- Update dev-dependencies: add wheel==0.44.0.
- Update dev-dependencies: add setuptools==74.1.2.
- Update dev-dependencies: add toml==0.10.2.

### Version - 0.8.0

- Implement collection.drop_index().
- Implement collection.drop_indexes().

### Version - 0.7.0

- Update the result of collection.delete_many() from None to deleted_count (int).
- Update the result of collection.delete_one() from None to deleted_count (int).

### Version - 0.6.0

- Implement auto retry for collection.create_indexes().

### Version - 0.5.0

- Update version in pyproject.toml to 0.5.0.
- Improve Docstrings.
- Make the name of an Index optional.

### Version - 0.4.2

- Add Changelog link in pyproject.toml in the project.urls section.
- Update README.md remove useless link from python versions banner.

### Version - 0.4.1

- Update project description in pyproject.toml

### Version - 0.4.0

- Improve and add new Docstrings
- Implement create_indexes method
- Implement create_index method

### Version - 0.3.2

- Update README.md

### Version - 0.3.1

- Add CHANGELOG.md