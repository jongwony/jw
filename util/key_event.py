# 한글 키도 입력 및 명령이 가능하여야 한다.
from .property import Mode


# 언제든 <ctrl+w> 로 종료할 수 있다.
def key_23(client):
    client.close()


# 아무 키를 누르면 검색 화면 구성으로 변경되며, 검색 영역과 결과 영역을 <ctrl+j,k> 키로 넘나들 수 있다.
def key_10(client):
    client.window.addstr('검색 모드')


def key_11(client):
    client.window.addstr('결과 모드')


# <ctrl+t> 를 누르면 태그만을 검색하는 모드로 바뀐다. 다시 누르면 비활성화된다. 체크 박스가 필요하다.
def key_20(client):
    client.window.addstr('태그 필터')


# <ctrl+i> 로 대소문자 무시 검색 모드를 변경하도록 한다. 체크박스 필요하다.
def key_9(client):
    client.window.addstr('대소문자 무시 필터')


# <ctrl+r> 를 누르면 python regex 를 사용하는 모드로 바뀐다. 다시 누르면 비활성화된다. 체크 박스가 필요.
def key_18(client):
    client.window.addstr('regex 필터')


# <ctrl+h,l> 키로 head, tail 미리보기 상태를 변경하도록 한다. 표시영역이 필요하다.
def key_8(client):
    client.window.addstr('head detail')


def key_12(client):
    client.window.addstr('tail detail')


# 결과 영역은 포커싱, 포커싱 외 영역으로 구분되며, <hjkl> 키로 넘나들 수 있다. jk는 항목 이동 hl는 태그 이동
def key_104(client):
    if client.status == Mode.RESULT:
        client.window.addstr('h')


key_72 = key_104
key_151 = key_104


def key_108(client):
    if client.status == Mode.RESULT:
        client.window.addstr('l')


key_76 = key_108
key_163 = key_108


def key_106(client):
    if client.status == Mode.RESULT:
        client.window.addstr('j')


key_74 = key_106
key_147 = key_106


def key_107(client):
    if client.status == Mode.RESULT:
        client.window.addstr('k')


key_143 = key_107
key_75 = key_107


def key_118(client):
    if client.status == Mode.RESULT:
        client.window.addstr('vim')


key_86 = key_118
key_141 = key_118


# <ctrl+v>로 새 임시파일을 생성할 수 있다. draft 태그를 자동 지정한다.
def key_22(client):
    client.window.addstr('create temp file')


# 포커싱 영역에서 a를 누르면 신규 태그,
def key_97(client):
    client.window.addstr('add tag')


key_65 = key_97
key_129 = key_97


# u를 누르면 현재 포커싱 태그 수정,
def key_117(client):
    client.window.addstr('update tag')


key_85 = key_117
key_149 = key_117


# d를 누르면 태그를 삭제한다.
def key_100(client):
    client.window.addstr('delete tag')


key_68 = key_100
key_135 = key_100
