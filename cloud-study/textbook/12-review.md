# 12장. 시험 범위와 복습

[목차](README.md)

## 공식 범위 대응표

2026-09-16 확인한 SAA-C03 가이드의 과제별 대응이다. '다뤘다'는 시험 범위 전체를 완전하게 설명했다는 뜻이 아니다.

| 공식 과제 | 교재 | 추가 확인 |
|---|---|---|
| 1.1 안전한 자원 접근 | 2장 | 연합 인증·계정 간 역할·조직 정책 세부 |
| 1.2 안전한 워크로드 | 2~3장 | 보안 서비스별 적용 위치 |
| 1.3 데이터 보안 제어 | 2·5장 | 키 정책·보존·인증서 갱신 |
| 2.1 확장·느슨한 결합 | 4·7장 | 컨테이너·큐·워크플로 세부 |
| 2.2 고가용·내결함 | 6·8장 | 장애 전환·할당량·복구 검증 |
| 3.1 저장 성능·확장 | 5장 | FSx·하이브리드 저장·처리량 |
| 3.2 컴퓨팅 성능·탄력성 | 4·7장 | Batch·EMR·실행 제약 |
| 3.3 DB 성능 | 6장 | 엔진별 옵션·IOPS·마이그레이션 |
| 3.4 네트워크 성능 | 3장 | Global Accelerator·연결 구성 |
| 3.5 수집·변환 | 7장 | 스트리밍·배치·분석 형식 |
| 4.1 저장 비용 | 5·8장 | 계층별 조회·최소 보관 조건 |
| 4.2 컴퓨팅 비용 | 4·8장 | 약정·Spot·적정 크기 |
| 4.3 DB 비용 | 6·8장 | 용량 방식·복제·캐시 비용 |
| 4.4 네트워크 비용 | 3·8장 | 데이터 경로·전송·엔드포인트 |

공식 세부 범위: [보안](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03-domain1.html), [복원력](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03-domain2.html), [성능](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03-domain3.html), [비용](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03-domain4.html).

## 추가 공부할 서비스의 역할

- DMS: 데이터베이스 이전·복제 요구. 엔진 변경의 스키마 호환은 별도 검토.
- DataSync: 데이터 이동 자동화 요구. 네트워크·원본·대상 조건 확인.
- Storage Gateway: 온프레미스와 클라우드 저장 연계.
- Transfer Family: 파일 전송 프로토콜 기반 요구.
- Global Accelerator: 전역 네트워크 경로·애플리케이션 엔드포인트 요구.
- Organizations·Control Tower: 여러 계정의 조직·거버넌스.
- AWS Backup: 지원 자원의 중앙 백업 정책.
- CloudFormation: 선언한 구성으로 인프라 재현.
- OpenSearch: 검색·로그 분석 등 요구.
- Redshift: 분석용 웨어하우스.

각 서비스는 이름만 암기하지 말고 '대체 후보, 선택 조건, 하지 않는 일'을 1개씩 적는다.

## 영어 용어 30개

| 용어 | 뜻 | 기억할 질문 |
|---|---|---|
| Availability | 가용성 | 요청에 응답 가능한가? |
| Durability | 내구성 | 데이터를 잃지 않고 보관하는가? |
| Resilience | 복원력 | 실패에 대응·회복하는가? |
| Fault tolerance | 내결함성 | 고장 중에도 요구 기능 유지? |
| Scalability | 확장성 | 더 큰 부하를 처리할 수 있는가? |
| Elasticity | 탄력성 | 수요에 맞게 늘고 줄어드는가? |
| Latency | 지연 | 한 요청이 얼마나 걸리는가? |
| Throughput | 처리량 | 단위 시간에 얼마나 처리하는가? |
| Concurrency | 동시성 | 동시에 몇 개가 진행되는가? |
| Authentication | 인증 | 누구인가? |
| Authorization | 인가 | 무엇을 해도 되는가? |
| Principal | 요청 주체 | 누가 호출했는가? |
| Policy | 정책 | 어떤 작업·대상을 허용하는가? |
| Role | 역할 | 어떤 임시 권한을 맡는가? |
| Least privilege | 최소 권한 | 꼭 필요한 권한인가? |
| Encryption at rest | 저장 암호화 | 보관 중 보호하는가? |
| Encryption in transit | 전송 암호화 | 이동 중 보호하는가? |
| Subnet | 서브넷 | 네트워크 주소의 어느 구간인가? |
| Route | 경로 | 다음 목적지는 어디인가? |
| Endpoint | 서비스 접점 | 어디로 접근하는가? |
| Failover | 장애 전환 | 장애 후 어디로 전환하는가? |
| Replica | 복제본 | 사본은 어떤 용도인가? |
| Snapshot | 시점 사본 | 어느 시점 상태인가? |
| Lifecycle | 수명 주기 | 언제 전환·삭제하는가? |
| Throttling | 요청 제한 | 허용 처리량을 넘었는가? |
| Idempotency | 멱등성 | 반복해도 중복 효과가 없는가? |
| Decoupling | 결합 완화 | 서로 독립적으로 처리 가능한가? |
| TTL | 유효 시간 | 언제 만료되는가? |
| RTO | 복구 시간 목표 | 언제까지 복구해야 하는가? |
| RPO | 복구 시점 목표 | 얼마의 데이터 손실을 허용하는가? |

## 오답을 줄이는 읽기 순서

1. 요구사항에서 '가장 적은 운영 부담', '지연', '비용', '데이터 손실'을 표시한다.
2. 반드시 충족해야 하는 조건과 선호 조건을 구분한다.
3. 기술적으로 불가능하거나 필수 조건을 어기는 보기를 제외한다.
4. 남은 보기에서 요구한 최적화 기준을 비교한다.
5. 복수 응답은 지정된 개수와 각 선택의 역할을 확인한다.

예: '최저 비용'이라고 해도 즉시 조회가 필수인 데이터를 장기 복원 대기 계층에 넣을 수는 없다. 먼저 기능 조건을 충족해야 한다.

## 복습 간격

당일: 핵심 3줄 → 다음 날: 보지 않고 설명 → 3일 후: 다른 문제 → 1주 후: 설계 사례. 틀린 문제 번호가 아니라 틀린 원인을 기억한다.

## 시험 전 확인

- [ ] 최신 시험 코드·지원 언어·예약 조건 확인.
- [ ] 공식 범위 내 낯선 서비스의 역할 정리.
- [ ] 시간 제한 아래 새로운 문제 풀이.
- [ ] 정답 이유와 오답 이유 설명.
- [ ] 온라인 응시라면 환경 검사·신분 확인 요건 확인.
- [ ] 준비가 부족하면 예약 변경 가능 시한 전에 판단.

자체 문제집 점수는 공식 환산점수나 합격 예측값이 아니다.
