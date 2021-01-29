from panda3d.core import TextNode
from direct.gui.DirectGuiGlobals import ENTER, EXIT
from yyagl.lib.gui import Btn
from yyagl.observer import Subject
from yyagl.gameobject import GameObject
from yyagl.lib.gui import Label
from .button import StaticMPBtn, MPBtn


class UserLabel(GameObject):

    def __init__(self, name, parent, menu_props, is_supporter):
        GameObject.__init__(self)
        self.menu_props = menu_props
        self.name = name
        self.parent = parent
        lab_args = menu_props.label_args
        lab_args['scale'] = .046
        self.lab = Label(text=name, pos=(0, 0), parent=parent,
                         text_wordwrap=64, text_align=TextNode.A_left,
                         **lab_args)
        self.supp_btn = None
        self.set_supporter(is_supporter)
        self.set_online(True)

    @property
    def widgets(self): return [self.lab] + ([self.supp_btn] if self.supp_btn
                                            else [])

    def on_enter(self, pos):  # unused pos
        self.lab['text_fg'] = self.menu_props.text_active_col

    def on_exit(self, pos):  # unused pos
        self.lab['text_fg'] = self.menu_props.text_normal_col

    def set_supporter(self, is_supporter):
        if is_supporter:
            self.lab.set_x(.03)
            self.supp_btn = StaticMPBtn(
                self.parent, self, self.menu_props,
                'assets/images/gui/medal.txo', .01, None, self.name,
                _('Supporter!'))
        else:
            self.lab.set_x(0)
            if self.supp_btn:
                self.supp_btn = self.supp_btn.destroy()

    def set_online(self, val=None):
        self.is_online = val
        self.lab.set_alpha_scale(1 if self.is_online else .4)

    def destroy(self):
        self.lab.destroy()
        if self.supp_btn: self.supp_btn.destroy()
        GameObject.destroy(self)


class UserFrmMe(GameObject, Subject):

    def __init__(self, uid, is_supporter, pos, parent, menu_props,
                 msg_btn_x=.58):  # unused msg_btn_x
        Subject.__init__(self)
        GameObject.__init__(self)
        self.menu_props = menu_props
        self.frm = Btn(
            frame_size=(-.01, 2.54, .05, -.03), frame_col=(1, 1, 1, 0),
            pos=pos, parent=parent, cmd=self.on_cmd, extra_args=[uid])
        self.lab = UserLabel(uid, self.frm, menu_props, is_supporter)
        self.frm.bind(ENTER, self.on_enter)
        self.frm.bind(EXIT, self.on_exit)

    @property
    def widgets(self): return [self.frm] + self.lab.widgets

    def on_enter(self, pos):
        self.lab.on_enter(pos)

    def on_exit(self, pos):
        self.lab.on_exit(pos)

    def on_cmd(self, uid): self.notify('on_clicked', uid)

    def destroy(self):
        self.lab.destroy()
        self.frm.destroy()
        Subject.destroy(self)
        GameObject.destroy(self)


class UserFrm(UserFrmMe):

    def __init__(self, name, is_supporter, pos, parent,
                 menu_props, msg_btn_x=.58):
        UserFrmMe.__init__(self, name, is_supporter, pos, parent, menu_props,
                           msg_btn_x)
        # self.msg_btn = MPBtn(
        #     self.frm, self, menu_props, 'assets/images/gui/message.txo',
        #     msg_btn_x, self.on_msg, name, _('send a message to the user'))

    # def on_msg(self, uid):
    #     self.notify('on_add_chat', uid)

    # def on_enter(self, pos):
    #     UserFrmMe.on_enter(self, pos)
    #     if self.msg_btn.is_hidden(): self.msg_btn.show()

    # def on_exit(self, pos):
    #     UserFrmMe.on_exit(self, pos)
    #     if not self.msg_btn.is_hidden(): self.msg_btn.hide()


