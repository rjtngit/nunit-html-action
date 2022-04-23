# NUnit HTML Report

This Github Action generates a human-readable HTML report from NUnit XML test results.

![](example.png)

## Usage

```yaml
- name: Generate HTML test report
  uses: rempelj/nunit-html-action@v1.0.1
  if: always()
  with:
    inputXmlPath: artifacts/results.xml
    outputHtmlPath: artifacts/results.html
```

## License

The scripts and documentation in this project are released under the [MIT License](https://github.com/rempelj/nunit-html-action/blob/main/LICENSE).
