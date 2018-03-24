from schedule.Schedule import Schedule, NextSchedule

class TestSchedule:

    def test_init(self):
        pass
        #with pytest.raises(KeyError):
        #    s = Schedule({})
        #j = { 'target': None, 'startTime': None, 'peroid': None, 'preCommand': None, 'command': None, 'nextSchedule': None }
        #s = Schedule()

class TestNextSchedule:

    def test_init(self):
        j = { 'command': None, 'delay': 1, 'nextSchedule': None }
        s = NextSchedule(j)
        assert s.command == None
        assert s.delay == 1
        assert s.nextSchedule == None

    def run(self):
        pass
