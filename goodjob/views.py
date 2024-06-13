from django.shortcuts import render

# Create your views here.
import re
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    CarouselTemplate,
    MessageTemplateAction,
    ConfirmTemplate,
    CarouselColumn,
    PostbackEvent,
    PostbackAction,
    URIAction,
    PostbackTemplateAction,
    MessageAction,
    FollowEvent

)
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError

line_bot_api = LineBotApi('mmluZAv/Ft+MtWvbh/aGBkTvMCFULzFJUB4d0VlCBohVyNLL6qJ6WP/7zdWwW/flE/+TWtfwUyHeYCL2ltFCwjwsAbec2wCtDt/kiy3/o2ZQKwEUyXzrNFjLURFE4s9HVmPskTJ+WbZdcpjNZCfgaAdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('aa838be35f335ab70d4f4919f5b1dc55')
# parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
parser = WebhookParser('aa838be35f335ab70d4f4919f5b1dc55')
college_dict = {1:"資訊學群", 2:"生命科學學群", 3:"大眾傳播學群", 4:"建築設計學群", 5:"文史哲學群", 6:"教育學群", 7:"管理學群", 8:"工程學群", 9:"地球環境學群",
                10:"數理化學群", 11:"財經學群", 12:"醫藥衛生學群", 13:"生物資源學群", 14:"藝術學群", 15:"社會心理學群", 16:"外語學群", 17:"法政學群", 18:"遊憩運動學群"}
uot_dict = {}
mbti_dict = {"ISFJ":"照顧者", "ESFJ":"組織者",	"ISTJ":"監察者", "ESTJ":"管理者",	"ISFP":"⼿藝者",	"ESFP":"表演者",  "ISTP":"⼯匠者",	"ESTP":"遊說者", "INFP":"療癒者", 
            "ENFP":"激發者", "INFJ":"創作者",	"ENFJ":"教育者", "INTP":"設計者",   "ENTP":"發明者",    "INTJ":"戰略者",  "ENTJ":"統帥者"}
city_dict = {"A":"臺北市", "B":"新北市", "C":"桃園市", "D":"臺中市", "E":"臺南市", "F":"高雄市", "G":"基隆市", "H":"新竹市", "I":"嘉義市", "J":"新竹縣", "K":"苗栗縣", "L":"彰化縣",
            "M":"南投縣", "N":"雲林縣", "O":"嘉義縣", "P":"屏東縣", "Q":"宜蘭縣", "R":"花蓮縣", "S":"臺東縣", "T":"澎湖縣", "U":"金門縣", "V":"連江縣"}
discipline_cluster = ""
mbti = ""
city = ""

@csrf_exempt
def callback(request):
    global discipline_cluster, mbti, city
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
 
                if event.message.text == "哈囉":

                    line_bot_api.reply_message(  
                        event.reply_token, [
                            TextSendMessage(
                                text='Hello! Welcome to Good Job!',
                                ),
                            ImageSendMessage(
                                original_content_url='https://raw.githubusercontent.com/Lin8823/Lin/main/image/2021%E7%94%A2%E6%A5%AD%E7%BC%BA%E5%B7%A5%E6%95%B8.png',
                                preview_image_url='https://raw.githubusercontent.com/Lin8823/Lin/main/image/2021%E7%94%A2%E6%A5%AD%E7%BC%BA%E5%B7%A5%E6%95%B8.png'
                            ),
                            ImageSendMessage(
                                original_content_url='https://raw.githubusercontent.com/Lin8823/Lin/main/image/2021%E7%94%A2%E6%A5%AD%E5%B9%B3%E5%9D%87%E8%96%AA%E8%B3%87.png',
                                preview_image_url='https://raw.githubusercontent.com/Lin8823/Lin/main/image/2021%E7%94%A2%E6%A5%AD%E5%B9%B3%E5%9D%87%E8%96%AA%E8%B3%87.png'
                            ),

                            #----------------------補上地區生活費---------------------------------
                            # ImageSendMessage(
                            #     original_content_url='', 
                            #     preview_image_url=''
                            # ),

                            TemplateSendMessage(
                                alt_text='Confirm template',
                                template=ConfirmTemplate(
                                    text='Why are you here?',
                                    actions=[
                                        PostbackAction(
                                            label='Find Job',
                                            text='Find Job',
                                            data='job'
                                        ),
                                        PostbackAction(
                                            label='Find Talent',
                                            text='Find Talent',
                                            data='talent'
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                elif re.compile(r"[0-9]").match(event.message.text.strip(" ")) !=None and int(event.message.text.strip(" ")) in college_dict: #辨識使用者輸入之數字(對應到學群)
                    # college_dict[event.postback.data]
                    line_bot_api.reply_message(   
                        event.reply_token,
                        TextSendMessage(text="接著，請完成MBTI職業性格測試，並輸入你的測驗結果 (例：ESFJ )\n測驗網站：https://www.apesk.com/mbti/dati_tw.asp")
                    )
                    discipline_cluster = college_dict[int(event.message.text)] # 使用者輸入之數字對應至學群dic
                    print(discipline_cluster)
                    print(event.message.text)
                    print(type(event.message.text))

                elif re.compile(r"[A-Za-z]{4}").match(event.message.text.strip(" ")) !=None and event.message.text.upper().strip(" ") in mbti_dict: #辨識使用者輸入之MBTI
                    line_bot_api.reply_message(   
                        event.reply_token,
                        TextSendMessage(text="請選擇你希望的就業區域：\nA.臺北市\nB.新北市\nC.桃園市\nD.臺中市\nE.臺南市\nF.高雄市\nG.基隆市\nH.新竹市\nI.嘉義市\nJ.新竹縣\nK.苗栗縣\nL.彰化縣\nM.南投縣\nN.雲林縣\nO.嘉義縣\nP.屏東縣\nQ.宜蘭縣\nR.花蓮縣\nS.臺東縣\nT.澎湖縣\nU.金門縣\nV.連江縣\n")
                    )
                    mbti = event.message.text.upper().strip(" ")
                    print(mbti)
                    print(discipline_cluster)
                
                elif re.compile(r"[A-Za-z]{1}").match(event.message.text.strip(" ")) !=None and event.message.text.upper().strip(" ") in city_dict: # 縣市
                    city = event.message.text.upper().strip(" ")
                    city = city_dict[city] # 使用者輸入之數字對應至學群dic

                    line_bot_api.reply_message(  
                        event.reply_token, [
                            TextSendMessage(
                                text='以下為根據MBTI職業性格測試，以及你所就讀的學群所匹配出的合適職缺：',
                                ),
                            TemplateSendMessage(
                                alt_text='Carousel template',
                                template=CarouselTemplate(
                                    columns=[
                                        CarouselColumn(
                                            thumbnail_image_url='https://example.com/item1.jpg',
                                            title='this is menu1',
                                            text='description1',
                                            actions=[
                                                PostbackAction(
                                                    label='postback1',
                                                    display_text='postback text1',
                                                    data='action=buy&itemid=1'
                                                ),
                                                MessageAction(
                                                    label='message1',
                                                    text='message text1'
                                                ),
                                                URIAction(
                                                    label='uri1',
                                                    uri='http://example.com/1'
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                    print(mbti)
                    print(discipline_cluster)
                    print(city)
                
                # else:
                #     line_bot_api.reply_message(   
                #         event.reply_token,
                #         TextSendMessage(text="請輸入正確資料")
                #     )

            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
 
                if event.postback.data == "job": 
 
                    line_bot_api.reply_message(   
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ConfirmTemplate(
                                text='What educational system you\'re in?',
                                actions=[
                                    PostbackAction(  
                                        label='大學',  # ConfirmTemplate 顯示的選項
                                        text='大學',     #  user回覆顯示的字
                                        data='college'
                                    ),
                                    PostbackAction(
                                        label='技職',
                                        text='技職',
                                        data='uot'
                                    )
                                ]
                            )
                        )
                    )
                elif event.postback.data == "college":
                    line_bot_api.reply_message(   
                        event.reply_token,
                        TextSendMessage(text='''請選擇你的學群，並輸入相對應的數字：\n1.資訊學群\n2.生命科學學群\n3.大眾傳播學群\n4.建築設計學群\n5.文史哲學群\n6.教育學群\n7.管理學群\n8.工程學群\n9.地球環境學群\n10.數理化學群\n11.財經學群\n12.醫藥衛生學群\n13.生物資源學群\n14.藝術學群\n15.社會心理學群\n16.外語學群\n17.法政學群\n18.遊憩運動學群\n''')
                    )
                elif event.postback.data == "uot":
                    line_bot_api.reply_message(   
                        event.reply_token,
                        TextSendMessage(text='''請選擇你的學群，並輸入相對應的數字：\n1.機械群\n2.動力機械群\n3.電機與電子群電機類\n4.電機與電子群資電類\n5.化工群\n6.土木與建築群\n7.設計群\n8.工程與管理類\n9.商業與管理群\n10.衛生與護理類\n11.食品群\n12.家政群幼保類\n13.家政群生活應用類\n14.農業群\n15.外語群英語類\n16.外語群日語類\n17.餐旅群\n18.海事群\n19.水產群\n20.藝術群影視類\n''')
                    )

                
                    
                else:
                    line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text='功能尚未開發完成\n請耐心等候')
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

#-------------------------------------------------------------------
# @csrf_exempt
# def callback(request: HttpRequest) -> HttpResponse:
    
#     if request.method == "POST":
#         # get X-Line-Signature header value
#         signature = request.META['HTTP_X_LINE_SIGNATURE']

#         # get request body as text
#         body = request.body.decode('utf-8')

#         # handle webhook body
#         try:
#             # handler.handle(body, signature)
#             events = parser.parse(body, signature)  # 傳入的事件
#         except InvalidSignatureError:
#             return HttpResponseBadRequest()

#         for event in events:
#             if isinstance(event, MessageEvent):  # 如果有訊息事件
#                 if event.message.text == "哈囉":
#                     line_bot_api.reply_message(  # 回復傳入的訊息文字
#                                     event.reply_token,
#                                     TemplateSendMessage(
#                                         alt_text='Confirm template',
#                                         template=ConfirmTemplate(
#                                             text='Why are you here?',
#                                             actions=[
#                                                 PostbackAction(
#                                                     label='Find Jod',
#                                                     display_text='Find Jod', #使用者回覆顯示詞-->需更改，amybe more funny   
#                                                     data='job' #data='action=buy&itemid=1'
#                                                     ),
#                                                 PostbackAction(
#                                                     label='Find Talent',
#                                                     display_text='Find Talent',
#                                                     data='no'
#                                                     )
#                                                 ]
#                                             )
#                                         )
#                                     )
#             elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
#                 # if event.postback.data == "job":
#                 line_bot_api.reply_message(  # 回復傳入的訊息文字
#                     event.reply_token,
#                     TemplateSendMessage(
#                         alt_text='Confirm template',
#                         template=ConfirmTemplate(
#                             text='What educational system you\'re in?',
#                             actions=[
#                                 PostbackAction(
#                                     label='College',
#                                     display_text='College', #使用者回覆顯示詞-->需更改，amybe more funny   
#                                     data='College' #data='action=buy&itemid=1'
#                                     ),
#                                 PostbackAction(
#                                     label='University of Technology',
#                                     display_text='University of Technology',
#                                     data='University of Technology'
#                                     )
#                                 ]
#                             )
#                         )
#                     )
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()

# def message_text(event: MessageEvent):
#     if event.message.text == "哈囉":
#         # line_bot_api.reply_message(
#         #     event.reply_token,
#         #     TextSendMessage(text=event.message.text)
#         # )
#         line_bot_api.reply_message(  # 回復傳入的訊息文字
#                         event.reply_token,
#                         TemplateSendMessage(
#                             alt_text='Confirm template',
#                             template=ConfirmTemplate(
#                                  text='Why are you here?',
#                                  actions=[
#                                     PostbackAction(
#                                         label='Find Jod',
#                                         display_text='Find Jod', #使用者回覆顯示詞-->需更改，amybe more funny   
#                                         data='job' #data='action=buy&itemid=1'
#                                         ),
#                                     PostbackAction(
#                                         label='Find Talent',
#                                         display_text='Find Talent',
#                                         data='no'
#                                         )
#                                     # MessageAction(
#                                     #     label='message',
#                                     #     text='message text'
#                                     #     )
#                                     ]
#                                 )
#                             )
#                         )
#         #---------------------------處理PostbackEvent---------------------------------------------
# @handler.add(FollowEvent)
# def handle_follow(event: PostbackEvent):
# # @handler.add(PostbackEvent, message=TextMessage)
# # def postback_text(event: PostbackEvent):
#     # if isinstance(event, PostbackEvent):  # 如果有回傳值事件
#     if event.postback.data == "job":
#         line_bot_api.reply_message(  # 回復傳入的訊息文字
#                         event.reply_token,
#                         TemplateSendMessage(
#                             alt_text='Confirm template',
#                             template=ConfirmTemplate(
#                                 text='What educational system you\'re in?',
#                                 actions=[
#                                     PostbackAction(
#                                         label='College',
#                                         display_text='College', #使用者回覆顯示詞-->需更改，amybe more funny   
#                                         data='College' #data='action=buy&itemid=1'
#                                         ),
#                                     PostbackAction(
#                                         label='University of Technology',
#                                         display_text='University of Technology',
#                                         data='University of Technology'
#                                         )
#                                     ]
#                                 )
#                             )
#                         )




# TemplateSendMessage(
                        #     alt_text='Confirm template',
                        #     template=ButtonsTemplate(
                        #         title='Menu',
                        #         text='請選擇地區',
                        #         actions=[
                        #             MessageTemplateAction(
                        #                 label='台北市',
                        #                 text='台北市'
                        #             ),
                        #             MessageTemplateAction(
                        #                 label='台中市',
                        #                 text='台中市'
                        #             ),
                        #             MessageTemplateAction(
                        #                 label='高雄市',
                        #                 text='高雄市'
                        #             )
                        #         ]
                        #     )
                        # )
