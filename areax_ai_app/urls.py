
from django.urls import path
from .import views
urlpatterns = [
    path('user_registration',views.UserRegistrationView.as_view(),name="user_registration"),
    path('user_login',views.LoginView.as_view(),name="user_login"),
    path('user_logout',views.LogoutView.as_view(),name="user_logout"),
    path("generate_content",views.Generate_ContentAPIView.as_view(),name="generate_content"),
    path("edit_caption",views.EditCaptionAPIView.as_view(),name="edit_caption"),
    path("caption_list",views.Caption_listAPI.as_view(),name="caption_list"),
    path('google_photos', views.GooglePhotosAPI.as_view(), name='google_photos'),
    path('photo_search_caption', views.SearchCaptionImageAPI.as_view(), name='photo_search_caption'),
    path('ai_agent_input', views.TextInputHandler.as_view(), name='text_input_handler'),
    path('image_generation', views.GenerateImageView.as_view(), name='image_generation'),
    path('image/<int:pk>/', views.RetrieveImageView.as_view(), name='retrieve_image'),
    path('generate_video', views.GenerateVideoAPIView.as_view(), name='generate_video'),
    path('feedback', views.FeedbackAPIView.as_view(), name='feedback'),

    path('voice_chat', views.AudioTranscriptionView.as_view(), name='voice_chat'),
    # path('openai_chat_cost', views.ChatbotAPIView.as_view(), name='openai_with_cost'),
    path('total_cost_Chat', views.OverallCostAPIView.as_view(), name='total_cost_Chat'),
    path('db_image_generation', views.ImageGenerationAPIView.as_view(), name='total_cost_Chat'),
    path('total_cost_sd_image', views.TotalImageCostAPIView.as_view(), name='total_cost_sd_image'),

    path('gemini_caption', views.GeminiCaptionAPIView.as_view(), name='gemini_caption'),
    path('gemini_cost', views.Gemini_OverallCostAPIView.as_view(), name='gemini_cost'),
    path('gemini_daterange_cost', views.Gemini_daterangeCostAPI.as_view(), name='gemini_daterange_cost'),
    path('openai_daterange_cost', views.OpenAI_daterangeCostAPI.as_view(), name='openai_daterange_cost'),
    path('sd_daterange_cost', views.SD_daterangeCostAPI.as_view(), name='sd_daterange_cost'),

    path('user_based_survey', views.UserBasedProfileAPI.as_view(), name='user_based_survey'), ##29oct
    path('broadcast_agent', views.Pw_BroadcastAgentAPI.as_view(), name='broadcast_agent'), ##11nov
    path('audio_transcription_agent', views.Swedish_AudioTranscriptionAPIView.as_view(), name='audio_transcription_agent'), ##11nov
    path('llama_Status', views.LlamaStatusView.as_view(), name='llama_Status'), ##11nov
    path('llama_chat', views.HuggingFaceChatAPI.as_view(), name='llama_chat'), ##18nov
    path('runway_video', views.VideoGenerationAPIViewRun.as_view(), name='runway_video'), ##20nov runway
    path('modellab_video', views.VideoGenerationAPIView.as_view(), name='runway_video'), ##20nov
    path('mimage_video', views.ImageToVideoGenerationAPIModel.as_view(), name='mimage_video'), ##20nov
    path('voice_video', views.VoiceCommandVideoModelLabAPI.as_view(), name='voice_video'), ##20nov
    path('notification', views.Notification_LocationAPI.as_view(), name='notification'), ##03nov
    path('data_clean', views.CleanDataPipelineAPI.as_view(), name='data_clean'), ##03nov

    path('chat_retrieve', views.ChatRetrieveAPIView.as_view(), name='chat_retrieve'), ##027nov
    path('history_sync', views.HistoryAPIView.as_view(), name='history_sync'), ##30nov
    path('delete_history', views.HistoryDeleteAPI.as_view(), name='delete_history'), ##06nov
    path('mob_location', views.Mob_LocationAPI.as_view(), name='mob_location'), ##16 Jan

    path("together_chat", views.TogetherChatAPIView.as_view(), name="together_chat"),

    path("plm_chat", views.PLM_API.as_view(), name="plm_chat"),
    path("plm_voice", views.PLM_Voice_API.as_view() , name="plm_voice"),

    path('image_generation_gemini', views.ImageGenerationAPIGemini.as_view(), name='image_generation_gemini'),
    path('gemini_voice', views.Gemini_voiceChat.as_view(), name='gemini_voice'), ##06mar
    path('one_feed', views.GeminiSmartAPIView.as_view(), name='one_feed'), ##26mar
    path('chatsession_history', views.ChatHistoryAPI.as_view(), name='chat_session'), ##15april
    path('veo_video', views.GenerateVideoAPI.as_view(), name='veo_video'), ##17april
    path('sessions_api', views.AllSessionIDsAPI.as_view(), name='sessions_api'), ##18april
    path('sessionstitle_api', views.AllSessionTitleAPI.as_view(), name='sessionstitle_api'), ##18april
    path('onefeed_new', views.GenerateSmartContentAPI.as_view(), name='sessionstitle_api'), ##18april
    path('deletechat_session', views.DeleteChatHistoryAPI.as_view(), name='sessionstitle_api'), ##18april
]

