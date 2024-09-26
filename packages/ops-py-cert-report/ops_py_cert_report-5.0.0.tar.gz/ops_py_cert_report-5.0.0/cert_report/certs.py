#!/usr/bin/env python

import ssl
import socket
import logging
from datetime import datetime
from operator import itemgetter


########################################################################################################################


def set_timestamp(fmt, s):
    """Returns a date object of a string in the provided format (fmt).

    The string has to be in the correct format, if not None is returned."""

    try:
        ts = datetime.strptime(str(s.strip()), fmt)
    except ValueError:
        logging.error(f"Unable to convert provided argument '{str(s)}' to timestamp object")
        return

    return ts


class Certs(object):
    """Request a list of URLs about SSL certificate info.

        Creates a dict for each cert which are added to a list.

        Attributes
        ----------
        urls : The list of URLs to be checked
        date_format : The dateformat of the returned expire date, which are converted to datetime object
        now : Current date and time object
        certs : The list of parsed SSL certs, each a dict object.

    """

    # set default socket time out to five seconds
    socket.setdefaulttimeout(5)

    def __init__(self, urls, warning=29, critical=13):

        self.urls = urls
        self.warning = warning
        self.critical = critical
        self.codes = {
            "ok": ["OK", 0],
            "warning": ["Warning", 1],
            "critical": ["Critical", 2],
            "error": ["Error", 3],
            "unknown": ["Unknown", 4],
            "expired": ["Expired", 5]
        }

        self.date_format = "%b %d %H:%M:%S %Y"
        self.now = datetime.now()
        self.certs = []
        self.report = []

    def parse_certs(self):
        """Parses through the list of provided URLs.

         Each URL are passed to the ssl_cert_expire() method which requests the URL and check the cert.

        Requests the passed URL and appends the result as dict to the list of checked certs
        """

        for url in self.urls:
            # Creates an empty json of the cert
            # If the url does not contain a cert (or a valid cert) it also will not contain an expiration date.
            # In that case a default high expire age will be set due to sorting.
            c = {"name": url,
                 "notAfter": None,
                 "expire_ts": None,
                 "expire_age": 999999,
                 "error_message": None
                 }

            # Executes the request to retrieve the SSL cert info and populate the cert dict
            context = ssl.create_default_context()
            try:
                with socket.create_connection((url, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=url) as s:
                        s.do_handshake()
                        cert = s.getpeercert()
                        not_after = cert.get("notAfter")
                        ts = set_timestamp(self.date_format, not_after.rstrip("GMT"))
                        age = (self.now - ts).days
                        c["notAfter"] = not_after
                        c["expire_ts"] = ts
                        c["expire_age"] = age
            except ssl.SSLCertVerificationError as e:
                c["error_message"] = e.verify_message
            except socket.gaierror as e:
                c["error_message"] = e.strerror
            except socket.error as e:
                c["error_message"] = str(e)
            finally:
                self.certs.append(c)

    def gen_report(self):
        """parses through the ssl certs to generate json reports"""

        for c in self.certs:
            name = c.get("name")
            expire_date = c.get("notAfter")
            days = c.get("expire_age")
            error_message = c.get("error_message")

            # add error message if any
            if error_message:
                status = "error"

                e = "certificate is not valid"
                if e in error_message:
                    # strip this unnecessary long error message
                    error_message = f"{error_message.split(e)[0]}{e}"

                if "expired" in error_message:
                    status = "expired"

                comment = error_message

            # if no error message, then check the expiration date and then the comment and status
            elif not error_message and isinstance(days, int) and days < 0:
                comment = f"Will expire in {abs(days)} days"
                if abs(days) <= self.critical:
                    status = "critical"
                elif self.warning >= abs(days) > self.critical:
                    status = "warning"
                else:
                    status = "ok"

            # if no error message, but the cert has already expired
            elif not error_message and isinstance(days, int) and days >= 0:
                comment = f"Has already expired. Expired {abs(days)} days ago."
                status = "critical"
            else:
                status = "unknown"
                comment = f"Unknown state for cert **{name}**."

            self.report.append(
                {
                    "status": self.codes.get(status)[0],
                    "name": name,
                    "comment": comment,
                    "expire_date": expire_date,
                    "expire_age": days,
                    "code": self.codes.get(status)[1]
                }
            )

    def get_certs(self):
        """Returns the list for checked ssl cert"""

        return self.certs

    def get_report(self, delete=()):
        """returns a sorted list of ssl certs dict reports"""
        report = []
        for s in sorted(self.report, key=itemgetter("code", "expire_age"), reverse=True):
            for d in delete:
                if d in s:
                    del s[d]
            report.append(s)
        return report
