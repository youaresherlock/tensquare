from django.urls import path, include
from django.urls import re_path
from apps.asks.views.labels import LablesView, LablesUserView, LabelDetailView, FocusinLabelView, FocusoutLabelView, LabelFullView
from apps.asks.views.questions import QuestionLabelsView, QuestionHotView, QuestionWaitView, PostQuestion, \
    QuestionDetail, QuestionUseful, QuestionUnuseful, QuestionReply, ReplyUseful, ReplyUnuseful


urlpatterns = [
    # 注册标签列表
    re_path(r"^labels/$", LablesView.as_view()),
    # 注册用户关注标签
    re_path(r"^labels/users/$", LablesUserView.as_view()),
    # 标签详情/labels/{id}/
    path("labels/<int:pk>/", LabelDetailView.as_view()),

    # labels/{id}/focusin/ 关注标签
    path("labels/<int:pk>/focusin/", FocusinLabelView.as_view()),
    # 取消关注
    path("labels/<int:pk>/focusout/", FocusoutLabelView.as_view()),
    # 获取更多标签
    path('labels/full/', LabelFullView.as_view()),
    # 获取问题标签
    re_path(r"questions/(?P<id>-?[0-9]\d*)/label/new/", QuestionLabelsView.as_view()),
    # 获取最热问题
    re_path(r"questions/(?P<id>-?[0-9]\d*)/label/hot/", QuestionHotView.as_view()),
    # 获取等待问题
    re_path(r"questions/(?P<id>-?[0-9]\d*)/label/wait/", QuestionWaitView.as_view()),
    # 注册发布问题的路由
    path('questions/', PostQuestion.as_view()),
    # 问题详情
    path("questions/<int:pk>/", QuestionDetail.as_view()),
    # 问题有用
    path("questions/<int:pk>/useful/", QuestionUseful.as_view()),
    # 问题没用
    path("questions/<int:pk>/unuseful/", QuestionUnuseful.as_view()),
    # # 回答问题
    path("reply/", QuestionReply.as_view()),
    # 回答有用
    path("reply/<int:pk>/useful/", ReplyUseful.as_view()),
    # 回答没用
    path("reply/<int:pk>/unuseful/", ReplyUnuseful.as_view()),
]
