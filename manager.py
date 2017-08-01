import ugfx, badge, sys, gc
import uos as os
import machine, esp, time

ugfx.clear(ugfx.WHITE)
ugfx.flush()

ugfx.input_init()


"""
Currently, array[0] represents left, array[1] represents right.
"""
class Filemanager:
    def __init__(self):
        self.window = ugfx.Container(0, 0, ugfx.width(), ugfx.height())
        self.window.show()

        ugfx_half_width = int(ugfx.width() / 2)

        self.active_lane = 0
        self.item_counter = [0, 0]
        self.index = [0, 0]

        # h4x, manually trigger the list by binding the controls to key 0 and set selected_index manually
        self.options = [
            ugfx.List(0, 0, ugfx_half_width, ugfx.height(), parent=self.window, up=0, down=0),
            ugfx.List(ugfx_half_width, 0, ugfx.width(), ugfx.height(), parent=self.window, up=0, down=0)
        ]

        self.options[0].selected_index(0, True)
        self.options[0].set_focus()
        self.options[1].selected_index(0, False)
        self.options[1].set_focus()

        self.load_list(0, '/')
        self.load_list(1, '/lib')

        ugfx.input_attach(ugfx.JOY_UP, self.joy_up)
        ugfx.input_attach(ugfx.JOY_DOWN, self.joy_down)
        ugfx.input_attach(ugfx.JOY_LEFT, self.joy_left)
        ugfx.input_attach(ugfx.JOY_RIGHT, self.joy_right)
        ugfx.input_attach(ugfx.BTN_A, self.btn_a)
        ugfx.input_attach(ugfx.BTN_B, self.btn_b)
        ugfx.input_attach(ugfx.BTN_START, self.btn_start)
        ugfx.input_attach(ugfx.BTN_SELECT, self.btn_select)

    def joy_up(self, active):
        self.debug()
        if active and self.index[self.active_lane] > 0:
            self.index[self.active_lane] -= 1
            self.options[self.active_lane].selected_index(self.index[self.active_lane])
            self.draw()

    def joy_down(self, active):
        self.debug()
        if active and self.index[self.active_lane] < self.item_counter[self.active_lane]:
            self.index[self.active_lane] += 1
            self.options[self.active_lane].selected_index(self.index[self.active_lane])
            self.draw()

    def joy_left(self, active):
        self.debug()
        if active and self.active_lane != 0:
            self.switch_lane(0)
            self.draw()

    def joy_right(self, active):
        self.debug()
        if active and self.active_lane != 1:
            self.switch_lane(1)
            self.draw()

    def btn_a(self, active):
        self.debug()

    def btn_b(self, active):
        self.debug()

    def btn_start(self, active):
        self.debug()

    def btn_select(self, active):
        self.debug()

    def load_list(self, lane_number, path):
        self.item_counter[lane_number] = 0
        self.index[self.active_lane] = 0
        for file in os.listdir(path):
            self.item_counter[lane_number] += 1
            self.options[lane_number].add_item(file)
        self.draw()

    def switch_lane(self, lane_number):
        self.options[self.active_lane].selected_index(self.index[self.active_lane], False)
        self.active_lane = lane_number
        self.options[self.active_lane].selected_index(self.index[self.active_lane])
        self.options[self.active_lane].set_focus()
        self.draw()

    def debug(self):
        print("left_i: {}, left_s: {}, right_i: {}, right_s: {}, active_lane: {}".format(
            self.index[0],
            self.options[0].selected_index(),
            self.index[1],
            self.options[1].selected_index(),
            self.active_lane,
        ))

    def draw(self):
      ugfx.flush()
      #self.debug()

fm = Filemanager()

ugfx.set_lut(ugfx.LUT_FULL)
ugfx.flush()
badge.eink_busy_wait()
ugfx.set_lut(ugfx.LUT_FASTER)

gc.collect()

