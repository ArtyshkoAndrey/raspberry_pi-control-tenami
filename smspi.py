import gammu
import time

# Outbox - 4
# Inbox - 3
# Outbox -2
# Inbox - 1

class Sms():
    def __init__(self):
        self.SmsLength = 0
        self.sm = gammu.StateMachine()
        self.sm.ReadConfig()
        self.sm.Init()
        self.number = "89029634366"
        self.cheker = False

    def GetFirstSms(self):
        # try:
        self.text = self.sm.GetAllSMS(0)
        self.cheker = False
        print(self.text)
        	# print(self.sm.GetSMSFolders())
        # except:
        # 	self.text = 'Сообщений нет'
        # 	self.cheker = True
        # 	print(self.text)


# sms = Sms()

# while True:
# 	sms.GetFirstSms()
# 	time.sleep(5)




while True:
    state_machine = gammu.StateMachine()
    state_machine.ReadConfig()
    state_machine.Init()

    status = state_machine.GetSMSStatus()

    remain = status['SIMUsed'] + status['PhoneUsed'] + status['TemplatesUsed']

    start = True

    try:
        while remain > 0:
            if start:
                sms = state_machine.GetNextSMS(Start=True, Folder=0)
                start = False
            else:
                sms = state_machine.GetNextSMS(
                    Location=sms[0]['Location'], Folder=0
                )
            remain = remain - len(sms)

            for m in sms:
                print()
                print('{0:<15}: {1}'.format('Number', m['Number']))
                print('{0:<15}: {1}'.format('Date', str(m['DateTime'])))
                print('{0:<15}: {1}'.format('State', m['State']))
                print('\n{0}'.format(m['Text']))
    except gammu.ERR_EMPTY:
        # This error is raised when we've reached last entry
        # It can happen when reported status does not match real counts
        print('Failed to read all messages!')

    print("----------")
    time.sleep(10)