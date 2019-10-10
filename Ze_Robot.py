import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

TOKEN = '토큰 키값을 입력 해주세요!' #BOT TOKEN KEY

updater = Updater(TOKEN)
updater.start_polling(poll_interval=0.0,
                          timeout=10,
                          clean=False,
                          bootstrap_retries=0)

InfoMsg = "저는 고객님의 제로페이에 대한 상담을 도와드릴 '제로' 입니다!\n" \
          "저는 제로페이에 대한 정보를 드릴 수 있어요!\n"

keyword_homepage = ['홈페이지', '사이트', '주소']
keyword_hi = ['안녕','hi','ㅎㅇ']
keyword_thanks = ['고마워','ㄳ','땡큐','감사','고맙습니다']
keyword_apply = ['가맹점신청','가맹점 신청','가맹점 참여','신청','참여']
keyword_member_store = ['주변','가맹점','찾기','사용처','사용']
keyword_payment_error = ['오류','오류코드','실패']
keyword_payment_help = ['결제방법','결제', '방법', '사용법','사용','결제']
keyword_what_zeropay = ['제로페이?','제로페이가','제로페이']
keyword_benefit = ['장점','혜택','좋은점','좋은 점']
keyword_bank = ['은행', '미지원']
keyword_plaform = ['어플','플랫폼']


def check_id(bot, update):
    try:
        id = update.message.chat.id
        print('Chat ID', id)
        return id
    except:
        id = update.channel_post.chat.id
        return id

def check_nickname(bot, update):
    try:
        nickname = update.message.from_user.first_name
        print('Chat NickName', nickname)
        return nickname
    except:
        nickname = update.channel_post.from_user.first_name
        return nickname

def start_command(bot, update):
    id = check_id(bot, update)
    show_list = []
    show_list.append(InlineKeyboardButton("소비자가 자주하는 질문", callback_data="소비자"))
    show_list.append(InlineKeyboardButton("가맹점주가 자주하는 질문", callback_data="가맹점"))
    show_list.append(InlineKeyboardButton("공통으로 자주하는 질문", callback_data="공통"))
    show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 1))  # make markup
    nickname = check_nickname(bot, update)
    bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
    update.message.reply_text("안녕하세요~ " + nickname +"님!\n" + InfoMsg , reply_markup=show_markup)


def help_command(bot, update):
    id = check_id(bot, update)
    nickname = check_nickname(bot, update)
    bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=id, text=nickname + "님! 제로봇은 대화형식으로 상담이 가능합니다.\n")


