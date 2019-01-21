import curses

from . import key_event
from .property import Mode


class Client:
    def __init__(self, debug=True):
        self.debug = debug
        self.status = Mode.READY
        self.window = None

    def close(self):
        self.status = Mode.CLOSE

    def key_handle(self, k):
        return getattr(key_event, f'key_{k}')(self)

    def key_event_loop(self):
        # 서브프로세스가 종료되면 서브프로세스 실행시킨 직전 상태로 되돌아간다.
        while self.status != Mode.CLOSE:
            c = self.window.getch()

            self.window.clear()
            self.key_handle(c)

            # debug
            if self.debug:
                self.window.chgat(-1)
                self.window.addstr(f'getch: {c}')

            # 상태가 변경되었을 경우 검색도 새로고침 할 수 있도록 한다.
            self.window.refresh()

            # window_hirarchy.noutrefresh_all()

            # Refresh the windows from the bottom up
            curses.doupdate()

    def main_window(self, stdscr):
        self.window = stdscr
        # 먼저 구글 같은 메인 화면에 진입한다.
        self.window.addstr('Bio', curses.A_REVERSE)
        self.window.chgat(-1, curses.A_REVERSE)

        if self.debug:
            win_size_str = f'{curses.LINES}, {curses.COLS}'
            self.window.addstr(0, curses.COLS - len(win_size_str), win_size_str,
                               curses.A_REVERSE)

            self.window.addstr(curses.LINES - 1, 0, "Press '^W' to quit",
                               curses.A_REVERSE)
            self.window.chgat(-1, curses.A_REVERSE)

        mid_point = curses.LINES // 2

        # Set up the window to search
        search_window = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
        text_window = search_window.subwin(3, curses.COLS - 4, mid_point - 2, 2)
        text_window.box()
        text_window.addstr(1, 2, f'Search your files.')

        # Draw a border around the main search window
        search_window.box()

        # Update the internal window data structures
        # window_hirarchy.noutrefresh_all()
        text_window.noutrefresh()
        search_window.noutrefresh()
        stdscr.noutrefresh()

        # Redraw the screen
        curses.doupdate()


@curses.wrapper
def main(stdscr):
    client = Client()
    curses.curs_set(0)
    client.main_window(stdscr)
    client.key_event_loop()


# 결과 영역은 자동완성과 비슷하며 키를 입력하는 중에 나타나는 컴포넌트의 구성은 다음과 같다
'''
파일이름
생성일 수정일             내용 미리보기
태그1 태그2 태그3
'''

# 나는 파일에 태그를 달아서 검색을 용이하게 하는 것이 목적이다.
# 파일 검색은 fzf, find 등의 다른 솔루션으로도 해결 가능하다. 나는 태그와 내용을 검색하기를 원한다.

# TODO:
# <ctrl> 키를 누르고 있으면 가능한 합성키를 해당하는 창 영역에 뿌려준다. - 이건 안되는 것 같음
# 검색 및 태그 히스토리를 윈도 크기를 지정하여 자동 저장시킨다.
# vim :wq에 git 을 후킹시킨다.
# 블로그로 퍼블리싱하는 방법도 생각해본다. ex: vimgolf
# github star 레포의 태그도 연동하는 것도 괜찮은 듯
