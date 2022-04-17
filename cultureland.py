import requests, re
from mTransKey.transkey import mTransKey


class Cultureland:
    def __init__(self, id_, pw):
        self.s = requests.session()
        self.id_ = id_
        self.pw = pw

    def _islogin(self):
        resp = self.s.post("https://m.cultureland.co.kr/mmb/isLogin.json")
        if resp.text != 'true':
            return False
        else:
            return True

    def _login(self):
        if self._islogin():
            return True
        mtk = mTransKey(self.s, "https://m.cultureland.co.kr/transkeyServlet")
        pw_pad = mtk.new_keypad("qwerty", "passwd", "passwd")
        encrypted = pw_pad.encrypt_password(self.pw)
        hm = mtk.hmac_digest(encrypted.encode())
        resp = self.s.post("https://m.cultureland.co.kr/mmb/loginProcess.do", data={"agentUrl": "", "returnUrl": "", "keepLoginInfo": "", "phoneForiOS": "", "hidWebType": "other", "userId": self.id_, "passwd": "*" * len(self.pw), "transkeyUuid": mtk.get_uuid(), "transkey_passwd": encrypted, "transkey_HM_passwd": hm})
        self.cookie = f"JSESSIONID={str(resp.cookies).split('JSESSIONID=')[1].split(' ')[0]}"
        if self._islogin():
            return True
        else:
            return False

    def get_balance(self):
        if not self._login():
            return False,
        resp = self.s.post("https://m.cultureland.co.kr/tgl/getBalance.json")
        result = resp.json()
        if result['resultCode'] != "0000":
            return False, result
        return True, int(result['blnAmt']), int(result['bnkAmt'])  # (True, 사용가능, 보광중)

    def charge(self, pin):
        if not self._login():
            return False,
        pin = re.sub(r'[^0-9]', '', pin)
        if len(pin) != 16 and len(pin) != 18:
            return False,
        pin = [pin[i:i + 4] if i != 12 and len(pin) > 12 else pin[i:] for i in range(0, 14, 4)]
        self.s.get('https://m.cultureland.co.kr/csh/cshGiftCard.do')
        mtk = mTransKey(self.s, "https://m.cultureland.co.kr/transkeyServlet")
        pin_pad = mtk.new_keypad("number", "txtScr14", "scr14")
        encrypted = pin_pad.encrypt_password(pin[-1])
        resp = self.s.post('https://m.cultureland.co.kr/csh/cshGiftCardProcess.do', data={'scr11': pin[0], 'scr12': pin[1], 'scr13': pin[2], 'transkeyUuid': mtk.get_uuid(), 'transkey_txtScr14': encrypted, 'transkey_HM_txtScr14': mtk.hmac_digest(encrypted.encode())})
        result = resp.text.split('<td><b>')[1].split("</b></td>")[0]
        if '충전 완료' in resp.text:
            return 1, int(resp.text.split("<dd>")[1].split("원")[0].replace(",", ""))
        elif result in ['이미 등록된 문화상품권', '상품권 번호 불일치']:
            return 0, result
        elif '등록제한(10번 등록실패)' in result:
            return 2, '등록제한'
        else:
            return 3, result

    def gift(self, amount, phone=None):
        if not self._login():
            return False,
        resp = self.s.post('https://m.cultureland.co.kr/tgl/flagSecCash.json').json()
        user_key = resp['user_key']
        if not phone:
            phone = resp['Phone']
        self.s.get('https://m.cultureland.co.kr/gft/gftPhoneApp.do')
        resp=self.s.post('https://m.cultureland.co.kr/gft/gftPhoneCashProc.do', data={"revEmail": "", "sendType": "S", "userKey": user_key, "limitGiftBank": "N", "giftCategory": "O", "amount": str(amount), "quantity": "1", "revPhone": str(phone), "sendTitl": "", "paymentType": "cash"})
        if '요청하신 정보로 전송' in resp.text:
            return True
        else:
            return False


if __name__ == "__main__":
    cl = Cultureland("ID", "PW")
    print(cl.charge("PIN-CODE"))
    print(cl.get_balance())
    print(cl.gift("금액", "전화번호(필수X)"))
