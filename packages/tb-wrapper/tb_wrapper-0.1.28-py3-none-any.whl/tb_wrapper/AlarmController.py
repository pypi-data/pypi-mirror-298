from tb_wrapper.handle_exception import *
from tb_wrapper.MainController import *


@handle_tb_wrapper_exception
class AlarmController(MainController):

    def __init__(self, tb_url=None, userfile=None, passwordfile=None, connection=None):
        super().__init__(tb_url, userfile, passwordfile, connection)

    def build_alarm(self, tenant_obj_id, alarm_name, alarm_type, entity_originator, customer_obj_id, severity_alarm, alarm_status, ack, clear, details=None):

        if details is None:
            alarm = Alarm(tenant_id=tenant_obj_id,
                          name=alarm_name,
                          type=alarm_type,
                          originator=entity_originator,
                          customer_id=customer_obj_id,
                          severity=severity_alarm,
                          status=alarm_status,
                          acknowledged=ack,
                          cleared=clear)
        else:
            alarm = Alarm(tenant_id=tenant_obj_id,
                          name=alarm_name,
                          type=alarm_type,
                          originator=entity_originator,
                          customer_id=customer_obj_id,
                          severity=severity_alarm,
                          status=alarm_status,
                          acknowledged=ack,
                          cleared=clear,
                          details=details)
        return alarm

    def save_alarm(self, alarm):
        return self.tb_client.save_alarm(alarm)
