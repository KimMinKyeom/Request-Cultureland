# Request-Cultureland

> **⚠️ 주의:** 현재 컬처랜드에서의 보안 업데이트로 인해 이 패키지의 로그인 기능이 제한되었음에 따라 막혔습니다.

Webdriver의 리소스, 속도 등의 단점을 모두 보완할 수 있고 정확하게 처리할 수 있는 requests 모듈을 사용한 컬처랜드 유틸

## Key Features
+ 로그인
+ 문화상품권 충전
+ 잔액 확인 
+ 핀번호 선물(전화번호 기입하지 않을 시 등록된 전화번호로)

## Quick Example
```py
import cultureland

cl=cultureland.Cultureland("ID","PW")
print(cl.charge("PIN-CODE"))
print(cl.get_balance())
print(cl.gift("금액", "전화번호"))
```

## Credit
- [mTranskey](https://github.com/Nua07/mTransKey)
