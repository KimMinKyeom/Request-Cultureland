import requests, re
from mTransKey.transkey import mTransKey


class Cultureland:
    def __init__(self, user_id, password):
        self.session = requests.session()
        self.user_id = user_id
        self.password = password

    def _is_logged_in(self):
        response = self.session.post("https://m.cultureland.co.kr/mmb/isLogin.json")
        return response.text == 'true'

    def _login(self):
        if self._is_logged_in():
            return True

        trans_key = mTransKey(self.session, "https://m.cultureland.co.kr/transkeyServlet")
        password_pad = trans_key.new_keypad("qwerty", "passwd", "passwd")
        encrypted_password = password_pad.encrypt_password(self.password)
        hmac_value = trans_key.hmac_digest(encrypted_password.encode())

        data = {
            "agentUrl": "",
            "returnUrl": "",
            "keepLoginInfo": "",
            "phoneForiOS": "",
            "hidWebType": "other",
            "userId": self.user_id,
            "passwd": "*" * len(self.password),
            "transkeyUuid": trans_key.get_uuid(),
            "transkey_passwd": encrypted_password,
            "transkey_HM_passwd": hmac_value
        }
        self.session.post("https://m.cultureland.co.kr/mmb/loginProcess.do", data=data)
        return self._is_logged_in()

    def get_balance(self):
        if not self._login():
            return False,
        response = self.session.post("https://m.cultureland.co.kr/tgl/getBalance.json")
        result = response.json()
        if result['resultCode'] != "0000":
            return False, result
        return True, int(result['blnAmt']), int(result['bnkAmt'])

    def charge(self, pin):
        if not self._login():
            return False,

        pin = re.sub(r'[^0-9]', '', pin)
        if len(pin) not in [16, 18]:
            return False,

        pin_segments = [pin[i:i + 4] if i != 12 and len(pin) > 12 else pin[i:] for i in range(0, 14, 4)]
        self.session.get('https://m.cultureland.co.kr/csh/cshGiftCard.do')

        trans_key = mTransKey(self.session, "https://m.cultureland.co.kr/transkeyServlet")
        pin_pad = trans_key.new_keypad("number", "txtScr14", "scr14")
        encrypted_pin = pin_pad.encrypt_password(pin_segments[-1])

        data = {
            'scr11': pin_segments[0],
            'scr12': pin_segments[1],
            'scr13': pin_segments[2],
            'transkeyUuid': trans_key.get_uuid(),
            'transkey_txtScr14': encrypted_pin,
            'transkey_HM_txtScr14': trans_key.hmac_digest(encrypted_pin.encode())
        }
        response = self.session.post('https://m.cultureland.co.kr/csh/cshGiftCardProcess.do', data=data)
        charge_result = response.text.split('<td><b>')[1].split("</b></td>")[0]
        if '충전 완료' in response.text:
            return 1, int(response.text.split("<dd>")[1].split("원")[0].replace(",", ""))
        elif charge_result in ['이미 등록된 문화상품권', '상품권 번호 불일치']:
            return 0, charge_result
        elif '등록제한(10번 등록실패)' in charge_result:
            return 2, '등록제한'
        else:
            return 3, charge_result

    def gift(self, amount, recipient_phone=None):
        if not self._login():
            return False,
        response = self.session.post('https://m.cultureland.co.kr/tgl/flagSecCash.json').json()
        user_key = response['user_key']
        if not recipient_phone:
            recipient_phone = response['Phone']

        self.session.get('https://m.cultureland.co.kr/gft/gftPhoneApp.do')
        data = {
            "revEmail": "",
            "sendType": "S",
            "userKey": user_key,
            "limitGiftBank": "N",
            "giftCategory": "O",
            "amount": str(amount),
            "quantity": "1",
            "revPhone": str(recipient_phone),
            "sendTitl": "",
            "paymentType": "cash"
        }
        response = self.session.post('https://m.cultureland.co.kr/gft/gftPhoneCashProc.do', data=data)
        return '요청하신 정보로 전송' in response.text


if __name__ == "__main__":
    culture_land = Cultureland("USER_ID", "USER_PASSWORD")
    print(culture_land.charge("PIN_CODE"))
    print(culture_land.get_balance())
    print(culture_land.gift("AMOUNT", "PHONE_NUMBER"))
