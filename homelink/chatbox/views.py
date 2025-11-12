from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from service.models import Work
from .models import Conversation
from .forms import ConversationMessagesForm

@login_required
def new_text(request, work_pk):
    work = get_object_or_404(Work, pk=work_pk)

    if work.worker == request.user:
        return redirect('dashboard:dashboard')
    
    conversation = Conversation.objects.filter(work=work).filter(members__in=[request.user.id]).first()

    if conversation:
        return redirect ('chatbox:inbox_detail', pk=conversation.id)

    if request.method == 'POST':
        form = ConversationMessagesForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(work=work)
            conversation.members.add(request.user)
            conversation.members.add(work.worker)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.sender = (request.user)
            conversation_message.conversation = conversation  
            conversation_message.save()

            return redirect ('chatbox:inbox_detail', pk=conversation.id)
        
    else:
        form = ConversationMessagesForm()

    return render (request, 'chatbox/text.html', {
        'form':form,
        'work_pk':work_pk,
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render (request, 'chatbox/inbox.html', {
        'conversations':conversations,
    })

@login_required
def inbox_detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if not conversation:
        return redirect ('chatbox:inbox')

    if request.method == 'POST':
        form = ConversationMessagesForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.sender = (request.user)
            conversation_message.conversation = conversation
            conversation_message.save()

            return redirect ('chatbox:inbox_detail', pk=pk)
        
    else:
        form = ConversationMessagesForm()

    return render (request, 'chatbox/inbox_detail.html',{
        'conversation': conversation,
        'form':form,
    })