# GitHub Actions CI/CD Pipeline

This project includes a comprehensive GitHub Actions workflow for continuous integration and testing.

## CI Pipeline Features

### Automated Testing
- **Django Tests**: Runs all Django unit tests using `python manage.py test`
- **Pytest Integration**: Additional test runner with detailed reporting
- **MySQL Database**: Uses MySQL 8.0 service for testing (production-like environment)
- **Database Migration Testing**: Ensures migrations work correctly

### Code Quality Checks
- **Black Formatting**: Ensures consistent code formatting
- **Flake8 Linting**: Checks for code style and potential issues
- **Security Scanning**: Uses Safety to check for known security vulnerabilities

### Performance Optimizations
- **Dependency Caching**: Caches pip dependencies for faster builds
- **Parallel Jobs**: Separates testing and security checks for efficiency

## Configuration Files

### `.github/workflows/ci.yml`
Main CI pipeline configuration that:
- Sets up Python 3.11 environment
- Configures MySQL 8.0 service
- Installs dependencies and system packages
- Runs comprehensive test suite
- Performs code quality checks

### `settings_test.py`
Test-specific Django settings that:
- Configures MySQL database for testing
- Optimizes settings for CI environment
- Includes fallback configurations
- Speeds up password hashing for tests

### Additional Configuration Files
- `pytest.ini`: Pytest configuration and markers
- `.flake8`: Flake8 linting rules and exclusions
- `pyproject.toml`: Black code formatter settings

## Environment Variables

The CI pipeline uses these environment variables:
- `DATABASE_URL`: MySQL connection string
- `SECRET_KEY`: Django secret key for testing
- `DEBUG`: Set to False for testing

## Database Setup

The workflow automatically:
1. Starts MySQL 8.0 service container
2. Creates test database (`test_messaging_app`)
3. Waits for MySQL to be ready
4. Runs Django migrations
5. Executes all tests

## Running Tests Locally

To run tests locally with MySQL:

```bash
# Install dependencies
pip install -r requirements.txt

# Set up MySQL database
mysql -u root -p -e "CREATE DATABASE test_messaging_app;"
mysql -u root -p -e "CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'test_password';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON test_messaging_app.* TO 'test_user'@'localhost';"

# Run tests
python manage.py test --settings=messaging_app.settings_test
pytest --settings=messaging_app.settings_test

# Check code quality
black --check .
flake8 .
```

## Triggering the CI Pipeline

The CI pipeline runs automatically on:
- Push to `main`, `develop`, or `master` branches
- Pull requests to `main`, `develop`, or `master` branches

## Pipeline Status

You can monitor the pipeline status in the GitHub repository under the "Actions" tab.
Each run provides detailed logs for:
- Environment setup
- Dependency installation
- Database configuration
- Test execution
- Code quality checks
- Security scanning

## Troubleshooting

Common issues and solutions:

1. **MySQL Connection Issues**: Check MySQL service status and credentials
2. **Migration Failures**: Ensure database schema is compatible
3. **Test Failures**: Review test logs for specific error details
4. **Code Quality Issues**: Run Black and Flake8 locally before pushing
