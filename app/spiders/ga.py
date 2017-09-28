from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from reporter import SpiderReporter
from .. import scheduler
from ..models import Affiliate, History, db
from env import KEYFILE_PATH

import logging
import datetime
import json
import dateutil.relativedelta
import urllib

class GoogleAnalyticsReport(object):
    """
    docstring for GoogleAnalyticsReport
    """
    def __init__(self):
        logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.KEY_FILE_LOCATION = KEYFILE_PATH + '/ga_keyfile.json'
        self.VIEW_ID = '134163596'
        self.report = SpiderReporter()
        self.affiliates_map = {
            '10 bet app': 'Bet10',
            '888sport': 'Eight88',
            'coralbetting': 'Coral',
            'ladbrokes-sports': 'LadBrokes',
            'realdealbet': 'Real',
            'Bet365': 'Bet365',
            'bet365': 'Bet365',
            'betvictor': 'Victor',
            'paddypower': 'Paddy',
            'skybet': 'SkyBet',
            'william-hill': 'William',
            'betfred': 'BetFred',
            'titanbet': 'TitanBet',
            'netbet': 'NetBet',
            'stanjamescasino': 'StanJames',
        }
        pass

    def get_delta_date(self, delta = 2, format_string = "%Y/%m/%d"):
        today = datetime.datetime.today()
        diff = datetime.timedelta(days = delta)
        return (today - diff).strftime(format_string)

    def log(self, message, type = 'info'):
        created_at = self.get_delta_date()
        if type == 'error':
            self.log_error(message)
        else:
            self.report.write_log("GA", message, created_at)

    def log_error(self, message):
        created_at = self.get_delta_date()
        self.report.write_error_log("GA", message, created_at)

    def initialize_analyticsreporting(self):
        """Initializes an Analytics Reporting API V4 service object.

        Returns:
            An authorized Analytics Reporting API V4 service object.
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.KEY_FILE_LOCATION, self.SCOPES)

        # Build the service object.
        analytics = build('analyticsreporting', 'v4', credentials=credentials, cache_discovery=False)

        return analytics


    def get_report(self, analytics, start = '2daysAgo', end = '2daysAgo'):
        """Queries the Analytics Reporting API V4.

        Args:
            analytics: An authorized Analytics Reporting API V4 service object.
        Returns:
            The Analytics Reporting API V4 response.
        """
        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                {
                'viewId': self.VIEW_ID,
                'dateRanges': [{'startDate': start, 'endDate': end}],
                'metrics': [{'expression': 'ga:totalEvents'}],
                'dimensions': [{'name': 'ga:eventCategory'}, {'name': 'ga:eventAction'}]
                }]
            }
        ).execute()


    def print_response(self, response):
        """Parses and prints the Analytics Reporting API V4 response.

        Args:
            response: An Analytics Reporting API V4 response.
        """
        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                dateRangeValues = row.get('metrics', [])

                for header, dimension in zip(dimensionHeaders, dimensions):
                    print header + ': ' + dimension

                for i, values in enumerate(dateRangeValues):
                    print 'Date range: ' + str(i)
                    for metricHeader, value in zip(metricHeaders, values.get('values')):
                        print metricHeader.get('name') + ': ' + value

    def parse_result(self, response = None):
        if response is None:
            return []
        
        try:
            report = response.get('reports', [])[0]
            results = []
            
            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions')
                clicks = row.get('metrics')[0].get('values', [])[0]
                results.append({
                    'category': dimensions[0],
                    'affiliate': urllib.unquote(dimensions[1]).decode('utf8'),
                    'clicks': int(clicks)
                })
            
            print(results)
            return results
        except:
            print("An error occured.")
            return []

    def save(self, reports):
        # try:
        app = scheduler.app
        with app.app_context():
            for report in reports:
                aff = self.affiliates_map.get(report.get('affiliate'))
                if aff is None:
                    continue

                created_at = self.get_delta_date()
                affiliate = Affiliate.query.filter_by(name = aff).first()
                if affiliate is None:
                    self.log_error("Affiliate `{0}` Not found at {1}.".format(aff, created_at))
                    continue

                history = History.query.filter_by(affiliate_id = affiliate.id, created_at = created_at).first()
                if history is None:
                    self.log_error("History for affiliate `{0}` Not found at {1}.".format(aff, created_at))
                    continue

                history.ga_click = report['clicks']
                db.session.commit()

    def run(self):
        analytics = self.initialize_analyticsreporting()
        response = self.get_report(analytics)
        reports = self.parse_result(response)
        if self.save(reports):
            return result
        else:
            return []

if __name__ == "__main__":
    me = GoogleAnalyticsReport()
    print(me.run())
