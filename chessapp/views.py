from django.shortcuts import render, redirect, get_object_or_404

def chess_view(request):
    return render(request, 'chess/chessBoard.html')

