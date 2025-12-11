import pytest
from battery import Battery
from unittest.mock import Mock


@pytest.fixture
def charged_battery():
    return Battery(100)


@pytest.fixture
def partially_charged_battery():
    b = Battery(100)
    b.mCharge = 70
    return b


def describe_battery():

    def it_calls_monitor_on_recharge(partially_charged_battery):
        # setup
        mock_monitor = Mock()
        battery = partially_charged_battery  # use the fixture
        battery.external_monitor = mock_monitor

        # execute
        battery.recharge(20)   # battery starts at 70, add 20

        # validate
        mock_monitor.notify_recharge.assert_called_once_with(90)

    # put more test cases here.
    def it_calls_monitor_on_drain(charged_battery):
        mock_monitor = Mock()
        battery = charged_battery
        battery.external_monitor = mock_monitor

        battery.drain(20)

        mock_monitor.notify_drain.assert_called_once_with(80)

    def recharge_works_as_intended(partially_charged_battery):
        old_charge = partially_charged_battery.getCharge()
        partially_charged_battery.recharge(10)
        new_charge = partially_charged_battery.getCharge()
        assert new_charge == old_charge + 10

    def drain_works_as_intended(charged_battery):
        old_charge = charged_battery.getCharge()
        charged_battery.drain(10)
        new_charge = charged_battery.getCharge()
        assert new_charge == old_charge - 10

    def recharge_doesnt_go_over_cap(charged_battery):
        old_charge = charged_battery.getCharge()
        charged_battery.recharge(10000)
        new_charge = charged_battery.getCharge()
        assert new_charge == old_charge

    def drain_doesnt_go_under_zero(charged_battery):
        charged_battery.drain(10000)
        new_charge = charged_battery.getCharge()
        assert new_charge == 0

    def recharge_doesnt_work_with_negatives(partially_charged_battery):
        old_charge = partially_charged_battery.getCharge()
        partially_charged_battery.recharge(-10)
        new_charge = partially_charged_battery.getCharge()
        assert new_charge == old_charge

    def drain_doesnt_work_with_negatives(partially_charged_battery):
        old_charge = partially_charged_battery.getCharge()
        partially_charged_battery.drain(-10)
        new_charge = partially_charged_battery.getCharge()
        assert new_charge == old_charge
