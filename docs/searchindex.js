Search.setIndex({docnames:["atomic_p2p","atomic_p2p.peer","atomic_p2p.peer.communication","atomic_p2p.peer.entity","atomic_p2p.peer.monitor","atomic_p2p.utils","atomic_p2p.utils.communication","atomic_p2p.utils.logging","atomic_p2p.utils.mixin","index","modules"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,sphinx:56},filenames:["atomic_p2p.rst","atomic_p2p.peer.rst","atomic_p2p.peer.communication.rst","atomic_p2p.peer.entity.rst","atomic_p2p.peer.monitor.rst","atomic_p2p.utils.rst","atomic_p2p.utils.communication.rst","atomic_p2p.utils.logging.rst","atomic_p2p.utils.mixin.rst","index.rst","modules.rst"],objects:{"":{atomic_p2p:[0,0,0,"-"]},"atomic_p2p.AtomicP2P":{__init__:[0,2,1,""],start:[0,2,1,""],stop:[0,2,1,""]},"atomic_p2p.local_monitor":{LocalMonitor:[0,1,1,""]},"atomic_p2p.local_monitor.LocalMonitor":{command_recv:[0,2,1,""],decrypt:[0,2,1,""],encrypt:[0,2,1,""],registerCommand:[0,2,1,""],registerHandler:[0,2,1,""],run:[0,2,1,""],stop:[0,2,1,""]},"atomic_p2p.peer":{Peer:[1,1,1,""],ProcessPeer:[1,1,1,""],ThreadPeer:[1,1,1,""],command:[1,0,0,"-"],communication:[2,0,0,"-"],dns_resolver:[1,0,0,"-"],entity:[3,0,0,"-"],monitor:[4,0,0,"-"],peer:[1,0,0,"-"],process_peer:[1,0,0,"-"],thread_peer:[1,0,0,"-"]},"atomic_p2p.peer.Peer":{__init__:[1,2,1,""],add_peer_in_net:[1,2,1,""],connectlist:[1,3,1,""],del_peer_in_net:[1,2,1,""],get_peer_info_by_host:[1,2,1,""],handler_broadcast_packet:[1,2,1,""],handler_unicast_packet:[1,2,1,""],is_peer_in_net:[1,2,1,""],join_net:[1,2,1,""],join_net_by_DNS:[1,2,1,""],loop:[1,2,1,""],loop_start:[1,2,1,""],loop_stop:[1,2,1,""],new_tcp_long_conn:[1,2,1,""],peer_pool:[1,3,1,""],pend_packet:[1,2,1,""],pend_socket:[1,2,1,""],pend_socket_to_rm:[1,2,1,""],pkt_handlers:[1,3,1,""],program_hash:[1,3,1,""],send_queue:[1,3,1,""],server_info:[1,3,1,""],tcp_server:[1,3,1,""]},"atomic_p2p.peer.ProcessPeer":{is_start:[1,2,1,""],run:[1,2,1,""],start:[1,2,1,""],stop:[1,2,1,""]},"atomic_p2p.peer.ThreadPeer":{is_start:[1,2,1,""],run:[1,2,1,""],start:[1,2,1,""],stop:[1,2,1,""]},"atomic_p2p.peer.command":{HelpCmd:[1,1,1,""],JoinCmd:[1,1,1,""],LeaveNetCmd:[1,1,1,""],ListCmd:[1,1,1,""],SendCmd:[1,1,1,""]},"atomic_p2p.peer.communication":{msg:[2,0,0,"-"],net:[2,0,0,"-"]},"atomic_p2p.peer.communication.msg":{MessageHandler:[2,1,1,""]},"atomic_p2p.peer.communication.msg.MessageHandler":{on_recv_pkt:[2,2,1,""],on_send_pkt:[2,2,1,""],pkt_type:[2,3,1,""]},"atomic_p2p.peer.communication.net":{AckNewMemberHandler:[2,1,1,""],CheckJoinHandler:[2,1,1,""],DisconnectHandler:[2,1,1,""],JoinHandler:[2,1,1,""],NewMemberHandler:[2,1,1,""]},"atomic_p2p.peer.communication.net.AckNewMemberHandler":{on_recv_pkt:[2,2,1,""],on_send_pkt:[2,2,1,""],pkt_type:[2,3,1,""]},"atomic_p2p.peer.communication.net.CheckJoinHandler":{on_recv_pkt:[2,2,1,""],on_send_pkt:[2,2,1,""],pkt_type:[2,3,1,""]},"atomic_p2p.peer.communication.net.DisconnectHandler":{on_recv_pkt:[2,2,1,""],on_send_pkt:[2,2,1,""],pkt_type:[2,3,1,""]},"atomic_p2p.peer.communication.net.JoinHandler":{on_recv_pkt:[2,2,1,""],on_send_pkt:[2,2,1,""],pkt_type:[2,3,1,""]},"atomic_p2p.peer.communication.net.NewMemberHandler":{on_recv_pkt:[2,2,1,""],on_send_pkt:[2,2,1,""],pkt_type:[2,3,1,""]},"atomic_p2p.peer.dns_resolver":{DNSResolver:[1,1,1,""]},"atomic_p2p.peer.dns_resolver.DNSResolver":{__init__:[1,2,1,""],change_ns:[1,2,1,""],forward:[1,2,1,""],reverse:[1,2,1,""],srv:[1,2,1,""],sync_from_DNS:[1,2,1,""]},"atomic_p2p.peer.entity":{peer_info:[3,0,0,"-"],peer_status:[3,0,0,"-"]},"atomic_p2p.peer.entity.peer_info":{PeerInfo:[3,1,1,""]},"atomic_p2p.peer.entity.peer_status":{PeerStatus:[3,1,1,""],StatusType:[3,1,1,""]},"atomic_p2p.peer.entity.peer_status.PeerStatus":{__init__:[3,2,1,""],last_update_ts:[3,3,1,""],no_response_count:[3,3,1,""],status:[3,3,1,""],toDict:[3,2,1,""],update:[3,2,1,""]},"atomic_p2p.peer.entity.peer_status.StatusType":{NO_RESP:[3,3,1,""],PENDING:[3,3,1,""],UNKNOWN:[3,3,1,""],UPDATED:[3,3,1,""]},"atomic_p2p.peer.monitor":{Monitor:[4,1,1,""],command:[4,0,0,"-"],communication:[4,0,0,"-"]},"atomic_p2p.peer.monitor.Monitor":{is_start:[4,2,1,""],on_recv_pkt:[4,2,1,""],removeMonitorlist:[4,2,1,""],run:[4,2,1,""],start:[4,2,1,""],stop:[4,2,1,""]},"atomic_p2p.peer.monitor.command":{HelpCmd:[4,1,1,""],ListCmd:[4,1,1,""],ManualCmd:[4,1,1,""],PauseCmd:[4,1,1,""],PeriodCmd:[4,1,1,""],ResetCmd:[4,1,1,""],VerboseCmd:[4,1,1,""]},"atomic_p2p.peer.monitor.communication":{CheckHandler:[4,1,1,""]},"atomic_p2p.peer.monitor.communication.CheckHandler":{on_recv_pkt:[4,2,1,""],on_recv_reject_pkt:[4,2,1,""],on_send_pkt:[4,2,1,""],pkt_type:[4,3,1,""]},"atomic_p2p.peer.peer":{Peer:[1,1,1,""]},"atomic_p2p.peer.peer.Peer":{__init__:[1,2,1,""],add_peer_in_net:[1,2,1,""],connectlist:[1,3,1,""],del_peer_in_net:[1,2,1,""],get_peer_info_by_host:[1,2,1,""],handler_broadcast_packet:[1,2,1,""],handler_unicast_packet:[1,2,1,""],is_peer_in_net:[1,2,1,""],join_net:[1,2,1,""],join_net_by_DNS:[1,2,1,""],loop:[1,2,1,""],loop_start:[1,2,1,""],loop_stop:[1,2,1,""],new_tcp_long_conn:[1,2,1,""],peer_pool:[1,3,1,""],pend_packet:[1,2,1,""],pend_socket:[1,2,1,""],pend_socket_to_rm:[1,2,1,""],pkt_handlers:[1,3,1,""],program_hash:[1,3,1,""],send_queue:[1,3,1,""],server_info:[1,3,1,""],tcp_server:[1,3,1,""]},"atomic_p2p.peer.process_peer":{ProcessPeer:[1,1,1,""]},"atomic_p2p.peer.process_peer.ProcessPeer":{is_start:[1,2,1,""],run:[1,2,1,""],start:[1,2,1,""],stop:[1,2,1,""]},"atomic_p2p.peer.thread_peer":{ThreadPeer:[1,1,1,""]},"atomic_p2p.peer.thread_peer.ThreadPeer":{is_start:[1,2,1,""],run:[1,2,1,""],start:[1,2,1,""],stop:[1,2,1,""]},"atomic_p2p.utils":{command:[5,0,0,"-"],communication:[6,0,0,"-"],host_valid:[5,4,1,""],logging:[7,0,0,"-"],manager:[5,0,0,"-"],mixin:[8,0,0,"-"],security:[5,0,0,"-"]},"atomic_p2p.utils.command":{Command:[5,1,1,""]},"atomic_p2p.utils.command.Command":{__init__:[5,2,1,""],_execute:[5,2,1,""],_on_command_recv:[5,2,1,""]},"atomic_p2p.utils.communication":{handler:[6,0,0,"-"],is_ssl_socket_open:[6,4,1,""],packet:[6,0,0,"-"],valid_ipv4_format:[6,4,1,""],valid_ipv6_format:[6,4,1,""]},"atomic_p2p.utils.communication.handler":{Handler:[6,1,1,""]},"atomic_p2p.utils.communication.handler.Handler":{__init__:[6,2,1,""],on_recv:[6,2,1,""],on_recv_pkt:[6,2,1,""],on_recv_reject_pkt:[6,2,1,""],on_send:[6,2,1,""],on_send_pkt:[6,2,1,""],on_send_reject_pkt:[6,2,1,""],peer:[6,3,1,""],pkt_type:[6,3,1,""]},"atomic_p2p.utils.communication.packet":{Packet:[6,1,1,""]},"atomic_p2p.utils.communication.packet.Packet":{"export":[6,3,1,""],__init__:[6,2,1,""],clone:[6,2,1,""],data:[6,3,1,""],deserilize:[6,5,1,""],dst:[6,3,1,""],is_reject:[6,2,1,""],program_hash:[6,3,1,""],redirect_to_host:[6,2,1,""],serilize:[6,5,1,""],set_reject:[6,2,1,""],src:[6,3,1,""],to_dict:[6,2,1,""]},"atomic_p2p.utils.logging":{formatters:[7,0,0,"-"],getLogger:[7,4,1,""],handlers:[7,0,0,"-"]},"atomic_p2p.utils.logging.formatters":{StdoutFormatter:[7,1,1,""]},"atomic_p2p.utils.logging.formatters.StdoutFormatter":{format:[7,2,1,""]},"atomic_p2p.utils.logging.handlers":{SocketHandler:[7,1,1,""],StreamHandler:[7,1,1,""]},"atomic_p2p.utils.logging.handlers.SocketHandler":{emit:[7,2,1,""],encrypt:[7,2,1,""]},"atomic_p2p.utils.manager":{ProcManager:[5,1,1,""],ThreadManager:[5,1,1,""]},"atomic_p2p.utils.manager.ProcManager":{is_start:[5,2,1,""],run:[5,2,1,""],start:[5,2,1,""],stop:[5,2,1,""]},"atomic_p2p.utils.manager.ThreadManager":{is_start:[5,2,1,""],run:[5,2,1,""],start:[5,2,1,""],stop:[5,2,1,""]},"atomic_p2p.utils.mixin":{CommandableMixin:[8,1,1,""],HandleableMixin:[8,1,1,""],commandable:[8,0,0,"-"],handleable:[8,0,0,"-"]},"atomic_p2p.utils.mixin.CommandableMixin":{commands:[8,3,1,""],onProcess:[8,2,1,""],register_command:[8,2,1,""],unregister_command:[8,2,1,""]},"atomic_p2p.utils.mixin.HandleableMixin":{pkt_handlers:[8,3,1,""],register_handler:[8,2,1,""],select_handler:[8,2,1,""],unregister_handler:[8,2,1,""]},"atomic_p2p.utils.mixin.commandable":{CommandableMixin:[8,1,1,""]},"atomic_p2p.utils.mixin.commandable.CommandableMixin":{commands:[8,3,1,""],onProcess:[8,2,1,""],register_command:[8,2,1,""],unregister_command:[8,2,1,""]},"atomic_p2p.utils.mixin.handleable":{HandleableMixin:[8,1,1,""]},"atomic_p2p.utils.mixin.handleable.HandleableMixin":{pkt_handlers:[8,3,1,""],register_handler:[8,2,1,""],select_handler:[8,2,1,""],unregister_handler:[8,2,1,""]},"atomic_p2p.utils.security":{create_self_signed_cert:[5,4,1,""],self_hash:[5,4,1,""]},atomic_p2p:{AtomicP2P:[0,1,1,""],local_monitor:[0,0,0,"-"],peer:[1,0,0,"-"],utils:[5,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","function","Python function"],"5":["py","staticmethod","Python static method"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:function","5":"py:staticmethod"},terms:{"byte":6,"case":8,"class":[0,1,2,3,4,5,6,7,8],"default":[1,3],"enum":3,"export":[1,6],"float":3,"function":1,"import":1,"int":[1,3,6],"new":[2,5],"return":[0,1,3,4,5,6,7,8],"static":6,"true":[1,8],"while":1,And:1,DNS:1,The:[0,1,4,5,6,7,8],__init__:[0,1,3,5,6],_data:6,_execut:5,_forwardref:[],_on_command_recv:5,_type:6,abil:[1,8],about:6,accept:6,ack:2,acknewmemberhandl:2,activ:[0,1,4,5],actual:[5,6,7],add:1,add_monitor_pass:7,add_peer_in_net:1,addit:1,addr:[0,4],address:[1,6],addtion:1,adjust:4,after:1,all:[1,3,4,6],also:8,ani:[0,1,4,5],annot:5,anyoth:1,anyth:8,append:[1,7],arg:[0,1,4,5],argument:[0,1,4,5],arrai:5,arrang:[1,4,5],assertionerror:1,atomicp2p:0,attribut:7,auto_regist:1,avai:1,avaiabl:1,base:[0,1,2,3,4,5,6,7,8],been:[1,5,6,8],befor:7,bind:1,block:1,bool:[1,4,5,6,8],broadcast:1,call:[1,4,5,7],callabl:[0,1,4,5],can:[1,5],carri:7,caus:[1,5],cert:[0,1,5],cert_dir:5,cert_fil:5,cess:1,chang:1,change_n:1,check:[3,4],checkhandl:4,checkjoin:2,checkjoinhandl:2,child:[1,5],circular:8,clear:1,clone:6,close:1,cmd:[1,4,5,8],code:1,command:[0,10],command_recv:0,commandablemixin:[1,4,8],commun:[0,1,5,8],comput:7,conn:[2,3,4,6],connec:1,connect:1,connectlist:1,constructor:[0,1,4,5],contain:[6,8],content:10,context:[1,5],control:[1,4,5],convert:6,count:3,coupl:7,creat:[1,5],create_self_signed_cert:5,crt:5,current:[1,3,8],current_host:1,data:[0,6],datacard:5,debug:[0,1,4,5],decrypt:0,defin:5,del_peer_in_net:1,delai:4,delet:1,deliv:3,descriptor:1,deseril:6,destin:1,detail:[3,4],determin:[6,7],dict:[1,3,6,8],dictionari:7,directli:0,directori:5,disconnect:2,disconnecthandl:2,dns_resolv:[0,10],dnsresolv:1,domain:1,don:5,dst:[1,6],dur:1,dure:3,each:[1,5,8],emit:7,empti:1,enc_data:0,encrypt:[0,7],entiti:[0,1],enumer:3,error:1,etc:3,event:7,everi:[1,4,6],except:[0,1,5,7],exist:[1,5,8],extens:0,fail:8,fals:[1,4,6,8],fetch:1,fianl:1,file:[0,1],first:1,flag:4,forc:8,format:[0,6,7],formatexcept:7,formatt:[0,5],formattim:7,forward:1,found:8,four:1,fqdn:1,from:[0,1,4,5,6],further:1,get:[1,8],get_peer_info_by_host:1,getlogg:[1,7],getmessag:7,give:1,given:[1,8],global:1,handl:[1,3,8],handleabl:[0,1,4,5],handleablemixin:[1,4,8],handler:[0,1,2,4,5,8],handler_broadcast_packet:1,handler_unicast_packet:1,hard:1,hash:[1,6],have:1,help:[1,4],helpcmd:[1,4],hide:6,host:[1,3,5,6],host_valid:5,how:[5,6],ident:1,implement:[5,7],includ:[3,6],index:9,info:1,inform:[6,7],inherit:8,init:[0,1,3,5,6],inner:6,instanc:[1,8],intend:7,interact:[6,8],invok:[0,1,4,5],is_peer_in_net:1,is_reject:6,is_ssl_socket_open:6,is_start:[1,4,5],iter:[1,8],its:[1,6],join:[1,2],join_net:1,join_net_by_dn:1,joincmd:1,joinhandl:2,keep:[1,4],kei:[0,5,6,8],key_fil:5,keypair:5,keyword:[0,1,4,5],known:1,kwarg:[0,1,4,5,6,8],labl:1,last:3,last_update_t:3,leav:1,leavenet:1,leavenetcmd:1,level:7,like:0,link:1,list:[1,4,5],listcmd:[1,4],listen:0,local_monitor:10,localmonitor:0,log:[0,1,5],logger:[0,1,4,5],logrecord:7,loop:1,loop_delai:[1,4],loop_start:1,loop_stop:1,loopdelai:[1,5],made:6,mai:[0,1,4,5],maintain:[1,6],maintain_data:6,maintain_secret:6,make:1,manag:[0,10],manuadl:4,manual:4,manualcmd:4,match:8,max_no_response_count:4,mean:[6,8],member:2,memeb:2,messag:[1,2,7],messagehandl:2,method:[0,1,4,5],miss:4,mixin:[0,1,4,5],modul:[9,10],monitor:[0,1,3],more:[1,4,5],most:[1,4,5],msg:[0,1],msg_arr:[5,8],multipl:1,multiprocess:[1,5],must:[1,4,5],myapp:5,name:[0,1,3,7,8],nameserv:1,namserv:1,need:[1,6,8],net:[0,1],new_tcp_long_conn:1,newmemberhandl:2,next:1,no_resp:3,no_response_count:3,non:1,none:[0,1,3,4,5,6,7,8],notimplementederror:7,ns1:1,ns2:1,ns3:1,obj:6,object:[0,1,3,4,5,6,8],occur:1,occurr:1,on_recv:6,on_recv_pkt:[2,4,6],on_recv_reject_pkt:[4,6],on_send:6,on_send_pkt:[2,4,6],on_send_reject_pkt:6,onc:[1,4,5],one:1,onli:1,onprocess:8,oper:7,operand:7,option:1,out:7,output:4,overrid:[0,1,4,5,8],overridden:[1,5],packag:10,packet:[0,1,3,5,8],page:9,param:0,paramet:[1,3,5,6,8],parent:8,pars:[1,6],pass:[0,1,4,5,8],password:[0,7],path:[0,1,5],paus:4,pausecmd:4,payload:6,peer:[0,6,8,10],peer_info:[0,1,2],peer_pool:1,peer_statu:[0,1],peerinfo:[1,3],peermanag:1,peerstatu:3,pem:0,pend:[1,3],pend_packet:1,pend_socket:1,pend_socket_to_rm:1,per:[1,4,5],period:[1,4],periodcmd:4,pkt:[1,2,4,6],pkt_handler:[1,8],pkt_type:[1,2,4,6,8],point:[0,1],pool:1,port:[0,1,4],posit:1,positon:1,precheck:5,preparatori:7,prevent:8,print:5,prioriti:1,pro:1,proce:6,process:[1,5],process_p:[0,10],processp:1,procmanag:5,program:1,program_hash:[1,6],prompt:[1,4],proper:1,ptr:1,put:1,queri:1,queue:1,rais:[1,4,5,7],raw_data:[0,1,6,7],readi:1,reciev:[1,6],reciv:1,record:[1,7],recv:6,redirect_to_host:6,regist:8,register_command:8,register_handl:8,registercommand:0,registerhandl:0,reject:6,reject_data:6,remov:[1,8],removemonitorlist:4,repres:[0,1,4,5,6],request:1,reset:4,resetcmd:4,resolv:1,respect:[0,1,4,5],respons:[1,3,6],result:[1,5],revers:1,riabl:8,role:[0,1,3],run:[0,1,4,5],runtimeerror:[1,4,5],safer:1,same:[0,1,4,5],search:9,sec:1,second:[1,4],secur:[0,6,10],select:8,select_handl:8,self:[1,5],self_hash:5,send:[1,4,6],send_queu:1,sendcmd:1,sender:6,separ:[1,4,5],sepecif:1,sequenti:[0,1,4,5],seril:6,server:[0,1],server_info:1,servic:[0,1],set:8,set_reject:6,should:[0,1,8],show:[1,4],sign:5,sinc:3,singl:1,skip:1,sock:[1,6],socket:1,sockethandl:7,sourc:6,specif:[1,4],specifi:[1,7],split:5,src:[2,4,6],srv:1,srv_fqdn:1,ssing:6,ssl:1,sslsocket:[1,6],standard:[0,1,4,5],start:[0,1,4,5],statu:[3,4],status_typ:3,statustyp:3,stdoutformatt:7,step:7,stop:[0,1,4,5],str:[0,1,5,6,8],stream:7,streamhandl:7,string:[6,7],stroe:8,sub:[0,1,5],subclass:[0,1,4,5,7],submodul:10,subpackag:10,success:[1,8],sync_from_dn:1,take:7,taken:[0,1,4,5],target:[0,1,2,4,5,6,8],tcp:1,tcp_server:1,teract:3,termin:1,text:7,than:[1,4,5],them:5,thi:[0,1,3,4,5,6,7,8],thread:[0,1,4,5],thread_peer:[0,10],threadmanag:[0,5],threadpeer:1,through:8,time:[3,7],timestamp:3,tion:1,to_dict:6,todict:3,toggl:4,trigger:5,tupl:[1,5,6],type:[0,1,3,4,5,6,8],unicast:1,union:[1,8],uniqu:[1,5,6],unknown:3,unregist:8,unregister_command:8,unregister_handl:8,updat:[1,3],usag:[1,4],use:1,used:[1,7],uses:7,usestim:7,using:7,utf:6,util:[0,1,2,4,10],valid:1,valid_ipv4_format:6,valid_ipv6_format:6,valueerror:1,variabl:[1,8],varialb:1,verbos:4,verbosecmd:4,version:7,want:1,weather:[],weight:1,what:6,whatev:7,when:[1,3,5,6],where:6,whether:8,which:[1,6,7,8],who:6,whole:1,whould:1,work:5,would:1,wrap:[1,6],wrape:1,write:5,yet:1,yield:7,you:[0,1,4,5]},titles:["atomic_p2p package","atomic_p2p.peer package","atomic_p2p.peer.communication package","atomic_p2p.peer.entity package","atomic_p2p.peer.monitor package","atomic_p2p.utils package","atomic_p2p.utils.communication package","atomic_p2p.utils.logging package","atomic_p2p.utils.mixin package","Welcome to AtomicP2P\u2019s documentation!","atomic_p2p"],titleterms:{atomic_p2p:[0,1,2,3,4,5,6,7,8,10],atomicp2p:9,command:[1,4,5,8],commun:[2,4,6],content:[0,1,2,3,4,5,6,7,8],dns_resolv:1,document:9,entiti:3,formatt:7,handleabl:8,handler:[6,7],indic:9,local_monitor:0,log:7,manag:5,mixin:8,modul:[0,1,2,3,4,5,6,7,8],monitor:4,msg:2,net:2,packag:[0,1,2,3,4,5,6,7,8],packet:6,peer:[1,2,3,4],peer_info:3,peer_statu:3,process_p:1,secur:5,submodul:[0,1,2,3,4,5,6,7,8],subpackag:[0,1,5],tabl:9,thread_peer:1,util:[5,6,7,8],welcom:9}})