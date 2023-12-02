from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from . import nftall
from thirdweb.types.nft import NFTMetadataInput
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import json
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction

def home(request):
    if request.method == 'POST' and request.FILES.get('home'):
        name_nft = request.POST.get('name', '')
        description_nft = request.POST.get('description', '')
        image_nft = request.FILES['home']
        image_nft.name = request.POST.get('name', '')
        prop = {}

        # Additional fields processing
        additional_properties = request.POST.get('additional_properties', '{}')
        try:
            prop = json.loads(additional_properties)
        except json.JSONDecodeError:
            prop = {}

        nft_metadata = {
            'name': name_nft,
            'description': description_nft,
            'image': image_nft,
            'properties': prop
        }

        try:
            nftall.nft_collection.mint(NFTMetadataInput.from_json(nft_metadata))
            return redirect("success")
        except Exception as e:
            messages.error(request, 'Failed to mint NFT: {}'.format(str(e)))
            return redirect("home")
   
    return render(request, "index.html", {})

@login_required
def user_profile(request):
    # Display user profile information
    user_info = {
        'username': request.user.username,
        'email': request.user.email
        # Add more user-specific information here
    }
    return render(request, "profile.html", {'user_info': user_info})

def success(request):
    # Enhanced success view
    return HttpResponse("Success! Your NFT has been minted.")

@transaction.atomic
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Failed to create user: {}'.format(str(e)))
            return redirect('create_user')

    return render(request, "create_user.html", {})

def custom_404_view(request, exception):
    return render(request, '404.html', {})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Process the form data
        request.user.email = request.POST.get('email', request.user.email)
        # Add other fields you want to update
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    return render(request, 'edit_profile.html')

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload_file.html', {'uploaded_file_url': uploaded_file_url})
    
    return render(request, 'upload_file.html')

def list_nfts(request):
    nfts = nftall.nft_collection.get_all()
    return render(request, 'list_nfts.html', {'nfts': nfts})
def contact(request):
    if request.method == 'POST':
        # Process the contact form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Here you would typically send an email or store the message
        messages.success(request, 'Thank you for your message!')
        return redirect('home')

    return render(request, 'contact.html')


