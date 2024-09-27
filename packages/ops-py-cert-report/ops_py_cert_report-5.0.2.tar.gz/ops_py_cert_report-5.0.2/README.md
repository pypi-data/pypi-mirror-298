# ops-py-cert-report

## Description

Requests SSL certificate info from a list of URLs and then creates report with status of the SSL certificates.

 The report is available in the following format:
- Slack Markdown
- HTML (table)
- JSON

The report contains the following information for each checked SSL certificate:
- **SSL cert name:** The name of the ssl certificate
- **Status:** `OK`, `Warning`, `Error`, `Critical!!`, `Expired!!`or `Unknown`
- **Message:** Error message or message about days till expire or days since expired
- **Expiration Date:** The expiration date of the SSL certificate

## Installation and Usage
```
pip install ops-py-cert-report

❯ python
Python 3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from cert_report import certs
>>> from cert_report import report
>>> ssl_certs = ["example.com", "google.com"]
>>> c = certs.Certs(ssl_certs)
>>> c.parse_certs()
>>> crts = c.get_certs()
>>> s = report.Report(crts, 45, 14, skip_ok=False)
>>> s.gen_report()
>>> json_report = s.get_report_json()
>>> for x in json_report:
...     print(x)
...
{'name': 'example.com', 'expire_date': 'Mar  1 23:59:59 2025 GMT', 'expire_age': -247, 'comment': 'Will expire in 247 days', 'status': 'OK', 'code': 0}
{'name': 'google.com', 'expire_date': 'Sep  5 15:27:13 2024 GMT', 'expire_age': -70, 'comment': 'Will expire in 70 days', 'status': 'OK', 'code': 0}
>>> html = s.get_html_report()[1]
>>> print(html)
<table bordercolor='black' border='2'>
    <thead>
    <tr style='background-color: Teal; color: White'>
        <th>Status</th>
        <th>SSL Cert</th>
        <th>Message</th>
        <th>Expiration date</th>
    </tr>
    </thead>
    <tbody>
    <tr>
            <td style='background-color: Green; color: White; font-weight:bold'>OK</td>
            <td>google.com</td>
            <td>Will expire in 70 days</td>
            <td>Sep  5 15:27:13 2024 GMT</td>
        </tr>
    <tr>
            <td style='background-color: Green; color: White; font-weight:bold'>OK</td>
            <td>example.com</td>
            <td>Will expire in 247 days</td>
            <td>Mar  1 23:59:59 2025 GMT</td>
        </tr>
    </tbody>
</table>

>>> slck = s.get_slack_report()
>>> print(slck)
*SSL certificates report*
:white_check_mark: *google.com* - Will expire in 70 days (Sep  5 15:27:13 2024 GMT).
:white_check_mark: *example.com* - Will expire in 247 days (Mar  1 23:59:59 2025 GMT).
```
