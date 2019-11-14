import json
from cqhttp_helper import CQHttp


def parse(key, data):
    if key in data:
        return data[key]
    else:
        return "None"


class ContextFather:
    """
    所有父对象
    """
    def __init__(self, context):
        self.post_type = context["post_type"]
        self.user_id = context["user_id"]


class MessageFather:
    """
    信息父对象
    """
    def __init__(self, context):
        self.message_type = context["message_type"]
        self.message_id = context["message_id"]
        self.message = context["message"]
        self.raw_message = context["raw_message"]
        self.font = context["font"]
        self.sender = Sender(context["sender"])


class ContextMessage:
    """
    用于管理信息
    """
    def __init__(self):
        self.PRIVATE = "private"
        self.GROUP = "group"
        self.DISCUSS = "discuss"

    def auto_context(self, context):
        """
        自动判断信息类别并返回
        :param context: 传入数据
        :return: 返回对应类别对象
        """
        if context["message_type"] == "private":
            return self.Private(context)
        elif context["message_type"] == "group":
            return self.Group(context)
        elif context["message_type"] == "discuss":
            return self.Discuss(context)

    class Private(ContextFather, MessageFather):
        """
        私聊信息
        """

        def __init__(self, context):
            ContextFather.__init__(self, context)
            MessageFather.__init__(self, context)
            self.sub_type = context["sub_type"]

    class Group(ContextFather, MessageFather):
        """
        群消息
        """

        def __init__(self, context):
            ContextFather.__init__(self, context)
            MessageFather.__init__(self, context)
            self.sub_type = context["sub_type"]
            self.group_id = context["group_id"]

    class Discuss(ContextFather, MessageFather):
        """
        讨论组消息
        """

        def __init__(self, context):
            ContextFather.__init__(self, context)
            MessageFather.__init__(self, context)
            self.discuss_id = context["discuss_id"]


class ContextMasterChange(ContextFather):
    """
    管理人员变动
    """
    def __init__(self, context):
        ContextFather.__init__(self, context)
        self.group_id = context["group_id"]
        self.user_id = context["user_id"]
        self.sub_type = context["sub_type"]


class ContextGroupMemberReduce(ContextFather):
    """
    群成员舰少
    """
    def __init__(self, context):
        ContextFather.__init__(self, context)
        self.operator_id = context["operator_id"]
        self.group_id = context["group_id"]
        self.user_id = context["user_id"]
        self.sub_type = context["sub_type"]


class ContextGroupMemberAdd(ContextFather):
    """
    群成员增加
    """
    def __init__(self, context):
        ContextFather.__init__(self, context)
        self.operator_id = context["operator_id"]
        self.group_id = context["group_id"]
        self.user_id = context["user_id"]


class ContextFriendAdd(ContextFather):
    """
    添加好友
    """
    def __init__(self, context):
        ContextFather.__init__(self, context)
        self.request_type = context["request_type"]
        self.comment = context["comment"]
        self.flag = context["flag"]


class ContextGroupAdd(ContextFather):
    """
    添加群
    """
    def __init__(self, context):
        ContextFather.__init__(self, context)
        self.request_type = context["request_type"]
        self.comment = context["comment"]
        self.flag = context["flag"]
        self.sub_type = context["sub_type"]
        self.group_id = context["group_id"]


class Sender:
    def __init__(self, context):
        self.user_id = parse("user_id", context)
        self.nickname = parse("nickname", context)
        self.sex = parse("sex", context)
        self.age = parse("age", context)
        self.area = parse("area", context)
        self.card = parse("card", context)
        self.role = parse("role", context)


class ContextMessageType:
    def __init__(self):
        self.PRIVATE = "private"  # 私聊
        self.GROUP = "group"    # 群聊
        self.DISCUSS = "discuss"  # 讨论组


