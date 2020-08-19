from django.urls import path
from apps.recruit.views import city, recruit, enterprise

urlpatterns = [
    # 注册获取热门城市的路由
    path('city/hotlist/', city.CityAPIView.as_view()),
    # 注册获取推荐职位的路由
    path('recruits/search/recommend/', recruit.RecruitRecommendAPIView.as_view()),
    # 注册获取最新职位的路由
    path('recruits/search/latest/', recruit.RecruitLatestAPIView.as_view()),
    # 注册热门企业子路由
    path('enterprise/search/hotlist/', enterprise.EnterpriseHotAPIView.as_view()),
    # 注册搜索职位子路由
    path('recruits/search/city/keyword/', recruit.RecruitSearchAPIView.as_view()),
    # 注册获取职位详情的自路由
    path('recruits/<int:pk>/', recruit.RecruitDetailAPIView.as_view()),
    # 注册增加职位访问次数的子路由
    path('recruits/<int:pk>/visit/', recruit.RecruitAddAPIView.as_view()),
    # 注册收藏职位的自路由
    path('recruits/<int:pk>/collect/', recruit.CollectRecruitAPIView.as_view()),
    # 取消收藏
    path('recruits/<int:pk>/cancelcollect/', recruit.CollectRecruitAPIViews.as_view()),
    # 注册企业详情子路由
    path('enterprise/<int:pk>/', enterprise.EnterpriseDetailAPIView.as_view()),
    # 注册增加奇特访问次数的子路由
    path('enterprise/<int:pk>/visit/', enterprise.EnterpriseVisitAPIView.as_view()),
    # 注册收藏企业的自路由
    path('enterprise/<int:pk>/collect/', enterprise.CollectEnterpriseAPIView.as_view()),
    # 取消收藏
    path('enterprise/<int:pk>/cancelcollect/', enterprise.CollectEnterpriseAPIViews.as_view()),
    # 添加搜索路由
    path('search/', recruit.MySearchView())
]
