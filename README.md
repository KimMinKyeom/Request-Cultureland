# Request-Cultureland
+ Webdriver 보다 빠르고 정확하게 처리할 수 있는 requests 모듈을 사용하여 만든 컬처랜드 유틸

## 기능
+ 로그인
+ 문화상품권 충전
+ 잔액 확인 

## 사용
```
import cultureland

cl=Cultureland("ID","PW")
print(cl.charge("PIN-CODE"))
print(cl.get_balance())
```