class ContextSubType:
    """
    sub_type对应信息
    """
    def __init__(self):
        # 私聊信息
        self.PRIVATE_FRIEND = "friend"  # 好友
        self.PRIVATE_GROUP = "group"  # 群
        self.PRIVATE_DISCUSS = "discuss"  # 讨论组
        self.PRIVATE_OTHER = "other"  # 临时会话

        # 群消息
        self.GROUP_NORMAL = "normal"  # 正常消息
        self.GROUP_ANONYMOUS = "anonymous"  # 匿名消息
        self.GROUP_NORMAL = "notice"  # 系统提示消息

        # 管理员变动
        self.MASTER_CHANGE_SET = "set"  # 设置管理员
        self.MASTER_CHANGE_UNSET = "unset"  # 取消管理员

        # 群成员减少
        self.GROUP_MEMBER_REDUCE_LEAVE = "leave"  # 正常退群
        self.GROUP_MEMBER_REDUCE_KICK = "kick"  # 被T退群
        self.GROUP_MEMBER_REDUCE_KICK_ME = "kick_me"  # 登录号被踢

        # 群成员增加
        self.GROUP_MEMBER_ADD_APPROVE = "approve"  # 正常退群
        self.GROUP_MEMBER_ADD_INVITE = "kick"  # invite

        # 加群邀请
        self.GROUP_INVITE_ADD = "add"
        self.GROUP_INVITE_INVITE = "invite"


class ContextRequestsType:
    def __init__(self):
        self.FRIEND = "friend"
        self.GROUP = "group"


class ContextNoticeType:
    def __init__(self):
        self.GROUP_UPLOAD = "group_upload"  # 群文件上传
        self.GROUP_ADMIN = "group_admin"  # 群管理员变动
        self.GROUP_DECREASE = "group_decrease"  # 群成员减少
        self.GROUP_INCREASE = "group_increase"  # 群成员增加
        self.FRIEND_ADD = "friend_add"  # 添加好友
        self.GROUP_WANT_ADD = ""


class FastReply:
    @staticmethod
    def group_message(reply="", auto_escape=True, at_sender=False, delete=False, kick=False, ban=False, ban_duration=0):
        """
        快速回复群消息
        :param reply: 回复的信息
        :param auto_escape:是否进行转义 默认False
        :param at_sender:是否@对象 默认False
        :param delete: 是否撤回 默认False
        :param kick: 是否踢出 默认False
        :param ban: 是否禁言, 默认False
        :param ban_duration: 禁言时长,单位分钟,默认为0
        :return: 返回json数据
        """
        return_message = dict()
        return_message["reply"] = reply
        return_message["auto_escape"] = auto_escape
        return_message["at_sender"] = at_sender
        return_message["delete"] = delete
        return_message["kick"] = kick
        return_message["ban"] = ban
        return_message["ban_duration"] = ban_duration
        return json.dumps(return_message)

    @staticmethod
    def discuss_message(reply="", auto_escape=True, at_sender=False):
        """
        快速回复讨论组信息
        :param reply: 回复的信息  
        :param auto_escape: 是否进行转义 默认False
        :param at_sender: 是否@对象 默认False
        :return: 
        """""
        return_message = dict()
        return_message["reply"] = reply
        return_message["auto_escape"] = auto_escape
        return_message["at_sender"] = at_sender
        return json.dumps(return_message)

    @staticmethod
    def private_message(reply="", auto_escape=True):
        """
        快速回复私聊信息
        :param reply: 回复的信息
        :param auto_escape: 是否进行转义 默认False
        """
        return_message = dict()
        return_message["reply"] = reply
        return_message["auto_escape"] = auto_escape
        return json.dumps(return_message)

    @staticmethod
    def add_friend(approve=False, remark=""):
        """
        加好友响应信息
        :param approve: 是否同意 默认False忽略
        :param remark: 同意进行备注
        :return:
        """
        return_message = dict()
        return_message["approve"] = approve
        return_message["remark"] = remark
        return json.dumps(return_message)

    @staticmethod
    def add_group(approve=False, reason=""):
        """
        加群响应信息
        :param approve: 是否同意 默认False忽略
        :param reason: 不同意的里有
        :return:
        """
        return_message = dict()
        return_message["approve"] = approve
        return_message["reason"] = reason
        return json.dumps(return_message)


class AddGroup:
    def __init__(self, context):
        self.sub_type = parse("sub_type", context)
        self.group_id = parse("group_id", context)
        self.user_id = parse("user_id", context)
        self.comment = parse("comment", context)
        self.flag = parse("flag", context)


class CqCode:
    @staticmethod
    def atQQ(qq):
        return "[CQ:at,qq={}]".format(str(qq))

    @staticmethod
    def file_image(path):
        return "[CQ:image,file=file:///{}]".format(str(path))

    @staticmethod
    def img(path):
        return "[CQ:image,file={}]".format(str(path))

    @staticmethod
    def share(url, title, content, image):
        return "[CQ:share,url={},title={},content={},image={}]".format(url, title, content, image)


ContextMessage = ContextMessage()
ContextMessageType = ContextMessageType()
ContextSubType = ContextSubType()
ContextNoticeType = ContextNoticeType()

