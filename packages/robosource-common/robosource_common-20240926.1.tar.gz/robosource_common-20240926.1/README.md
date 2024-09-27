# RoboSource Common (Python Edition)

This package contains functionality that RoboSource developers use over and over across multiple client automations. It is public and free to use at your own convenience. We offer no official external support of this package, but drop us a line if you have a suggestion or bugfix to include! If you are using this package and don't know the values for any of the secrets, reach out and we may be able to help you out.

## CoachBot API

### Configuration

In order to call the CoachBot API, you must have endpoint URLs configured in your project:

```
os.getenv('COACHBOT_ATTACH_FILE_ENDPOINT')
os.getenv('COACHBOT_COMPLETE_STEP_ENDPOINT')
os.getenv('COACHBOT_FAIL_STEP_ENDPOINT')
```

### Usage

