
import OpenGL.GL as gl
import glfw
import imgui
import sys
from imgui.integrations.glfw import GlfwRenderer
from log import log
from context import Context


def impl_glfw_init():
    width, height = 800, 600
    window_name = "Сирень"

    if not glfw.init():
        log.error("Could not initialize OpenGL context")
        sys.exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        log.error("Could not initialize Window")
        sys.exit(1)

    return window


class Gui:
    def __init__(self):
        imgui.create_context()
        self._window = impl_glfw_init()
        self._impl = GlfwRenderer(self._window)
        self._should_close = False

        # io = imgui.get_io()
        # self._font = io.fonts.add_font_from_file_ttf("UbuntuMono-Regular.ttf", 16)
        # self._impl.refresh_font_texture()

    def update(self):
        glfw.poll_events()
        self._impl.process_inputs()
        imgui.new_frame()

        # imgui.push_font(self._font)
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(imgui.get_io().display_size.x, imgui.get_io().display_size.y)
        window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE
        if not imgui.begin('Custom window', flags=window_flags):
            imgui.end()

        self.draw_gui()

        imgui.end()

        # imgui.show_test_window()

        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # imgui.pop_font()
        imgui.render()
        self._impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self._window)

        self._should_close = glfw.window_should_close(self._window)

    def draw_gui(self):
        data = Context().data

        imgui.text('Settings')
        show, _ = imgui.collapsing_header('Trade config')
        if show:
            _, data.trade_url = imgui.input_text(label='Trades URL', value=data.trade_url)
            _, data.close_bid_btn_xpath = imgui.input_text(label='"Close bid btn" xpath', value=data.close_bid_btn_xpath)
            _, data.close_bid_error_btn_xpath = imgui.input_text(label='"Close bid error btn" xpath', value=data.close_bid_error_btn_xpath)
            _, data.seconds_refresh = imgui.input_int(label='Refresh after seconds', value=data.seconds_refresh)
            _, data.tg_bot_url = imgui.input_text(label='TG bot URL', value=data.tg_bot_url)
            imgui.separator()

            imgui.text('Lots')
            for i in range(1, len(data.lots) + 1):
                if imgui.tree_node('Lot #' + str(i)):
                    lot = data.lots[i - 1]
                    _, lot.time_left_xpath = imgui.input_text(label='"Time left" xpath', value=lot.time_left_xpath)
                    _, lot.best_bid_xpath = imgui.input_text(label='"Best bid" xpath', value=lot.best_bid_xpath)
                    _, lot.my_bid_xpath = imgui.input_text(label='"My bid" xpath', value=lot.my_bid_xpath)
                    _, lot.open_bid_btn_xpath = imgui.input_text(label='"Open bid btn" xpath', value=lot.open_bid_btn_xpath)
                    _, lot.seconds_left_min = imgui.input_int(label='Min value of seconds left', value=lot.seconds_left_min)
                    imgui.tree_pop()
            if imgui.button('Add new lot'):
                data.add_new_lot()
            if imgui.button('Save'):
                Context().config.save()
            imgui.separator()

        if imgui.button('START'):
            Context().webdriver.start()
        imgui.same_line()
        if imgui.button('STOP'):
            Context().webdriver.stop()

    def terminate(self):
        self._impl.shutdown()
        glfw.terminate()

    def should_close(self):
        return self._should_close;
