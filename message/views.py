from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Message, ResponseMeesage
from users.models import CustomUser
from .forms import SendMessageAdmin, SendMessageUsers

def calculate_number_of_sent(user_messages_send):
	user_messages_send_list = []
	temp = user_messages_send[0].title
	user_messages_send_list.append(user_messages_send[0])
	for i in range(1, len(user_messages_send)):
		if temp == user_messages_send[i].title and user_messages_send[i].reciver.userType == 'is_admin' and user_messages_send[i].messageType == "send":
			temp = user_messages_send[i].title
			continue
		else:
			user_messages_send_list.append(user_messages_send[i])
	return user_messages_send_list  



@login_required(login_url='signpage')
def send_message(request, pk):
	user_messages_send = Message.objects.filter(sender=request.user)
	number_of_sent = user_messages_send.count()
	user_messages_send_list = []
	if number_of_sent >= 1:
		user_messages_send_list = calculate_number_of_sent(user_messages_send)
		number_of_sent = len(user_messages_send_list)
	user_inbox = Message.objects.filter(reciver=request.user)
	number_of_inbox =user_inbox.count()
	obj = request.user
	if request.method == "POST" and 'send_content' in request.POST:
		if obj.userType == 'is_admin':
			form = SendMessageAdmin(request.POST)
			if form.is_valid():
				sender = request.user
				message_recivers = form.cleaned_data['reciver_user']
				title = form.cleaned_data['title']
				content = form.cleaned_data['send_content']
				recivers = CustomUser.objects.filter(userType = message_recivers)
				for reciver in recivers:
					message = Message.objects.create(sender=sender, reciver=reciver, title=title, send_content=content)
				return redirect('messages', pk)

		else:
			form = SendMessageUsers(request.POST)
			if form.is_valid():
				sender = request.user
				title = form.cleaned_data['title']
				content = form.cleaned_data['send_content']
				recivers = CustomUser.objects.filter(userType = "is_admin")
				for reciver in recivers:
					message = Message.objects.create(sender=sender, reciver=reciver, title=title, send_content=content)
				return redirect('messages', pk)



	else:
		if obj.userType == 'is_admin':

			form = SendMessageAdmin()
		else:
			form = SendMessageUsers()

		messages =[]
		for message in user_messages_send_list:
			messages.append({'reciver': message.reciver.username, 'title': message.title, 'date_message': message.date_message.strftime("%Y-%m-%d %H:%M:%S"),
							'visualized':message.visualized, 'urls' : message.get_absolute_url_inbox()})

	return render(request, 'message.html', {'form':form, 'messages':messages, 'number_of_sent':number_of_sent, 'number_of_inbox':number_of_inbox})



@login_required(login_url='signpage')
def inbox(request, pk):
	if request.method == 'POST':
		pass

	else:
		user_inbox = Message.objects.filter(reciver = request.user)
		number_of_inbox = user_inbox.count()
		messages = []
		for message in user_inbox:
			messages.append({'title': message.title, 'date_message': message.date_message.strftime("%Y-%m-%d %H:%M:%S"),
							 'urls' : message.get_absolute_url_inbox(), 'visualized':message.visualized, 'sender': message.sender.username})


			
		return JsonResponse({'messages':messages, 'count':number_of_inbox}, status=200)


@login_required(login_url='signpage')
def send(request, pk):
	if request.method == 'POST':
		pass
	else:
		user_messages_send = Message.objects.filter(sender = request.user)
		user_messages_send_list = []
		if user_messages_send.count() >= 1:
			user_messages_send_list = calculate_number_of_sent(user_messages_send)
		number_of_sent = len(user_messages_send_list)
		messages = []
		for message in user_messages_send_list:
			if request.user.userType != 'is_admin':
				reciver_name = 'Admin'
			else:
				reciver_name = message.reciver.username
			messages.append({'title': message.title, 'date_message': message.date_message.strftime("%Y-%m-%d %H:%M:%S"),
							 'urls' : message.get_absolute_url_send(), 'content':message.send_content, 'reciver': reciver_name})
		return JsonResponse({'messages': messages, 'count':number_of_sent}, status=200)



@login_required(login_url='signpage') 
def send_detail(request, slug):
	message_details = Message.objects.filter(slug = slug)
	for message_detail in message_details:
		message_details = message_detail
	if request.user.userType == 'is_admin':
		reciver = message_details.reciver.username
	else:
		reciver = 'Admin'
	message = {'content_message':message_details.send_content, 'seen': message_details.visualized, 
	'title':message_details.title,'date_message':message_details.date_message.strftime("%Y-%m-%d %H:%M:%S"),
	'reciver':reciver}
	return JsonResponse({'message':message}, status=200)



@login_required(login_url='signpage') 
def inbox_detail(request, slug):
	global message_details
	message = Message.objects.filter(slug = slug)
	message.update(visualized = True)
	if request.method == 'POST':
		ResponseMeesage.objects.create(
			message=message_details,
			content=request.POST.get('content'),
			author = request.user
			)
		for inbox_message in message :
			my_message = inbox_message
		sender = request.user
		title = my_message.title
		content = request.POST.get('content')
		reciver = my_message.sender
		messageType = "replay"
		Message.objects.create(sender=sender, reciver=reciver, title=title, send_content=content, messageType=messageType)
		return redirect(inbox , request.user.pk)
	else:
		message_details = Message.objects.filter(slug = slug)
		for message_detail in message_details:
			message_details = message_detail
		message = {'content_message':message_details.send_content, 'seen': message_details.visualized, 
		'title':message_details.title,'date_message':message_details.date_message.strftime("%Y-%m-%d %H:%M:%S"),
		'sender':message_details.sender.username}
		return JsonResponse({'message':message}, status=200)


