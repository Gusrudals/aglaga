# GALAGA - Classic Arcade Game

A faithful recreation of the classic Namco Galaga (1981) arcade game, written in Python using Pygame.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Pygame Version](https://img.shields.io/badge/pygame-2.5.0%2B-green)
![License](https://img.shields.io/badge/license-Educational-orange)

[한국어 버전](#한국어-설명서) | [English Version](#features)

---

## 🚀 Quick Start

### For Linux/macOS

```bash
# Clone the repository
git clone <repository-url>
cd galaga

# Install Pygame
pip3 install -r requirements.txt

# Run the game
python3 main.py
```

### For Ubuntu/Debian (Alternative Method)

```bash
# Install Pygame via apt (if pip is not available)
sudo apt-get update
sudo apt-get install python3-pygame

# Run the game
python3 main.py
```

### For Windows

```bash
# Install Pygame
pip install -r requirements.txt

# Run the game
python main.py
```

---

## Features

### Implemented Features ✓

- **Classic Galaga Gameplay**
  - Player fighter ship with smooth controls
  - Three enemy types: Bee, Butterfly, and Boss Galaga
  - Formation system with classic entry animations
  - Diving attack patterns unique to each enemy type
  - Progressive difficulty across stages

- **Combat System**
  - Player shooting with cooldown
  - Enemy projectiles
  - Capture beam mechanic (Boss Galaga)
  - Dual fighter mode after rescuing captured ship
  - Collision detection

- **Visual Effects**
  - Scrolling starfield background
  - Particle explosion effects
  - Enemy wing animations
  - Formation sway motion
  - Invulnerability blinking

- **Game Features**
  - Score system with bonuses
  - Multiple lives
  - Stage progression with increasing difficulty
  - High score tracking
  - Title screen and game over screen

### 🎮 Controls

| Action | Keys |
|--------|------|
| Move Left | ← (Left Arrow) or A |
| Move Right | → (Right Arrow) or D |
| Shoot | Space or Z |
| Quit Game | ESC |
| Start Game | Space or Enter |

## Installation

### Requirements

- Python 3.7 or higher
- Pygame 2.5.0 or higher

### Setup

1. Navigate to the galaga directory:
```bash
cd galaga
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

## Gameplay

### Objective

Destroy all enemy ships in each stage while avoiding their attacks and projectiles.

### Scoring

- **Bee**: 50 points (100 when diving)
- **Butterfly**: 80 points (160 when diving)
- **Boss Galaga**: 150 points (300 when diving)
- **Diving Boss**: 400 points
- **Rescued Fighter**: 500 points
- **Dual Fighter Bonus**: 1000 points

### Special Mechanics

#### Capture Beam

Boss Galaga enemies can deploy a tractor beam during dive attacks. If caught:
- Your fighter is captured and held by the Boss
- You lose control but don't lose a life
- Destroy the Boss holding your fighter to rescue it
- Rescuing your fighter activates Dual Fighter mode

#### Dual Fighter Mode

After rescuing a captured fighter:
- Control two fighters at once
- Fire two bullets simultaneously
- Massive firepower advantage
- Taking a hit only loses the dual fighter (not a life)

### Enemy Patterns

- **Bee**: Simple swooping dive attacks
- **Butterfly**: Loop-de-loop diving patterns
- **Boss Galaga**: Slower dives with potential capture beam deployment

## File Structure

```
galaga/
├── main.py          # Entry point
├── game.py          # Main game engine
├── player.py        # Player fighter class
├── enemy.py         # Enemy ship classes
├── formation.py     # Enemy formation system
├── bullet.py        # Projectile classes
├── particles.py     # Visual effects
├── constants.py     # Game constants
├── requirements.txt # Dependencies
└── README.md        # This file
```

## Technical Details

### Game Architecture

The game uses a classic game loop architecture:
1. Event handling (keyboard input, window events)
2. Game state update (physics, AI, collisions)
3. Rendering (drawing all game objects)
4. Frame rate control (60 FPS)

### Game States

- **Title**: Main menu
- **Stage Start**: Enemy entry animation
- **Playing**: Active gameplay
- **Game Over**: End screen

### Screen Resolution

- Original: 224×288 pixels
- This version: 672×864 pixels (3× scale)

## Credits

- **Original Game**: Namco (1981)
- **Python Recreation**: Created with Claude Code
- **Graphics**: Procedurally generated using Pygame primitives

## License

This is a fan recreation for educational purposes. Galaga is a trademark of Bandai Namco Entertainment Inc.

## Future Enhancements (Not Yet Implemented)

- Bonus/Challenging Stages
- Sound effects and music
- More authentic enemy formations
- Perfect shot bonus
- Additional attack patterns
- Save/load high scores

---

## 한국어 설명서

### 📖 게임 소개

남코의 클래식 아케이드 게임 갤러그(1981)를 파이썬과 Pygame으로 충실하게 재현한 게임입니다.

### 🎮 조작 방법

| 동작 | 키 |
|------|-----|
| 좌측 이동 | ← (왼쪽 화살표) 또는 A |
| 우측 이동 | → (오른쪽 화살표) 또는 D |
| 발사 | 스페이스바 또는 Z |
| 게임 종료 | ESC |
| 게임 시작 | 스페이스바 또는 엔터 |

### 💻 실행 방법

#### 방법 1: pip를 이용한 설치 (권장)

```bash
# 저장소 클론
git clone <repository-url>
cd galaga

# Pygame 설치
pip3 install -r requirements.txt

# 게임 실행
python3 main.py
```

#### 방법 2: apt를 이용한 설치 (Ubuntu/Debian)

pip이 설치되어 있지 않은 경우:

```bash
# Pygame 패키지 설치
sudo apt-get update
sudo apt-get install python3-pygame

# 게임 실행
python3 main.py
```

#### 방법 3: 실행 권한 부여 후 직접 실행

```bash
# 실행 권한 부여
chmod +x main.py

# 게임 실행
./main.py
```

### 🎯 게임 목표

각 스테이지의 모든 적 우주선을 파괴하면서 적의 공격과 발사체를 피하세요.

### 💯 점수 시스템

| 적 종류 | 기본 점수 | 다이빙 중 점수 |
|---------|----------|---------------|
| 벌 (Bee) | 50점 | 100점 |
| 나비 (Butterfly) | 80점 | 160점 |
| 보스 갤러그 (Boss) | 150점 | 300점 |
| 다이빙 보스 격파 | 400점 | - |
| 구출한 파이터 | 500점 | - |
| 듀얼 파이터 보너스 | 1000점 | - |

### 🚁 특수 메카닉

#### 캡처 빔 (Capture Beam)

보스 갤러그는 다이빙 공격 중 트랙터 빔을 발사할 수 있습니다:
- 빔에 잡히면 당신의 파이터가 보스에게 포획됩니다
- 조종권을 잃지만 생명은 잃지 않습니다
- 파이터를 들고 있는 보스를 파괴하면 구출할 수 있습니다
- 파이터를 구출하면 듀얼 파이터 모드가 활성화됩니다

#### 듀얼 파이터 모드 (Dual Fighter)

포획된 파이터를 구출한 후:
- 두 대의 파이터를 동시에 조종합니다
- 동시에 두 발의 탄환을 발사합니다
- 엄청난 화력 우위를 가집니다
- 피격 시 듀얼 파이터만 잃고 생명은 잃지 않습니다

### 👾 적 공격 패턴

- **벌 (Bee)**: 단순한 급강하 공격
- **나비 (Butterfly)**: 루프를 그리며 다이빙하는 패턴
- **보스 갤러그 (Boss)**: 느린 강하와 캡처 빔 발사 가능

### 📋 시스템 요구사항

- Python 3.7 이상
- Pygame 2.5.0 이상

### 📂 파일 구조

```
galaga/
├── main.py          # 게임 실행 파일
├── game.py          # 메인 게임 엔진
├── player.py        # 플레이어 파이터 클래스
├── enemy.py         # 적 우주선 클래스
├── formation.py     # 적 편대 시스템
├── bullet.py        # 발사체 클래스
├── particles.py     # 시각 효과
├── constants.py     # 게임 상수
├── requirements.txt # 의존성 목록
└── README.md        # 이 파일
```

### 🎨 기술적 세부사항

#### 게임 아키텍처

클래식 게임 루프 구조:
1. 이벤트 처리 (키보드 입력, 윈도우 이벤트)
2. 게임 상태 업데이트 (물리, AI, 충돌)
3. 렌더링 (모든 게임 오브젝트 그리기)
4. 프레임 레이트 제어 (60 FPS)

#### 게임 상태

- **Title**: 메인 메뉴
- **Stage Start**: 적 진입 애니메이션
- **Playing**: 실제 게임플레이
- **Game Over**: 게임 오버 화면

#### 화면 해상도

- 오리지널: 224×288 픽셀
- 이 버전: 672×864 픽셀 (3배 스케일)

### 🎮 게임 플레이 팁

1. **편대가 모두 진입할 때까지 기다리세요** - 진입 중에는 적이 예측 가능합니다
2. **다이빙하는 적을 우선 처치하세요** - 2배 점수를 획득할 수 있습니다
3. **듀얼 파이터 모드를 노리세요** - 보스의 캡처 빔에 일부러 잡히는 것도 전략입니다
4. **화면 측면을 활용하세요** - 적 탄환을 피하기 쉽습니다
5. **스테이지가 올라갈수록 더 빠르게 공격합니다** - 방어적으로 플레이하세요

### 🚀 향후 개선 사항

- 보너스/챌린징 스테이지
- 사운드 이펙트 및 음악
- 더 정교한 적 편대 패턴
- 퍼펙트 샷 보너스
- 추가 공격 패턴
- 하이스코어 저장/로드

### 📝 라이선스

이 프로젝트는 교육 목적의 팬 메이드 재현입니다. Galaga는 Bandai Namco Entertainment Inc.의 상표입니다.

### 👨‍💻 제작

- **오리지널 게임**: Namco (1981)
- **파이썬 재현**: Claude Code
- **그래픽**: Pygame 프리미티브를 이용한 절차적 생성

---

### ⚠️ 문제 해결

#### Pygame이 설치되지 않는 경우

**문제**: `pip` 명령어를 찾을 수 없음

**해결방법**:
```bash
sudo apt-get install python3-pip
```

**문제**: Display 오류 (WSL 환경)

**해결방법**: X Server 설치 또는 Windows에서 직접 실행

#### 게임이 느린 경우

`constants.py` 파일에서 FPS 값을 조정하세요:
```python
FPS = 30  # 기본값 60에서 30으로 변경
```

---

**즐거운 게임 되세요! 🎮✨**
