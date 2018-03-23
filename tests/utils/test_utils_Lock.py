from utils.Lock import Lock

class TestLock:

    def test_init(self):
        l = Lock()
        assert l.lock == False
        assert l.locker == None

        l.setLock('Locker')
        assert l.lock == True
        assert l.locker == 'Locker'

        l.unLock()
        assert l.lock == False
        assert l.locker == None

        assert l.isLock() == False
        
        assert l.getLocker() == None