def build_box(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

# callback
def callback_get(bot, update):
    print("callback")

    if update.callback_query.data == "소비자":
        show_list = []
        show_list.append(InlineKeyboardButton("제로페이 홈페이지나 가맹점용 앱에서는 결제를 할 수 없나요?", callback_data="결제여부"))
        show_list.append(InlineKeyboardButton("제로페이로 결제한 내역과 매출액을 어디서 볼 수 있나요?", callback_data="결제내역"))
        show_list.append(InlineKeyboardButton("이벤트당첨자 확인은 어디서 하나요 ?", callback_data="당첨확인"))
        show_list.append(InlineKeyboardButton("결제된 건을 취소(환불)하고 싶습니다.", callback_data="환불"))
        show_list.append(InlineKeyboardButton("고정형 QR, 변동형 QR이 뭔가요?", callback_data="QR"))
        show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 4))
        bot.edit_message_text(text='고객님, 소비자가 자주하는 질문 리스트입니다!',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id, reply_markup=show_markup)

    elif update.callback_query.data == "가맹점":
        show_list = []
        show_list.append(InlineKeyboardButton("가맹점 신청", callback_data="신청"))
        show_list.append(InlineKeyboardButton("알바 결제", callback_data="알바"))
        show_list.append(InlineKeyboardButton("결제 내역, 매출액", callback_data="내역"))
        show_list.append(InlineKeyboardButton("가맹점 관리", callback_data="관리"))
        show_list.append(InlineKeyboardButton("QR코드 설치", callback_data="QR"))
        show_list.append(InlineKeyboardButton("가맹점용 APP", callback_data="APP"))
        show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 5))
        bot.edit_message_text(text='고객님, 가맹점주 분이 자주하는 질문 리스트입니다!',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id, reply_markup=show_markup)
    elif update.callback_query.data == "신청":
        bot.edit_message_text(text="제로페이 가맹점 신청은 홈페이지에 회원가입 후 가맹점 신청을 하거나 지자체에서 가맹점을 모집할 때 신청가능합니다.\n가맹점 신청은 사업자등록증에 기재된 대표자 본인이 가맹점 신청을 하실 수 있습니다.\n법인의 경우 대표자의 위임을 받은 대리인도 신청 가능합니다.\n운영하는 매장이 2개일 경우 가맹점 신청이 아닌 가맹점 추가를 해야합니다.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "알바":
        bot.edit_message_text(text="아르바이트생의 경우 홈페이지에 별도 가입하지 않으며 가맹점용 앱만으로 업무를 처리하게 됩니다.\n직원이 앱을 통해 직원등록을 신청하면 가맹점주가 이를 승인하게 되고,\n이후 결제내역관리, 결제취소, QR코드 관리가 가능해집니다.",chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "내역":
        bot.edit_message_text(text="제로페이 홈페이지 내 결제관리 메뉴를 통해 상세 결제내역과 결제통계를 조회가능하십니다.", chat_id=update.callback_query.message.chat_id
                                   ,message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "관리":
        bot.edit_message_text(text="가맹점 정보가 변경되었을 때 '가맹점관리>가맹점 정보관리' 메뉴에서 정보를 수정할 수 있습니다.\n가맹점의 모든 정보는 제로페이 담당자의 확인을 거친 후 반영됩니다.", chat_id=update.callback_query.message.chat_id
                                   ,message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "QR":
        bot.edit_message_text(text="제로페이 가맹점 신청 시 사업자 당 1개의 QR코드를 무료발급하며 택배배송을 해드리고 있습니다.\n만약 QR코드를 분실하면 홈페이지에서 사고신고 후 QR코드 결제를 정지할 수 있습니다.", chat_id=update.callback_query.message.chat_id
                                   ,message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "APP":
        bot.edit_message_text(text="가맹점용 앱에서는 가맹점신청이 불가능합니다.\n가맹점용 앱은 휴대폰으로 간편하게 제로페이 결제를 관리할 수 있고, 제로페이 결제취소 기능은 앱에서만 가능합니다.\n현재 가맹점 앱은 안드로이드 4.1 이상, ios 9.0 이상인 휴대폰에서 사용가능합니다.", chat_id=update.callback_query.message.chat_id
                                   ,message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "공통":
        print(update.callback_query.data)
        show_list = []
        show_list.append(InlineKeyboardButton("결제 오류", callback_data="오류"))
        show_list.append(InlineKeyboardButton("결제 취소", callback_data="취소"))
        show_list.append(InlineKeyboardButton("결제 방법", callback_data="결제"))
        show_list.append(InlineKeyboardButton("고정형 QR, 변동형 QR이 뭔가요?", callback_data="공통QR"))
        show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 1))
        bot.edit_message_text(text='고객님, 공통으로 자주하는 질문 리스트입니다!',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id, reply_markup=show_markup)
    elif update.callback_query.data == "오류":
        zeropayurl2 = 'https://www.zeropay.or.kr/main.do?pgmId=PGM1582'
        promo_keyboard = InlineKeyboardButton(text="오류코드조회", callback_data="openurl2", url=zeropayurl2)
        custom_keyboard = [[promo_keyboard]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.edit_message_text(text="결제/취소 시 오류발생에는 여러 원인이 있습니다.\n'오류코드확인' 또는 '오류코드조회'를 통해 오류코드(숫자3자리)의 상세내용을 조회하실 수 있습니다.\n"
                                   "아래 버튼을 눌러 오류코드를 조회하시면 됩니다.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id, reply_markup=reply_markup)
    elif update.callback_query.data == "취소":
        bot.edit_message_text(text="결제취소는 가맹점 앱에서 하실 수 있습니다.\n앱을 다운로드 받으신 후 '결제내역' 메뉴에서 취소하시기 바랍니다.\n(거래고유번호의 끝 4자리와 비밀번호 입력 후 취소)",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "결제":
        bot.edit_message_text(text="제로봇에게 결제 방법을 물어보면 친절하게 답해드립니다.\nex) 제로페이 결제는 어떻게 하니?",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "공통QR":
        bot.edit_message_text(text="결제할 때마다 동일한 QR을 사용하는 것을 고정형QR이라고 합니다.\n가맹점에 설치하는 QR코드가 고정형QR입니다.\n\n반대로 결제할 때마다 새로운 QR코드를 생성해 사용하는 것을 변동형QR이라고 합니다.\n소비자의 휴대폰에서 간편결제 앱을 구동하여 QR을 생성하는 방식입니다.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "결제여부":
        bot.edit_message_text(text='제로페이 홈페이지나 가맹점용 앱에는 결제기능이 없습니다.' \
                                   '제로페이 결제는 소비자가 이용하는 간편결제 앱이나 매장의 POS기에서 이루어집니다.'
                                   '가맹점용 앱에서는 정상결제된 건을 조회하여 결제취소를 할 수 있습니다.' \
                                   '자세한 결제 방법은 ‘제로페이소개>결제방법’ 메뉴 또는 공지사항의 ‘제로페이 가맹점 홈페이지 이용가이드’를 참조하십시오.',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

    elif update.callback_query.data == "결제내역":
        bot.edit_message_text(text='제로페이 홈페이지 내 결제관리 메뉴를 통해 상세 결제내역과 결제통계를 조회할 수 있습니다.' \
                                   '가맹점용 앱에서는 결제내역 조회와 더불어 결제취소가 가능합니다',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

    elif update.callback_query.data == "당첨확인":
        bot.edit_message_text(text='. www.zeropayevent.co.kr 페이지 가시면 1차 이벤트 당첨자 확인하실 수 있습니다!',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
    elif update.callback_query.data == "환불":
        bot.edit_message_text(text="결제취소는 가맹점 앱에서 하실 수 있습니다." \
                                   "앱을 다운로드 받으신 후 ‘결제내역’ 메뉴에서 취소하시기 바랍니다. (거래고유번호의 끝 4자리와 비밀번호 입력 후 취소)",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

    elif update.callback_query.data == "QR":
        bot.edit_message_text(text="1. 매장에 설치(부착)된 QR코드를 소비자의 휴대폰에서 간편결제 앱 카메라로 촬영하고 휴대폰에 금액을 입력하여 결제" \
                                   "2. 소비자의 휴대폰에서 간편결제 앱으로 QR코드를 생성하면, 매장직원이 스캐너로 휴대폰의 QR코드를 스캔하여 결제" \
                                   "2번 방식은 일부프랜차이즈 가맹점에서 실시 후 확대할 예정입니다." \
                                   "상세방법은 ‘제로페이소개>결제방법’ 메뉴 또는 공지사항의 ‘제로페이 가맹점 홈페이지 이용가이드’를 참조하십시오.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

def handler(bot, update):
    text = update.message.text
    id = check_id(bot, update)
    print(text)
    print(id)

    # 공통용 질문 - 시작

    if any(format in text for format in keyword_hi):
        bot.send_photo(chat_id=id, photo='https://hoy.kr/sSM17')
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id,
                         text="안녕하세요~ " + check_nickname(bot, update) + "님! :D\n궁금하신 점이 있어서 찾아오셨나보군요!\n편하게 말씀해주세요 ㅎ,ㅎ")

    # 공통용 질문 - 끝

    # 가맹점용 질문 - 시작

    #1.제로페이 가맹점 신청 - 시작

    #-   홈페이지에 들어오기 전에 이미 제로페이 가맹점 신청을 했습니다. 홈페이지에서 무엇을 해야 하나요?
    elif all(format in text for format in '이미') and all(format in text for format in '가맹점') \
            and all(format in text for format in '신청'):
        bot.send_message(chat_id=id, text="제로페이 홈페이지가 아닌 곳(별도 모집기관 등을 경유)에서 실물신청서 제출 등으로 이미 가맹점 신청을 하신 경우, "
                                          "다음의 절차에 따라 제로페이 이용이 가능합니다.\n ① 홈페이지에 회원가입을 해주십시오.\n"
                                          "② 가맹점관리>가맹점신청 메뉴에서 사업자번호로 신청하신 가맹점을 조회해 주십시오.\n"
                                          "③ 신청하신 가맹점이 조회되면 ‘연결하기’를 하여 회원ID와 신청 가맹점정보를 연결(매칭)합니다.\n"
                                          "④ 제로페이 가맹점앱을 설치하시고, QR코드를 배송받아 매장에 설치하신 후 제로페이를 이용합니다.")

    #-   가맹점 신청은 누가 할 수 있나요?
    elif all(format in text for format in '가맹점') and all(format in text for format in '누가') \
            and all(format in text for format in '신청'):
        bot.send_message(chat_id=id, text= "사업자등록증에 기재된 대표자(사업등록자) 본인이 가맹점 신청을 하실 수 있습니다.\n"
                                           "법인의 경우 대표자의 위임을 받은 대리인도 신청 가능합니다.")

    #-   소상공인만 가맹점 신청을 할 수 있나요?
    elif all(format in text for format in '만') and all(format in text for format in '가맹점') \
            and all(format in text for format in '신청'):
        bot.send_message(chat_id=id,text="아닙니다. 사업자번호를 보유한 법인 또는 개인사업자 누구나 가능하므로, 소상공인이 아닌 가맹점 및 대형 프랜차이즈도 제로페이 가맹점으로 가입할 수 있습니다.\n"
                                         "* 단, 도박, 사행성 업체 등 일부 업종 제외\n"
                                         "소상공인이 아닌 가맹점을 ‘일반가맹점’이라 하며, 별도의 가맹점수수료(신용카드보다 낮은 수준)가 적용됩니다.")

    #-   법인도 가맹점신청할 수 있나요?
    elif all(format in text for format in '법인') and all(format in text for format in '가맹점') \
            and all(format in text for format in '신청'):
        bot.send_message(chat_id=id,text="법인도 제로페이 가맹점 신청을 하실 수 있습니다.\n"
                                         "법인의 대표자 또는 대표자의 대리인이 신청하실 수 있습니다.\n"
                                         "대리인이 신청한 경우 법인의 제로페이 관리는 대표자가 아닌 대리인이 수행하게 되니 유의하시기 바랍니다.\n"
                                         "또한, 가맹점 신청 시 입금계좌를 법인 명의의 계좌를 사용하여야 합니다. (대표자 개인계좌 불가)")

    #-   가맹점 추가란 무엇인가요?
    elif all(format in text for format in '가맹점') and all(format in text for format in '추가'):
        bot.send_message(chat_id=id, text="이미 제로페이 가맹점 승인이 된 가맹점과 사업자번호가 동일한 다른 가맹점(매장)을 신청하는 것입니다.\n"
                                          "제로페이 가맹점은 사업자번호를 단위로 신청하므로 신규 가맹점 신청이 아닌 가맹점 추가로 신청할 수 있습니다.\n"
                                          "소상공인의 기준이 되는 전년도매출액과 상시근로자 수도 사업등록자를 기준으로 합니다.\n"
                                          "따라서 동일한 사업자등록증에 가맹점(매장)이 2개인 경우 2개 가맹점의 합을 기준으로 작성하여야 합니다.")

    #-   운영하는 매장(가맹점)이 2개 입니다. 가맹점 신청을 따로 해야 하나요?
    elif all(format in text for format in '가맹점') and all(format in text for format in '여러개') \
            and all(format in text for format in '따로'):
        bot.send_message(chat_id=id, text="사업자등록증(사업자번호)을 기준으로 신청합니다.\n"
                                          "2개의 가맹점의 사업자번호가 다른 경우, 별도로 신청하셔야 합니다.\n"
                                          "2개의 가맹점의 사업자번호가 같은 경우, 1개만 먼저 신청하시고 ‘가맹점 추가’를 하시면 됩니다. \n"
                                          "(가맹점 추가 메뉴는 향후 오픈 예정")

    #-   제로페이 가맹점이 되고 싶은데 어떻게 신청하나요?
    elif all(format in text for format in '가맹점') and all(format in text for format in '신청'):
        bot.send_message(chat_id=id, text="① 홈페이지에 회원가입하고 바로 가맹점 신청을 하실 수 있습니다.\n"
                                          "가맹점관리>가맹점신규신청 메뉴에서 신청된 내역이 있는지 조회하신 후 신청내역이 없으면 신규신청 하실 수 있습니다.\n\n"
                                          "② 서울시, 부산시, 경상남도 등 지자체에서 가맹점을 모집할 때 신청하실 수 있습니다. \n"
                                          "이 경우 실물(종이)신청서로 작성·제출하신 신청내역이 홈페이지에 등록됩니다.")
    #-   휴대폰 본인인증이 잘 안돼요
    elif all(format in text for format in '휴대폰') and all(format in text for format in '인증'):
        bot.send_message(chat_id=id, text="회원가입, 회원정보 변경, 비밀번호 찾기 등을 할 때 휴대폰 본인인증이 필요합니다.   \n"
                                          "휴대폰 본인인증이 잘 안되는 경우 아래 사항을 참고하십시오.\n\n"
                                          "(1) 인증절차 확인\n"
                                          "- 휴대폰 번호를 입력하신 후 '인증번호 받기' 버튼을 눌러야 인증번호가 발송되며,\n"
                                          "- 인증번호를 입력 후 '인증번호 확인' 버튼을 눌러야 인증이 완료됩니다.\n\n"
                                          "(2) 스팸등록여부 확인\n"
                                          "- 휴대폰 번호를 입력하고, '인증번호 받기' 버튼을 눌렀는데도 휴대폰으로 인증번호가 안오는 경우\n"
                                          "- 한국모바일인증의 발송전화번호(02-2033-8500)가 스팸으로 등록된 경우일 수 있습니다\n"
                                          "- 스팸등록은 본인이 직접할수도 있고, 스팸방지 프로그램에서 자동등록하는 경우도 있습니다\n\n"
                                          "(3) 이용횟수 5회 초과\n"
                                          "- 한국 모바일 인증을 통한 휴대폰 본인인증은 하루에 5번만 할 수 있습니다.\n"
                                          "- 이미 5번을 인증한 경우 다음날 다시 하실 수 있습니다\n\n"
                                          "(4) 알뜰폰 사용자가 통신3사 선택\n"
                                          "- 알뜰폰사용자의 경우 통신3사를 선택하지 마시고, 해당 통신사의 알뜰폰을 선택하셔야 합니다.")
    # 1.제로페이 가맹점 신청 - 끝

    # 2.제로페이 결제 - 시작

    #-   제로페이 홈페이지나 가맹점용 앱에서는 결제를 할 수 없나요?
    elif all(format in text for format in '홈페이지') and all(format in text for format in '결제'):
        bot.send_message(chat_id=id, text="제로페이 홈페이지나 가맹점용 앱에는 결제기능이 없습니다.\n"
                                          "제로페이 결제는 소비자가 이용하는 간편결제 앱이나 매장의 POS기에서 이루어집니다.\n\n"
                                          "가맹점용 앱에서는 정상결제된 건을 조회하여 결제취소를 할 수 있습니다.\n"
                                          "자세한 결제 방법은 ‘제로페이소개>결제방법’ 메뉴 또는 공지사항의 ‘제로페이 가맹점 홈페이지 이용가이드’를 참조하십시오.")

    #-   아르바이트생도 제로페이 결제를 관리할 수 있나요?
    elif all(format in text for format in '아르바이트') and all(format in text for format in '결제'):
        bot.send_message(chat_id=id, text="네 가능합니다. 다만, 직원(아르바이트생)의 경우 홈페이지에 별도 가입하지 않으며 가맹점용 앱만으로 업무를 처리하게 됩니다.\n"
                                          "직원이 앱을 통해 직원등록을 신청하면 가맹점주가 이를 승인하게 되고, 이후 결제내역관리, 결제취소, QR코드 관리가 가능합니다.\n"
                                          "자세한 사항은 공지사항의 ‘제로페이 가맹점앱 이용가이드’를 참조하십시오.")

    #-   결제하는 데 오류가 뜹니다.
    elif all(format in text for format in '결제') and all(format in text for format in '오류'):
        zeropayurl = 'https://www.zeropay.or.kr/main.do?pgmId=PGM1582'
        promo_keyboard = InlineKeyboardButton(text="오류 확인!", callback_data="openurl", url=zeropayurl)
        custom_keyboard = [[promo_keyboard]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=id, text="결제/취소 시 오류발생에는 여러 원인이 있습니다.\n"
                                          "아래의 버튼을 눌러 오류코드를 조회해 보세요.!", reply_markup=reply_markup)

    #-   결제된 건을 취소(환불)하고 싶습니다.
    elif all(format in text for format in '환불'):
        bot.send_message(chat_id=id, text="결제취소는 가맹점 앱에서 하실 수 있습니다.\n"
                                          "앱을 다운로드 받으신 후 ‘결제내역’ 메뉴에서 취소하시기 바랍니다.\n"
                                          "(거래고유번호의 끝 4자리와 비밀번호 입력 후 취소)")

    #-   제로페이로 결제한 내역과 매출액을 어디서 볼 수 있나요?
    elif all(format in text for format in '결제') and all(format in text for format in '환불'):
        bot.send_message(chat_id=id, text="제로페이 홈페이지 내 결제관리 메뉴를 통해 상세 결제내역과 결제통계를 조회할 수 있습니다.\n"
                                          "가맹점용 앱에서는 결제내역 조회와 더불어 결제취소가 가능합니다.")

    #-   제로페이는 어떻게 결제하는 건가요?
    elif all(format in text for format in '결제') and all(format in text for format in '방법') \
            and all(format in text for format in '가맹점'):
        bot.send_message(chat_id=id, text="제로페이 결제방식은 아래의 2가지가 있습니다.\n"
                                          "대부분의 가맹점에서는 첫 번째 방식으로 결제합니다.\n\n"
                                          "1. 매장에 설치(부착)된 QR코드를 소비자의 휴대폰에서 간편결제 앱 카메라로 촬영하고 휴대폰에 금액을 입력하여 결제\n\n"
                                          "소비자의 휴대폰에서 간편결제 앱으로 QR코드를 생성하면, 매장직원이 스캐너로 휴대폰의 QR코드를 스캔하여 결제\n\n"
                                          "2번 방식은 일부프랜차이즈 가맹점에서 실시 후 확대할 예정입니다.\n"
                                          "상세방법은 ‘제로페이소개>결제방법’ 메뉴 또는 공지사항의 ‘제로페이 가맹점 홈페이지 이용가이드’를 참조하십시오.")

    # 2.제로페이 결제 - 끝

    # 3.가맹점 관리 - 시작

    #-   가맹점(매장)의 정보가 변경되었습니다. 어디서 수정할 수 있나요?
    elif all(format in text for format in '정보') and all(format in text for format in '수정'):
        bot.send_message(chat_id=id, text="‘가맹점관리>가맹점 정보관리’메뉴에서 정보를 수정할 수 있습니다.\n"
                                          "가맹점의 모든 정보는 제로페이 담당자의 확인을 거친 후 반영됩니다.")

    #-   사업등록자(대표자)가 아닌 다른 사람이 제로페이를 관리하고 싶습니다.
    elif all(format in text for format in '등록자') and all(format in text for format in '다른')  \
            and all(format in text for format in '관리'):
        bot.send_message(chat_id=id, text="등록사업자(사업자등록증 상 대표자)와 가맹점주(실제 매장 운영자)가 다른 경우입니다.\n"
                                          "(예) 사업등록자는 남편이나, 부인이 실질적으로 매장을 운영하는 경우\n\n"
                                          "사업등록자는 실제 매장운영자를 가맹점주로 지정할 수 있습니다.\n"
                                          "(가맹점 신청 당시에는 사업등록자가 가맹점주로 등록되어 있음)\n"
                                          "경우 결제 관리, 직원 관리 등 가맹점 영업에 대한 메뉴는 가맹점주만 이용 가능하게 됩니다.\n"
                                          "자세한 사항은 ‘가맹점 이용안내>가맹점관리’메뉴 또는 공지사항의 ‘제로페이 가맹점 홈페이지 이용가이드’를 참조하십시오.")

    # 3.가맹점 관리 - 끝

    # 4.QR 코드 - 시작

    #-   한 매장에 여러 개의 QR코드를 사용하고 싶습니다.
    elif all(format in text for format in '여러개') and all(format in text for format in 'QR코드'):
        bot.send_message(chat_id=id, text="현재 사업자 당 1개의 QR코드를 무료발급 해드리고 있습니다.\n"
                                          "(지자체에 따라 무료발급 개수 및 유료QR코드 가격에 차이가 있을 수 있습니다.)\n"
                                          "1개의 가맹점에 여러개의 QR코드를 설치하고 싶으시면 ‘홈페이지>가맹점관리>고정형QR신청/발급 현황’ 메뉴에서 추가로 신청(유료)하실 수 있습니다.\n\n"
                                          "*QR코드 유료구매는 시범실시 이후 시행할 예정입니다.")

    #-   매장에 설치한 QR코드를 분실하면 어떻게 하나요?
    elif all(format in text for format in 'QR코드') and all(format in text for format in '분실'):
        bot.send_message(chat_id=id, text="홈페이지에서 사고신고를 하시면, 해당 QR코드 결제를 바로 정지할 수 있습니다.\n"
                                          "사고신고는 유선으로도 가능합니다.\n"
                                          "자세한 사항은 공지사항의 ‘제로페이 가맹점 홈페이지 이용가이드’를 참조하십시오.")

    #-   고정형QR, 변동형QR이 뭔가요?
    elif all(format in text for format in 'QR코드') and all(format in text for format in '분실'):
        bot.send_message(chat_id=id, text="결제할 때마다 동일한 QR을 사용하는 것을 고정형QR이라고 합니다.\n"
                                          "가맹점에 설치(부착)하는 QR코드가 고정형QR입니다.\n\n"
                                          "반대로 결제할 때마다 새로운 QR코드를 생성해 사용하는 것을 변동형QR이라고 합니다.\n"
                                          "소비자의 휴대폰에서 간편결제 앱을 구동하여 QR을 생성하는 방식입니다. (변동형 QR은 일부 프랜차이즈에서 시범 실시 후 확대 예정)\n"
                                          "자세한 사항은 ‘제로페이소개>결제방법’ 메뉴 또는 공지사항의 ‘제로페이 가맹점 홈페이지 이용가이드’를 참조하십시오.")

    #-   QR코드는 언제 받을 수 있나요?
    elif all(format in text for format in 'QR코드') and all(format in text for format in '받을'):
        bot.send_message(chat_id=id, text="가맹점 신청시 수일 후에 QR코드를 배송받으실 수 있습니다.\n"
                                          "가맹점 신청을 완료하면 제로페이 가맹점 승인담당자가 신청내역을 확인 후 승인하게 되며, \n"
                                          "이후 QR제작업체에 의뢰해 QR코드를 제작·배송합니다.")

    #-   QR코드를 매장에 설치하고 싶은데 어떻게 신청하나요?
    elif all(format in text for format in 'QR코드') and all(format in text for format in '설치'):
        bot.send_message(chat_id=id, text="제로페이 가맹점 신청 시 기본적으로 1개의 QR코드가 무료발급됩니다.\n"
                                          "가맹점 신청 시 기재하신 ‘QR배송주소지’로 QR코드가 택배로 배송됩니다")

    #-   매장에 QR코드를 설치하지 않으면 제로페이를 이용할 수 없나요?
    elif all(format in text for format in 'QR코드') and all(format in text for format in '설치') \
            and all(format in text for format in '이용'):
        bot.send_message(chat_id=id, text="제로페이를 이용하시려는 가맹점은 QR코드를 배송받아 매장에 설치하셔야 제로페이 결제를 이용할 수 있습니다.\n"
                                          "(일부 프랜차이즈 가맹점 제외)")

    # 4.QR 코드 - 끝

    # 5.앱 이용 - 시작

    #-   가맹점용 앱에서도 가맹점신청이 가능한가요?
    elif all(format in text for format in '앱') and all(format in text for format in '신청'):
        bot.send_message(chat_id=id, text="제로페이 가맹점신청은 첨부서류 등이 필요하여 현재 앱에서는 하실 수 없습니다.\n"
                                          "홈페이지에서 가맹점 신청을 해주시기 바랍니다.\n"
                                          "다만, 기존에 종이신청서로 가입신청을 하신 분은 앱에서 해당가맹점을 조회하여 연결(회원아이디에 가맹점을 등록)하실 수 있습니다.")

    #- 회원가입을 했는데 가맹점용 앱을 이용할 수 없습니다.
    elif all(format in text for format in '회원가입') and all(format in text for format in '가맹점 앱') \
            and all(format in text for format in '불가'):
        bot.send_message(chat_id=id, text="앱설치 후 최초 접속시 회원가입 또는 회원임을 확인해야 합니다.\n"
                                          "홈페이지에서 회원가입을 먼저 하고 앱을 설치하시면, 앱에서는 기존에 가입한 회원임을 확인하는 절차를 거친 후 간편비밀번호 6자리를 설정하고 로그인할 수 있습니다.\n"
                                          "홈페이지에서는 아이디/패스워드를 입력하여 로그인하고, 앱에서는 간편비밀번호 6자리만 입력하여 로그인 합니다.")

    #-   제로페이 가맹점용 앱은 왜 설치해야 하나요?’
    elif all(format in text for format in '가맹점용') and all(format in text for format in '설치') \
            and all(format in text for format in '이유'):
        bot.send_message(chat_id=id, text="제로페이 가맹점용 앱을 설치하시면 휴대폰으로 간편하게 제로페이 결제를 관리할 수 있습니다.\n"
                                          "또한 제로페이 결제취소 기능은 앱에서만 가능합니다.\n"
                                          "따라서 제로페이 가맹점주께서는 앱을 설치하시어 이용해주시기 바랍니다.")

    #-   제로페이 가맹점 앱은 어느 기종 휴대폰부터 사용이 가능한가요?
    elif all(format in text for format in '가맹점') and all(format in text for format in '앱') \
            and all(format in text for format in '기종'):
        bot.send_message(chat_id=id, text="o 안드로이드 폰/태블릿\n\n"
                                          "- 운영체제(OS)가 안드로이드4.1(젤리빈, 2012년 6월) 이상인 휴대폰(패드)에서 사용가능합니다.\n"
                                          "- 갤럭시 S3 이상의 모델에서 사용 가능합니다. 예전 모델인 경우 운영체제 업그레이드가 필요할 수 있습니다.\n\n"
                                          "o iOS(아이폰/아이패드)\n"
                                          "- 운영체제(OS)가 iOS 9.0(2015년) 이상인 휴대폰(패드)에서 사용가능합니다.\n"
                                          "- 아이폰은 4S, 아이패드는 2세대 이상의 모델에서 사용가능합니다. 예전 모델인 경우 운영체제 업그레이드가 필요할 수 있습니다.")
    # 5.앱 이용 - 끝

    # 가맹점용 질문 - 끝

    # 1.제로페이 결제- 시작

    #Q. 제로페이 홈페이지나 가맹점용 앱에서는 결제를 할 수 없나요?
    # elif all(format in text for format in '소비자') and all(format in text for format in '가맹점앱') \
    #         and all(format in text for format in '결제'):
    #     bot.send_message(chat_id=id, text="o 안드로이드 폰/태블릿\n\n"

    # 1.제로페이 결제- 끝

    # 소비자용 질문 - 시작
    # 소비자용 질문 - 끝


    # 제로페이 주소
    elif any(format in text for format in keyword_homepage):
        zeropayurl = 'https://www.zeropay.or.kr/'
        promo_keyboard = InlineKeyboardButton(text="Click!", callback_data="openurl", url=zeropayurl)
        custom_keyboard = [[promo_keyboard]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="고객님은 제로페이 홈페이지 주소를 알고 싶으신가보네요!\n텍스트 밑에 있는 버튼을 클릭하시면 홈페이지로 이동합니다.",
                         reply_markup=reply_markup)
    # 감사말
    elif any(format in text for format in keyword_thanks):
        bot.send_photo(chat_id=id, photo="https://hoy.kr/FfYKy")
        bot.send_message(chat_id=id, text="별말씀을요 :)")

    # 주변 가맹점 찾기
    elif any(format in text for format in keyword_member_store):
        zeropayurl = 'https://www.zeropay.or.kr/main.do?pgmId=PGM0081'
        promo_keyboard = InlineKeyboardButton(text="Click!", callback_data="openurl", url=zeropayurl)
        custom_keyboard = [[promo_keyboard]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="고객님! 제로페이를 사용할 수 있는 가맹점이 궁금하신가요?\n텍스트 밑에 있는 버튼을 클릭하시면 가맹점 찾기가 가능하십니다!",
                             reply_markup=reply_markup)

    # 오류 도움말
    elif any(format in text for format in keyword_payment_error):
        zeropayurl = 'https://www.zeropay.or.kr/main.do?pgmId=PGM1582'
        promo_keyboard = InlineKeyboardButton(text="Click!", callback_data="openurl", url=zeropayurl)
        custom_keyboard = [[promo_keyboard]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="고객님! 제로페이를 사용하시다가 오류가 나셨나요?\n텍스트 밑에 있는 버튼을 클릭하시면 오류코드조회가 가능하십니다!",
                         reply_markup=reply_markup)
    # 지원 은행,플랫폼
    elif any(format in text for format in keyword_bank) or any(format in text for format in keyword_plaform):
        show_list = []
        show_list.append(
            InlineKeyboardButton("핫플레이스", callback_data=None, url="https://www.facebook.com/watch/?v=1289628791185926"))
        show_list.append(
            InlineKeyboardButton("모바일 티머니", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/568435233564128/"))
        show_list.append(
            InlineKeyboardButton("체크 페이", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/309448153301632/"))
        show_list.append(
            InlineKeyboardButton("포스트페이", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/542319306173018/"))
        show_list.append(
            InlineKeyboardButton("SSGPAY", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/429081771000938/"))
        show_list.append(
            InlineKeyboardButton("광주은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/325875854748162/"))
        show_list.append(
            InlineKeyboardButton("하나 멤버스", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/367637034064236/"))
        show_list.append(
            InlineKeyboardButton("네이버 페이", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/724736127908060/"))
        show_list.append(
            InlineKeyboardButton("페이코 ", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/776164239383469/"))
        show_list.append(
            InlineKeyboardButton("케이뱅크", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/378812969590061/"))
        show_list.append(
            InlineKeyboardButton("우리은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/1093306087515228/"))
        show_list.append(
            InlineKeyboardButton("신한은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/2150179028532423/"))
        show_list.append(
            InlineKeyboardButton("수협은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/781832848820199/"))
        show_list.append(
            InlineKeyboardButton("부산은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/319518591980285/"))
        show_list.append(
            InlineKeyboardButton("뱅크페이", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/790012458009136/"))
        show_list.append(
            InlineKeyboardButton("머니트리", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/2244914939061335/"))
        show_list.append(
            InlineKeyboardButton("농협은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/265883530772988/"))
        show_list.append(
            InlineKeyboardButton("기업은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/2043751689052065/"))
        show_list.append(
            InlineKeyboardButton("국민은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/1115675438591919/"))
        show_list.append(
            InlineKeyboardButton("경남은행", callback_data=None,
                                 url="https://www.facebook.com/zeropay.official/videos/2004659056308325/"))
        show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 18))
        bot.send_message(chat_id=id, text='지원 하는 어플,은행 목록 입니다. 눌러서 사용방법을 확인해 보세요.', reply_markup=show_markup)

    # 결제방법
    elif any(format in text for format in keyword_payment_help):
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="제로페이 결제 방식은 3가지가 있습니다!")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="소비자 휴대폰의 간편결제 앱으로 가맹점에 부착된 QR코드를 촬영")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.send_photo(chat_id=id, photo="https://hoy.kr/REmON")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="소비자 휴대폰의 간편결제 앱으로 결제화면(무인계산기, PC모니터 등)에 보이는 QR코드를 촬영")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.send_photo(chat_id=id, photo="https://hoy.kr/yekRO")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="소비자 휴대폰의 간편결제 앱에 생성된 QR코드를 가맹점에서 스캔")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.send_photo(chat_id=id, photo="https://hoy.kr/Tyfmv")

    # 제로페이 혜택
    elif any(format in text for format in keyword_benefit):
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="제로페이를 사용하시면 총 3가지의 혜택이 있는데요..!")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="첫 번째 혜택 :: 제로페이 사용대금 40% 소득공제혜택")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="두 번째 혜택 :: 공공시설 이용요금 할인")
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=id, text="세 번째 혜택 :: 현재 사용하는 간편결제 앱을 그대로 사용가능")

    # 제로페이설명
    elif any(format in text for format in keyword_what_zeropay):
        bot.send_photo(chat_id=id, photo="https://hoy.kr/fTaE3")
        bot.send_message(chat_id=id, text="소상공인의 가맹점수수료 부담을 줄이기 위해 도입한 공동QR코드 방식의 모바일 간편결제서비스입니다.\n\n"
                                          "소비자는 기존에 사용하던 간편결제 앱을 그대로 사용하며 제로페이를 이용하여 소득공제(40%) 혜택과 각종 할인혜택을 받을 수 있습니다.\n\n")


    else:
        bot.send_photo(chat_id=id, photo="https://postfiles.pstatic.net/MjAxOTEwMDZfMTY0/MDAxNTcwMzM2NzA3MTgw.45lDKeI2KnhJF-C2ZpZQ8nXcHgMdks0dSwxdjN1q0kcg.4DM7-aDeeiLqZLEoZsztliZs6ICfIe2d0WSZ3vbo0ycg.JPEG.natephb1/sticker7.jpg?type=w966")
        zeropayurl1 = 'https://www.zeropay.or.kr/main.do?pgmId=PGM1580'
        zeropayurl2 = 'https://www.zeropay.or.kr/main.do?pgmId=PGM1581'
        promo_keyboard = InlineKeyboardButton(text="고객문의", callback_data="openurl2", url=zeropayurl2)
        promos_keyboard = InlineKeyboardButton(text="자주묻는질문", callback_data="openurl1", url=zeropayurl1)
        custom_keyboard = [[promo_keyboard],[promos_keyboard]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=id, text="죄송합니다 고객님.. 문제를 해결하지못하셨다면 밑에 있는 버튼을 클릭하시면 해결하실 수 있습니다.",
                         reply_markup=reply_markup)

updater.dispatcher.add_handler(MessageHandler(Filters.text, handler))
updater.dispatcher.add_handler(CommandHandler('start', start_command))
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))



updater.idle()