class UserFrmListMe(UserFrmMe):

    def __init__(self, uid, is_supporter, pos, parent, menu_props):
        UserFrmMe.__init__(
            self, uid, is_supporter, pos, parent, menu_props)

    # def enable_invite_btn(self, enable=True): pass


class UserFrmList(UserFrm):

    def __init__(self, name, is_supporter, is_playing, pos, parent,
                 menu_props):  # unused is_playing
        UserFrm.__init__(
            self, name, is_supporter, pos, parent, menu_props, .72)
        lab_args = menu_props.label_args
        lab_args['scale'] = .046
        lab_args['text_fg'] = self.menu_props.text_normal_col
        # self.__enable_invite_btn = not is_playing
        # self.invite_btn = MPBtn(
        #     self.frm, self, menu_props, 'assets/images/gui/invite.txo',
        #     .65, self.on_invite, name, _("%s isn't playing yorg") % name)
        # self.create_friend_btn(is_friend, menu_props, name_full)

    def create_friend_btn(self, is_friend, menu_props, name_full):
        pass
        # if not is_friend:
        #     self.friend_btn = MPBtn(
        #         self.frm, self, menu_props, 'assets/images/gui/friend.txo',
        #         .72, self.on_friend, name_full.name,
        #         _('add to xmpp friends'))
        # else:
        #     self.friend_btn = MPBtn(
        #         self.frm, self, menu_props, 'assets/images/gui/kick.txo',
        #         .72, self.on_unfriend, name_full.name,
        #         _('remove from xmpp friends'))

    # def enable_invite_btn(self, enable=True):
    #     self.__enable_invite_btn = enable

    # def on_invite(self, usr_name):
    #     self.eng.log('invite ' + usr_name)
    #     self.invite_btn.disable()
    #     self.notify('on_invite', self.eng.client.find_usr(usr_name))

    # def on_friend(self, usr_name):
    #     self.eng.log('friend with ' + usr_name)
    #     self.friend_btn.disable()
    #     self.notify('on_friend', usr_name)

    # def on_enter(self, pos):
    #     UserFrm.on_enter(self, pos)
    #     if self.invite_btn.is_hidden():
    #         self.invite_btn.show()
    #         if not self.__enable_invite_btn: self.invite_btn.disable()
    #         else: self.invite_btn.enable()
    #     #if self.friend_btn.is_hidden(): self.friend_btn.show()

    # def on_exit(self, pos):
    #     UserFrm.on_exit(self, pos)
    #     if not self.invite_btn.is_hidden(): self.invite_btn.hide()
    #     #if not self.friend_btn.is_hidden(): self.friend_btn.hide()

    # def on_unfriend(self, usr):
    #     self.eng.log('unfriend with ' + usr)
    #     self.friend_btn.disable()
    #     self.notify('on_unfriend', usr)


class UserFrmMatch(UserFrm):

    def __init__(self, uid, usr, is_supporter, pos, parent, menu_props):
        UserFrm.__init__(
            self, uid, is_supporter, pos, parent, menu_props, 1.0)
        self.frm['frameSize'] = (-.01, 1.06, .05, -.03)
        lab_args = menu_props.label_args
        lab_args['scale'] = .046
        lab_args['text_fg'] = self.menu_props.text_normal_col
        self.remove_btn = MPBtn(
            self.frm, self, menu_props, 'assets/images/gui/remove.txo',
            .92, self.on_remove, usr.uid, _("remove from the match"))

    @property
    def widgets(self): return [self.remove_btn] + UserFrm.widgets.fget(self)

    def on_remove(self, usr):
        self.notify('on_remove', usr)

    def on_enter(self, pos):
        UserFrm.on_enter(self, pos)
        if self.remove_btn.is_hidden():
            self.remove_btn.show()

    def on_exit(self, pos):
        UserFrm.on_exit(self, pos)
        if not self.remove_btn.is_hidden(): self.remove_btn.hide()
