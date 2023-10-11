from django.shortcuts import render, redirect
from mail.models import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime, timedelta
import uuid
from django.contrib.auth import logout, login

# Create your views here.
def home(request):
    user = request.user  
    return render(request, 'home.html', {'user': user})

def connexion(request):
    if request.method == "POST":   
        email = request.POST.get('email')
        password = request.POST.get('password')
                
        user = Utilisateur.objects.filter(email=email).first()        
        if user is not None:
            if user.is_active==0:
                if user.check_password(password):
                    if user.confirmation_token and user.created_at:
                        expiration = user.created_at + timedelta(hours=2)
                        if datetime.now() <= expiration:
                            messages.error(request,"Veuillez consulter vos mails. Une url vous a été envoyé pour validation de compte!")
                            return render(request, 'login.html')
                        else:
                            new_confirmation_token = str(uuid.uuid4())
                            user.confirmation_token = new_confirmation_token
                            user.created_at = datetime.now()
                            user.save()
                            
                            confirmation_url = request.build_absolute_uri('/confirm/' + new_confirmation_token)
                            sendmail(request, confirmation_url, user.email)
                            return render(request, 'confirmation.html')
                    else:
                        new_confirmation_token = str(uuid.uuid4())
                        user.confirmation_token = new_confirmation_token
                        user.created_at = datetime.now()
                        user.save()
                        
                        confirmation_url = request.build_absolute_uri('/confirm/' + new_confirmation_token)
                        sendmail(request, confirmation_url, user.email)
                        return render(request, 'confirmation.html')
                else:
                    messages.error(request,"Email ou mot de passe non valide")
            else:      
                if user.check_password(password):
                    login(request, user)                    
                    return redirect('home')
                else:
                    messages.error(request, "Mot de passe non valide")
        else:
            messages.error(request,"Email ou mot de passe non valide")
    return render(request, 'connexion.html')

def confirmation_view(request, confirmation_token):
    try:
        user = Utilisateur.objects.get(confirmation_token=confirmation_token, is_active=False)
        user.is_active = True 
        user.confirmation_token = None  
        user.save()
        return redirect('login')
    except Utilisateur.DoesNotExist:
        messages.error(request, 'Le lien de confirmation est invalide ou a déjà été utilisé.')
        return redirect('inscription') 

def inscription(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        photo = request.FILES['photo']
        password = request.POST.get('password')
        
        try:
            utilisateur = Utilisateur.objects.get(email=email)
            messages.error(request, 'Cet email existe déjà.')
        except Utilisateur.DoesNotExist:
            utilisateur = None

        if utilisateur is None and len(password) >= 6:
            user = Utilisateur.objects.create_user(
                first_name=nom,
                last_name=prenom,
                email=email,
                username=email,
                numero=telephone,
                photo=photo,
                password=password
            )
            user.set_password(password)
            user.is_active = False
            confirmation_token = str(uuid.uuid4())
            user.confirmation_token = confirmation_token
            user.save()
            
            
            confirmation_url = request.build_absolute_uri('/confirm/' + confirmation_token)

            sendmail(request, confirmation_url, email)
            return redirect('confirmation')
        elif len(password) < 6:
            messages.error(request, 'Le mot de passe doit avoir au moins 6 caractères')

    return render(request, 'inscription.html')

def sendmail(request, url, email):
    subject = "Voici l'url de connexion"
    from_email = "mdtech3007@gmail.com"
    to_email = email  
    message = render_to_string('url-mail.html', {'email': email, 'url': url})
                                            
    send_mail(subject, strip_tags(message), from_email, [to_email], html_message=message)
       
    request.session['email']=email
    request.session['url']=url
    durée_expiration = timedelta(hours=2)  
    request.session.set_expiry(durée_expiration.total_seconds())
    
def confirmation_page(request):
    return render(request, 'confirmation.html')

def deconnexion(request):
    logout(request)
    return redirect('login')
