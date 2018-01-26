from pexpect.pxssh import pxssh
from pexpect import spawn,TIMEOUT,EOF

from OExceptionPexpect import OExceptionPexpect

class OPxssh(pxssh):
    def __init__(self):
        super().__init__(timeout=10, maxread=2000, searchwindowsize=None,logfile=None, cwd=None, env=None, ignore_sighup=True, echo=True,options={}, encoding=None, codec_errors='strict')
    def login (self, server, username, password='', terminal_type='ansi',
                original_prompt=r"[a-zA-Z]" , login_timeout=10, port=None,
                auto_prompt_reset=False, ssh_key=None, quiet=True,
                sync_multiplier=1, check_local_ip=True,parameter=None):

        ssh_options = ''.join([" -o '%s=%s'" % (o, v) for (o, v) in self.options.items()])
        if quiet:
            ssh_options = ssh_options + ' -q'
        if not check_local_ip:
            ssh_options = ssh_options + " -o'NoHostAuthenticationForLocalhost=yes'"
        if self.force_password:
            ssh_options = ssh_options + ' ' + self.SSH_OPTS
        if port is not None:
            ssh_options = ssh_options + ' -p %s'%(str(port))
        if ssh_key is not None:
            try:
                os.path.isfile(ssh_key)
            except:
                raise OExceptionPexpect('private ssh key does not exist')
            ssh_options = ssh_options + ' -i %s' % (ssh_key)
        cmd = "ssh %s -l %s %s %s" % (ssh_options, username, server,parameter)

        # This does not distinguish between a remote server 'password' prompt
        # and a local ssh 'passphrase' prompt (for unlocking a private key).
        spawn._spawn(self, cmd)
        i = self.expect(["(?i)are you sure you want to continue connecting","(?i)(?:password:)|(?:passphrase for key)",original_prompt, "(?i)permission denied", "(?i)terminal type", TIMEOUT, "(?i)connection closed by remote host", EOF], timeout=login_timeout)
        print(i,original_prompt)

        # First phase
        if i==0:
            # New certificate -- always accept it.
            # This is what you get if SSH does not have the remote host's
            # public key stored in the 'known_hosts' cache.
            self.sendline("yes")
            i = self.expect(["(?i)are you sure you want to continue connecting","(?i)(?:password:)|(?:passphrase for key)",  original_prompt,"(?i)permission denied", "(?i)terminal type", TIMEOUT])
        if i==1: # password or passphrase
            self.sendline(password)
            i = self.expect(["(?i)are you sure you want to continue connecting","(?i)(?:password:)|(?:passphrase for key)", original_prompt,  "(?i)permission denied", "(?i)terminal type", TIMEOUT])
            print(i,original_prompt)
        if i==4:
            self.sendline(terminal_type)
            i = self.expect(["(?i)are you sure you want to continue connecting","(?i)(?:password:)|(?:passphrase for key)", original_prompt,  "(?i)permission denied", "(?i)terminal type", TIMEOUT])
        if i==7:
            self.close()
            raise OExceptionPexpect('Could not establish connection to host')

        # Second phase
        if i==0:
            # This is weird. This should not happen twice in a row.
            self.close()
            raise OExceptionPexpect('Weird error. Got "are you sure" prompt twice.')
        elif i==2: # can occur if you have a public key pair set to authenticate.
            ### TODO: May NOT be OK if expect() got tricked and matched a false prompt.
            pass
        elif i==1: # password prompt again
            # For incorrect passwords, some ssh servers will
            # ask for the password again, others return 'denied' right away.
            # If we get the password prompt again then this means
            # we didn't get the password right the first time.
            self.close()
            raise OExceptionPexpect('password refused')
        elif i==3: # permission denied -- password was bad.
            self.close()
            raise OExceptionPexpect('permission denied')
        elif i==4: # terminal type again? WTF?
            self.close()
            raise OExceptionPexpect('Weird error. Got "terminal type" prompt twice.')
        elif i==5: # Timeout
            #This is tricky... I presume that we are at the command-line prompt.
            #It may be that the shell prompt was so weird that we couldn't match
            #it. Or it may be that we couldn't log in for some other reason. I
            #can't be sure, but it's safe to guess that we did login because if
            #I presume wrong and we are not logged in then this should be caught
            #later when I try to set the shell prompt.
            pass
        elif i==6: # Connection closed by remote host
            self.close()
            raise OExceptionPexpect('connection closed')
        else: # Unexpected
            self.close()
            raise OExceptionPexpect('unexpected login response')
        if not self.sync_original_prompt(sync_multiplier):
            self.close()
            raise OExceptionPexpect('could not synchronize with original prompt')
        # We appear to be in.
        # set shell prompt to something unique.
        if auto_prompt_reset:
            if not self.set_unique_prompt():
                self.close()
                raise OExceptionPexpect('could not set shell prompt '
                                     '(received: %r, expected: %r).' % (
                                         self.before, self.PROMPT,))
        return True
    def prompt(self,regular=r'[]',timeout=-1):
        if timeout == -1:
            timeout = self.timeout
        i = self.expect([regular, TIMEOUT], timeout=timeout)
        if i==1:
            return False
        return True

