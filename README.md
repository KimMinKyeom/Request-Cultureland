# Request-Cultureland
Webdriver의 리소스, 속도 등의 단점을 모두 보완할 수 있고 정확하게 처리할 수 있는 requests 모듈을 사용하여 만든 컬처랜드 유틸

## 기능
+ 로그인
+ 문화상품권 충전
+ 잔액 확인 
+ 핀번호 선물(전화번호)

## 사용
```
import cultureland

cl=cultureland.Cultureland("ID","PW")
print(cl.charge("PIN-CODE"))
print(cl.get_balance())
print(cl.gift("금액", "전화번호(필수X)"))
```
