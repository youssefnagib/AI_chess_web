from django.shortcuts import render

# Create your views here.

def chat_bot(request):
    return render(request, 'chat_bot/chat_bot.html')