import logging
import sys
import unittest

from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldType

from data_type_models import SampleModel
from sapiopylib.rest.pojo.CustomReport import CustomReportCriteria, ReportColumn

from sapiopylib.rest.DataMgmtService import DataMgmtServer

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.utils.autopaging import CustomReportAutoPager

user = SapioUser(url="https://linux-vm:8443/webservice/api", verify_ssl_cert=False,
                 guid="66c2bea5-7cb2-4bfc-a413-304a3f4c3f33",
                 username="yqiao_api", password="Password1!")
report_man = DataMgmtServer.get_custom_report_manager(user)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.getLogger().setLevel(logging.DEBUG)

class FR52729Test(unittest.TestCase):

    def test_multi_page_report_auto_paging(self):
        column_list = [ReportColumn(SampleModel.DATA_TYPE_NAME, SampleModel.SAMPLEID__FIELD_NAME.field_name, FieldType.STRING),
                       ReportColumn(SampleModel.DATA_TYPE_NAME, SampleModel.OTHERSAMPLEID__FIELD_NAME.field_name, FieldType.STRING),
                       ReportColumn(SampleModel.DATA_TYPE_NAME, SampleModel.CONTAINERTYPE__FIELD_NAME.field_name, FieldType.STRING)]
        report_criteria = CustomReportCriteria(column_list)
        report_criteria.page_size = 500

        original_report = report_man.run_custom_report(report_criteria)
        original_result = original_report.result_table

        report_criteria.page_size = 10
        report_criteria.page_number = 0
        auto_pager = CustomReportAutoPager(user, report_criteria)
        auto_pager.max_page = 50
        auto_pager_result = auto_pager.get_all_at_once()
        self.assertTrue(original_result == auto_pager_result)
