from yyagl.lib.gui import Text
from yyagl.engine.gui.page import Page
from yorg.thanksnames import ThanksNames
from .thankspage import ThanksPageGui


class SupportersPageGui(ThanksPageGui):

    def build(self, back_btn=True):  # parameters differ from overridden
        menu_props = self.menu_props
        text = ', '.join(ThanksNames.get_all_thanks())
        txt = Text(text, pos=(0, .72), wordwrap=16,
                   **menu_props.text_args)
        self.add_widgets([txt])
        ThanksPageGui.build(self)


class SupportersPage(Page):
    gui_cls = SupportersPageGui
