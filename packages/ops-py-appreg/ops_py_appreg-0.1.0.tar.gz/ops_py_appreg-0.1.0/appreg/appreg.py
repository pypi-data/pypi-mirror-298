#!/usr/bin/env python

import logging
from set_timestamp import set_timestamp, now
from operator import itemgetter

########################################################################################################################


class AppReg(object):
    def __init__(self, results, warning=29, critical=13):
        self.results = results
        self.warning = warning
        self.critical = critical
        self.items = []
        self.date_format = "%Y-%m-%dT%H:%M:%S"
        self.codes = {
            "ok": ["OK", 0],
            "warning": ["Warning", 1],
            "critical": ["Critical", 2],
            "error": ["Unknown", 3],
            "expired": ["Expired", 4]
        }

    def parse_credentials(self, items, app_id, app_display_name, record_type):
        for item in items:
            ts = None
            age = "-"
            display_name = item.get("displayName")
            if not display_name:
                display_name = "No description"

            start_date_time = item.get("startDateTime")
            end_date_time = item.get("endDateTime")
            if end_date_time:
                ts = set_timestamp(end_date_time[:19], date_format=self.date_format)
            if ts:
                age = (now() - ts).days

            d = {
                "status": "-",
                "appId": app_id,
                "displayName": app_display_name,
                "recordDisplayName": display_name,
                "type": record_type,
                "startDateTime": start_date_time[:19],
                "endDateTime": end_date_time[:19],
                "age": age
            }

            self.set_status(d)
            self.items.append(d)

    def set_status(self, d):
        status = "unknown"
        age = d.get("age")
        comment = ""

        if isinstance(age, int):
            if age > 0:
                status = "expired"
                comment = f"Expired {abs(age)} days ago."
            else:
                comment = f"Will expire in {abs(age)} days."
                if abs(age) <= self.critical:
                    status = "critical"
                elif self.critical < abs(age) <= self.warning:
                    status = "warning"
                elif abs(age) > self.warning:
                    status = "ok"

        msg = self.codes.get(status)[0]
        code = self.codes.get(status)[1]

        d["comment"] = comment
        d["status"] = msg
        d["code"] = code

    def parse_results(self):
        if not isinstance(self.results, list):
            logging.error(f"The provided results must be a list.")
            return

        for result in self.results:
            app_id = result.get("appId")
            display_name = result.get("displayName")
            key_credentials = result.get("keyCredentials")
            password_credentials = result.get("passwordCredentials")

            if key_credentials:
                self.parse_credentials(key_credentials, app_id, display_name, "Certificate")

            if password_credentials:
                self.parse_credentials(password_credentials, app_id, display_name, "Client secret")

    def get_items_sorted(self):
        report = []
        for s in sorted(self.items, key=itemgetter("code", "age"), reverse=True):
            del s["code"]
            del s["age"]
            report.append(s)
        return report

    def get_items(self):
        return self.items

