# 검토한 공개 Skill과 사용 우선순위

확인일: 2026-10-31. 아래 다섯 후보의 실제 `SKILL.md`를 읽고 원본 커밋을 고정했다. 이 목록의 순위는 제한 시간 프로젝트를 위한 준비 제안이며, 대회 채점 기준이나 도구 허용 인증이 아니다. 외부 Skill 본문은 이 저장소에 복사하지 않았다.

**권장 시작점은 이 저장소의 짧은 작업 Skill과 실제 검증 습관이다.** 외부 후보는 해당 문제가 있을 때만 읽는다. 전부 설치하거나 프레임워크·MCP를 추가할 필요는 없다.

| 후보 | 실제로 돕는 일 | 필요한 환경·부담 | 선택 기준과 주의 |
|---|---|---|---|
| [verification-before-completion](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md) | 완료 주장과 실제 검사 근거 연결 | 검사 명령을 실행할 수 있는 기존 환경. 별도 외부 AI는 요구하지 않음 | **우선 참고.** 요구 충족을 테스트 통과와 구분하는 관점이 유용하다. 매 메시지마다 전체 검사를 반복하는 운영 부담은 고려한다. |
| [systematic-debugging](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/SKILL.md) | 오류 재현, 입력·출력 추적, 원인 가설과 최소 수정 | 로컬 코드·오류 로그·실행 명령. 같은 폴더의 참조 파일과 다른 Superpowers Skill을 참조함 | **오류 때만 참고.** `SKILL.md` 한 파일만으로 모든 보조 절차가 갖춰졌다고 보지 않는다. 예시의 환경 변수·자격증명 진단을 무분별하게 실행하지 않는다. |
| [frontend-design](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/frontend-design/SKILL.md) | 사용 목적에 맞는 화면 계층·레이아웃·색·글·상태 표현 | 현재 웹 구현 환경. 특정 외부 모델 연결은 요구하지 않음 | **핵심 동작 후 선택.** 업무 도구에서는 읽기·표·오류·저장 상태를 먼저 다룬다. 시각적 차별화 때문에 필수 기능·검증 시간을 줄이지 않는다. 자동 화면 조작은 별도 규칙을 따른다. |
| [security-best-practices](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-best-practices/SKILL.md) | Python·JavaScript/TypeScript·Go의 보안 검토와 안전한 기본 구현 | 해당 언어·프레임워크별 `references/` 파일. 별도 계정 연결은 기본 요구가 아님 | **관련 위험이 있을 때 선택.** 명시적인 보안 검토 등에 적용하는 Skill이다. 입력 검증·출력 처리·파일 경로 같은 실제 범위를 좁히고, 무관한 대규모 보안 개편을 시작하지 않는다. |
| [playwright](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/SKILL.md) | 실제 브라우저 탐색·폼 입력·스크린샷 등 자동 검사 | Node/npm, npx 또는 CLI, 브라우저 실행 환경과 래퍼·참조 파일 | **자동 조작 금지 평가에는 추천 제외.** 공식 Skill 본문이 브라우저 자동 조작을 명시한다. 특정 시험이 Playwright라는 제품명을 금지했다는 주장이 아니라, 기능이 자동 조작 제한과 충돌할 수 있어 제외하는 판단이다. 제한 없는 개인 연습 환경에서만 별도로 검토한다. |

## 과도하게 가져오지 않기

- 필요한 Skill 폴더와 참조 파일을 원본 구조로 확인한다. `.md` 하나를 복사하고 설치·연결이 완료됐다고 쓰지 않는다.
- 외부 Skill의 ‘필수’ 지시도 사용자 요청·과제 규칙·환경 권한을 바꾸지 못한다. 새 모델·계정·브라우저 자동화·배포를 자동 허용하지 않는다.
- 공개 소스의 사용 조건과 실제 라이선스는 해당 저장소·Skill의 최신 파일을 확인한다. 여기에 링크가 있다는 이유로 완성품 반입·재배포가 허용되는 것은 아니다.
- 실제 평가 중 사용 여부는 현재 공식 안내와 운영자 판단을 따른다. 참가 후기의 점수·순위만으로 이 Skill의 효과를 확정하지 않는다.

## 참고 출처

- [OpenAI 공식 Skill 작성·발견·설치 안내](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI 공개 Skill 목록](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated)
- [크래프톤 FDE 코파톤 참가 후기](https://brunch.co.kr/@luma/5): 다른 행사 참가자의 경험·관찰이다. 이번 시험의 확정 배점·문항·도구 규칙을 뜻하지 않는다.

원본 파일의 경로·커밋·SHA256은 [PUBLIC_SOURCES.json](PUBLIC_SOURCES.json)에 기록했다. 실제 외부 코드·Skill 설치와 실행 검증은 별도로 하지 않았다.
