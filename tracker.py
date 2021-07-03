from cowin_api import CoWinAPI
from _datetime import datetime
from playsound import playsound
import smtplib
import json
import time
import sys


class FindSlot:

    def __init__(self):
        try:
            self.cowin = CoWinAPI()
            print(self.cowin.get_states())
            print(type(self.cowin.get_states()))
            states = self.cowin.get_states()['states']
            print(type(states), states)

            self.mailServer = smtplib.SMTP("smtp.gmail.com", 587)
            self.mailServer.starttls()

        except Exception as error:
            print(error, 'in init')

    def get_state_district_details(self):
        try:
            stateDict = {}
            for i in self.cowin.get_states()['states']:
                for j in self.cowin.get_districts(i['state_id'])['districts']:
                    if str(i['state_name']) not in stateDict.keys():
                        stateDict[i['state_name']] = [j['district_name']]
                    else:
                        stateDict[i['state_name']] += [j['district_name']]
            return stateDict
        except Exception as e:
            print(e, 'in get_state_district_details')

    def getState(self, stateIp):
        try:
            stateIp = stateIp.replace(' ', '').lower()
            states = self.cowin.get_states()['states']

            for values in states:
                if stateIp in values['state_name'].replace(' ', '').lower():
                    state_id = values['state_id']
                    state_name = values['state_name']
                    break

            return state_id, state_name

        except Exception as e:
            state_id = "Wrong State Name {}".format(stateIp)
            print(e, 'in getstate')
            return state_id,

    def getDistrict(self, state_id, districtIp):
        try:

            districtIp = districtIp.replace(' ', '').lower()
            districts = self.cowin.get_districts(state_id)['districts']
            for values in districts:
                if districtIp in values['district_name'].replace(' ', '').lower():
                    district_id = values['district_id']
                    district_name = values['district_name']
                    break

            return district_id, district_name

        except Exception as e:
            district_id = "No districts found with {} in ".format(districtIp)
            print(e, 'in getdistrict')
            return district_id

    def getCentersByDistrict(self, state_id, district_id):
        try:
            available_centers = self.cowin.get_availability_by_district(str(district_id))['centers']
            slotAvailable = []
            for center in available_centers:
                for sessions in center['sessions']:
                    if sessions['available_capacity'] > 0:
                        slotAvailable.append(center)

            return slotAvailable

        except Exception as e:
            print(e, 'in getCentersByDistrict-0')

    def getSlotInfo(self, slotAvailable):
        try:
            detailDict = []
            # print(slotAvailable)
            for slotinfo in slotAvailable:
                name = slotinfo['name']
                address = slotinfo['address']
                pincode = slotinfo['pincode']
                fee_type = slotinfo['fee_type']
                for sessions in slotinfo['sessions']:
                    date = sessions['date']
                    # avlShot = sessions['available_capacity']
                    dose1 = sessions['available_capacity_dose1']
                    dose2 = sessions['available_capacity_dose2']
                    min_age = sessions['min_age_limit']
                    vaccineName = sessions['vaccine']
                    detailDict.append({"name": name, "address": address,
                                       "pincode": pincode, "date": date, "dose1": dose1, "dose2": dose2,
                                       "min_age": min_age, "vaccine": vaccineName, "fee_type": fee_type})

            return detailDict

        except Exception as e:
            print(e, 'in getslotinfo')

    def getCentersByPincode(self, pincode):
        try:

            date = datetime.today().date()
            date = date.strftime("%d-%m-%Y")
            min_age_limit = 18
            available_centers = []
            for codes in pincode:
                if codes.isdigit() and len(codes) == 6:
                    available_centers += self.cowin.get_availability_by_pincode(codes, date, min_age_limit)['centers']
            # print(available_centers)
            slotAvailable = []
            for center in available_centers:
                for sessions in center['sessions']:
                    if sessions['available_capacity'] > 0:
                        slotAvailable.append(center)
                        break

            return slotAvailable

        except Exception as e:
            print(e, 'in getcentersbypincode')

    def sendMail(self, body):
        try:

            self.mailServer.login('<sender e-mail>', '<sender-pass>')
            sub = 'Vaccine Slot Available Update'

            message = "Subject : {}\n\n{}".format(sub, body)

            self.mailServer.sendmail('from address', 'lis of to addresses', message)

            print('sent ..')
            self.mailServer.quit()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_obj, exc_tb.tb_linenos)
            print(e, 'in sendmail')

    def checkByPin(self, pincode):
        try:

            slotAvailable = self.getCentersByPincode([str(pincode)])
            if len(slotAvailable) > 0:
                detailDict = self.getSlotInfo(slotAvailable)
                return True, detailDict

            else:
                return False, "No slots available"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(e, 'in checkByPin')

    def checkByStateDistrict(self, state, district):
        try:
            states = self.cowin.get_states()['states']

            for st in states:
                if str(st['state_name']) == state:
                    state_id = st['state_id']
            districts = self.cowin.get_districts(state_id)['districts']
            for ds in districts:
                if str(ds['district_name']) == district:
                    district_id = ds['district_id']

            slotAvailable = self.getCentersByDistrict(state_id, district_id)
            if len(slotAvailable) > 0:
                detailDict = self.getSlotInfo(slotAvailable)
                return True, detailDict

            else:
                return False, "No slots available"

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(e, 'in checkByStateDistrict')


# run = FindSlot()
# res, output = self.checkByPin('221005')
# print(output)
# res, output = self.checkByStateDistrict('Uttar Pradesh', 'Varanasi')
# print(output)

# while (True):
#     mailBody = ''
#     try:
#         res, output = self.checkByStateDistrict('Uttar Pradesh', 'Varanasi')
#         for op in output:
#             if op['vaccine'] == 'COVAXIN' and op['min_age'] == 45 and op['date'] == '15-06-2021':
#                 mailBody += str(op)
#         if mailBody != '':
#             print(mailBody)
#             while True:
#                     playsound(r"C:\Users\DELL\Documents\first app\plugins\cordova-plugin-dialogs\src\ios\CDVNotification.bundle\beep.wav")
#                     time.sleep(2)
#         else:
#             print("No slots available")
#             time.sleep(5)
#     except Exception as e:
#         print(e, 'in while')
#         playsound(r"C:\Users\DELL\Documents\first app\plugins\cordova-plugin-dialogs\src\ios\CDVNotification.bundle"
#                   r"\beep.wav")

# while (True):
#     mailBody=''
#     slotAvailable=self.getCentersByPincode(['221005','221008'])
#     if len(slotAvailable)>0:
#         detailDict=self.getSlotInfo(slotAvailable)
#         for val in detailDict:
#             json_object = json.dumps(val, indent = 4)
#             mailBody=mailBody+json_object
#         if str(mailBody)!='':
#             print(mailBody)
#             print(datetime.today(),'##################')
#             while (True):
#                 playsound(r"C:\Users\DELL\Documents\first app\plugins\cordova-plugin-dialogs\src\ios\CDVNotification.bundle\beep.wav")
#                 time.sleep(2)
#
#     else:
#         print("No slots available")
#         time.sleep(5)
