from botoy import Action, GroupMsg, S, FriendMsg, decorators, jconfig
from botoy.collection import MsgTypes
from botoy.parser import group as gp
from botoy.contrib import plugin_receiver

__doc__ = "主人可以通过机器人其他人进行对话"


@plugin_receiver.friend
@decorators.startswith(string="发消息")
def remote_chat(ctx: FriendMsg):
    """
    发消息 私聊\群聊 qq号\群号 内容
    例如：发消息 私聊 123456 你好
    """
    action = Action(ctx.CurrentQQ)
    box = ctx.Content.split(' ', 3)
    if box[1] == "私聊":
        try:
            action.sendFriendText(user=int(box[2]), content=box[3])
            S.text("私聊发送成功")
        except:
            S.text(text="格式错误或无该好友")
    elif box[1] == "群聊":
        try:
            action.sendGroupText(group=int(box[2]), content=box[3])
            S.text("群聊发送成功")
        except:
            S.text(text="格式错误或不在该群")


@plugin_receiver.group
@decorators.these_msgtypes(MsgTypes.AtMsg, MsgTypes.ReplyMsg)
def remote_return(ctx: GroupMsg):
    """
    想要通过机器人和主人聊天时 艾特或者回复机器人即可
    """
    action = Action(ctx.CurrentQQ)
    at_data = gp.at(ctx, clean=True)
    reply_data = gp.reply(ctx)
    if at_data is not None:
        if ctx.CurrentQQ in at_data.UserID:
            content = f"机器人收到来自:{ctx.FromGroupName}({ctx.FromGroupId})\n用户:{ctx.FromNickName}({ctx.FromUserId})\n内容:{at_data.Content}"
            action.sendFriendText(user=jconfig.master, content=content)
            S.text("消息已传达给主人")
    if reply_data is not None:
        if ctx.CurrentQQ in reply_data.UserID:
            content = f"机器人收到来自:{ctx.FromGroupName}({ctx.FromGroupId})\n用户:{ctx.FromNickName}({ctx.FromUserId})\n回复你发的消息:{reply_data.SrcContent}\n\n回复的内容:\n{reply_data.Content}"
            action.sendFriendText(user=jconfig.master, content=content)
            S.text("消息已传达给主人")
